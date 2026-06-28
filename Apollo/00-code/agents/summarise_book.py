import os
import re
import json
import asyncio
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import textwrap
from tqdm import tqdm
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from util.llm_utils import MLXChatModel
from util.obsidian_utils import write_obsidian_note


# ==========================================
# 1. LLM Setup
# ==========================================

# ~750 tokens per 1000 chars. DeepSeek V4 Flash has 1M token context.
# We cap a single chunk at ~100k chars (~75k tokens) to leave plenty of
# headroom for the prompt wrapper and the output.
# For MLX (local, memory-bound) we keep chunks small.
CHUNK_SIZE = {
    "openrouter": 100_000,
    "mlx": 1_000,
}

# Max parallel chunk requests. OpenRouter can handle many; MLX is sequential.
MAX_WORKERS = {
    "openrouter": 8,
    "mlx": 1,
}

def setup_llm(provider="mlx"):
    if provider == "openrouter":
        return ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
            model="deepseek/deepseek-v4-flash",
            temperature=0.5,
        )
    elif provider == "mlx":
        return MLXChatModel(
            model_path="lmstudio-community/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit",
            max_tokens=1024,
        )
    else:
        raise ValueError("Provider must be 'openrouter' or 'mlx'")


# ==========================================
# 2. Non-Fiction Agents
# ==========================================
def nonfiction_chunk_summarizer(llm, chunk_text):
    prompt = f"""You are a rigorous study assistant helping a reader deeply understand a non-fiction book.

Read the following passage and extract:
- The core argument or idea being made
- Any frameworks, models, or mental models introduced
- Key facts, data points, or evidence cited
- Terms or concepts that need to be understood to follow the argument

Output as a concise bulleted list. Prioritise depth over breadth — a well-explained point beats five shallow ones.

PASSAGE:
{chunk_text}"""
    return llm.invoke([HumanMessage(content=prompt)]).content


def nonfiction_chapter_synthesizer(llm, chunk_notes, rolling_context):
    prompt = f"""You are a teacher helping a student truly understand a non-fiction book, not just remember it.

WHAT HAS BEEN COVERED SO FAR:
{rolling_context if rolling_context else "This is the opening chapter."}

NOTES FROM THIS CHAPTER:
{chunk_notes}

Write a chapter summary in three parts:

**Core Idea** (1 paragraph)
What is the single most important thing this chapter argues or teaches? Explain it as if to someone encountering it for the first time. Use analogies where they help.

**How It Fits** (1 paragraph)
How does this chapter's idea build on, challenge, or reframe what came before? What is the author setting up for later?

**Key Takeaways** (5 bullet points)
Concrete, specific insights a reader should walk away with. Avoid vague statements — each point should be something the reader could explain to someone else or apply.

**Reflection Prompt**
End with a single open question that invites the reader to connect this chapter's ideas to their own experience or prior knowledge."""
    return llm.invoke([HumanMessage(content=prompt)]).content


def nonfiction_memory_manager(llm, current_chapter_summary, rolling_context):
    if not rolling_context:
        return current_chapter_summary
    prompt = f"""You are maintaining a running map of a non-fiction book's argument.

ARGUMENT SO FAR:
{rolling_context}

LATEST CHAPTER:
{current_chapter_summary}

Update the running map by:
- Integrating the new chapter's core idea into the overall argument
- Noting how the book's central thesis is evolving or deepening
- Flagging any new frameworks or concepts introduced that will likely matter later
- Keeping the total under 500 words

Write in clear, connected prose — this is a living outline of the book's intellectual journey."""
    return llm.invoke([HumanMessage(content=prompt)]).content


# ==========================================
# 3. Fiction Agents
# ==========================================
def fiction_chunk_summarizer(llm, chunk_text):
    prompt = f"""You are a thoughtful literary reader helping someone follow and appreciate a work of fiction.

Read the following passage and note:
- What happens (plot events, decisions, turning points)
- Who is involved and how they behave or change
- The emotional texture of the scene — what is the reader meant to feel?
- Any symbols, recurring motifs, or moments that feel thematically loaded

Output as a concise bulleted list. Pay attention to subtext — what is left unsaid often matters as much as what is written.

PASSAGE:
{chunk_text}"""
    return llm.invoke([HumanMessage(content=prompt)]).content


def fiction_chapter_synthesizer(llm, chunk_notes, rolling_context):
    prompt = f"""You are a perceptive literary guide helping a reader engage deeply with a work of fiction.

STORY SO FAR:
{rolling_context if rolling_context else "This is the opening chapter."}

NOTES FROM THIS CHAPTER:
{chunk_notes}

Write a chapter summary in three parts:

**What Happened** (1 paragraph)
Summarise the key events and character moments. Focus on what changed — in the plot, in relationships, in a character's understanding of themselves or their world.

**What It Means** (1 paragraph)
Step back from the plot. What is the author doing here? What themes, ideas, or human truths is this chapter exploring? How do the events connect to the larger story the author is trying to tell?

**Things to Hold** (5 bullet points)
Specific details — a line of dialogue, a character choice, an image, a moment of tension — that are worth remembering as the story continues. These are the threads the author may pull on later.

**Reflection Prompt**
End with a single question that invites the reader to sit with this chapter — something that connects the story to the reader's own life, relationships, or understanding of the world."""
    return llm.invoke([HumanMessage(content=prompt)]).content


def fiction_memory_manager(llm, current_chapter_summary, rolling_context):
    if not rolling_context:
        return current_chapter_summary
    prompt = f"""You are tracking the living story of a novel.

STORY SO FAR:
{rolling_context}

LATEST CHAPTER:
{current_chapter_summary}

Update the story map by:
- Weaving in the new chapter's events and their consequences
- Noting how characters are evolving or being revealed
- Tracking any themes or motifs that are deepening
- Flagging unresolved tensions or questions the story is building toward
- Keeping the total under 500 words

Write in flowing prose, as if briefing someone who wants to understand not just what happened but why it matters."""
    return llm.invoke([HumanMessage(content=prompt)]).content


# ==========================================
# 4. Agent Dispatcher
# ==========================================
AGENTS = {
    "nonfiction": {
        "chunk":   nonfiction_chunk_summarizer,
        "chapter": nonfiction_chapter_synthesizer,
        "memory":  nonfiction_memory_manager,
        "tag":     "genre/non-fiction",
    },
    "fiction": {
        "chunk":   fiction_chunk_summarizer,
        "chapter": fiction_chapter_synthesizer,
        "memory":  fiction_memory_manager,
        "tag":     "genre/fiction",
    },
}


# ==========================================
# 5. EPUB Parsing
# ==========================================
def parse_and_chunk_epub(epub_path, max_chunk_chars=1000):
    print(f"Parsing EPUB: {epub_path}...")
    try:
        book = epub.read_epub(epub_path)
    except Exception as e:
        print(f"Error reading EPUB: {e}")
        return []

    chapters_and_chunks = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        html_content = item.get_body_content()
        if not html_content:
            continue
        soup = BeautifulSoup(html_content, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        if not text:
            continue
        chapter_chunks = textwrap.wrap(text, width=max_chunk_chars)
        if chapter_chunks:
            chapters_and_chunks.append(chapter_chunks)

    return chapters_and_chunks


def get_book_title(epub_path: str) -> str:
    try:
        book = epub.read_epub(epub_path)
        title = book.get_metadata("DC", "title")
        if title:
            return title[0][0].strip()
    except Exception:
        pass
    return os.path.splitext(os.path.basename(epub_path))[0]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


# ==========================================
# 6. State Management
# ==========================================
def state_path(epub_path: str, book_title: str) -> str:
    folder = os.path.dirname(epub_path)
    safe_title = re.sub(r'[\\/*?:"<>|]', "", book_title)
    return os.path.join(folder, f"{safe_title}.state.json")


def load_state(epub_path: str, book_title: str) -> dict:
    path = state_path(epub_path, book_title)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        print(f"Resuming from saved state: {len(state['chapters_done'])} chapter(s) already done.")
        return state
    return {"chapters_done": {}, "rolling_context": ""}


def save_state(epub_path: str, book_title: str, state: dict):
    path = state_path(epub_path, book_title)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def clear_state(epub_path: str, book_title: str):
    path = state_path(epub_path, book_title)
    if os.path.exists(path):
        os.remove(path)
        print(f"State file cleared: {path}")


# ==========================================
# 7. Parallel Chunk Summarisation
# ==========================================
async def _summarise_chunk_async(semaphore, chunk_fn, llm, chunk, pbar):
    """Run one chunk summarisation with concurrency control."""
    async with semaphore:
        loop = asyncio.get_event_loop()
        # LangChain's invoke is sync; run it in a thread pool so we don't block
        result = await loop.run_in_executor(None, chunk_fn, llm, chunk)
        pbar.update(1)
        return result


async def summarise_chunks_parallel(chunk_fn, llm, chunks, max_workers, pbar):
    """Fire all chunk summaries concurrently, bounded by max_workers."""
    semaphore = asyncio.Semaphore(max_workers)
    tasks = [
        _summarise_chunk_async(semaphore, chunk_fn, llm, chunk, pbar)
        for chunk in chunks
    ]
    return await asyncio.gather(*tasks)


# ==========================================
# 8. Main Orchestrator
# ==========================================
def process_book(epub_path, provider="mlx", book_type="nonfiction"):
    if book_type not in AGENTS:
        raise ValueError("book_type must be 'nonfiction' or 'fiction'")

    agents = AGENTS[book_type]
    llm = setup_llm(provider)
    chapters = parse_and_chunk_epub(epub_path, max_chunk_chars=CHUNK_SIZE[provider])
    book_title = get_book_title(epub_path)
    workers = MAX_WORKERS[provider]

    print(f"\nBook    : {book_title}")
    print(f"Type    : {book_type}")
    print(f"Provider: {provider}")
    print(f"Chunk size: {CHUNK_SIZE[provider]:,} chars | Parallel workers: {workers}")
    print(f"Chapters found: {len(chapters)}\n")

    state = load_state(epub_path, book_title)
    chapters_done = state["chapters_done"]
    rolling_context = state["rolling_context"]

    final_book_output = {f"Chapter {k}": v for k, v in chapters_done.items()}

    chapter_bar = tqdm(chapters, desc="Chapters", unit="ch", colour="green")

    for i, chapter_chunks in enumerate(chapter_bar):
        chapter_num = i + 1
        chapter_key = str(chapter_num)
        chapter_bar.set_description(f"Chapter {chapter_num}/{len(chapters)}")

        if chapter_key in chapters_done:
            chapter_bar.set_postfix_str("skipped (cached)")
            continue

        # Parallel chunk summarisation
        chunk_pbar = tqdm(
            total=len(chapter_chunks),
            desc="  Chunks",
            unit="chunk",
            leave=False,
            colour="cyan",
        )
        chunk_summaries = asyncio.run(
            summarise_chunks_parallel(
                agents["chunk"], llm, chapter_chunks, workers, chunk_pbar
            )
        )
        chunk_pbar.close()

        combined_chunk_notes = "\n\n".join(chunk_summaries)

        chapter_bar.set_postfix_str("synthesising...")
        chapter_summary = agents["chapter"](llm, combined_chunk_notes, rolling_context)
        final_book_output[f"Chapter {chapter_num}"] = chapter_summary

        chapter_bar.set_postfix_str("updating memory...")
        rolling_context = agents["memory"](llm, chapter_summary, rolling_context)

        chapters_done[chapter_key] = chapter_summary
        state["rolling_context"] = rolling_context
        save_state(epub_path, book_title, state)

        chapter_bar.set_postfix_str("done")

    tag_llm = (
        "llm/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit"
        if provider == "mlx"
        else "llm/openrouter"
    )

    print("\n=== BOOK PROCESSING COMPLETE ===")
    write_obsidian_note(
        title=book_title,
        sections=final_book_output,
        vault_subfolder="03-resources/books/book-summaries",
        tags=[
            "resource/book",
            f"title/{slugify(book_title)}",
            agents["tag"],
            tag_llm,
            "generated",
        ],
    )

    clear_state(epub_path, book_title)
    return final_book_output


# ==========================================
# Run
# ==========================================
if __name__ == "__main__":
    book_path = (
        "/Users/debayanbhattacharya/Library/Mobile Documents/"
        "iCloud~md~obsidian/Documents/Debayan_Personal/"
        "03-resources/books/epubs/ML/Designing ML Systems.epub"
    )
    results = process_book(book_path, provider="openrouter", book_type="nonfiction")