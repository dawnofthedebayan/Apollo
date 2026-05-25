import os
import json
import sys
from pathlib import Path
from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()


# ── Pydantic schema ──────────────────────────────────────────────────────────
class MCQOption(BaseModel):
    label: str = Field(description="The label for the option (e.g., 'A', 'B', 'C', 'D')")
    text: str = Field(description="The text content of the option")


class MCQQuestion(BaseModel):
    question: str = Field(description="The question text")
    options: List[MCQOption] = Field(description="List of answer options")
    correct_answer: str = Field(description="The correct answer label (e.g., 'A', 'B', 'C', 'D')")
    explanation: str = Field(description="Brief explanation of the correct answer")
    source: str = Field(description="'document' if based on the md file, 'llm' if general knowledge")


class QuizOutput(BaseModel):
    file: str = Field(description="Original markdown filename")
    topic: str = Field(description="Inferred topic of the document")
    questions: List[MCQQuestion]


# ── LLM setup ────────────────────────────────────────────────────────────────
llm = ChatOpenRouter(
    model="anthropic/claude-sonnet-4-5",
    temperature=0.3,
    api_key=os.environ["OPENROUTER_API_KEY"],  # hard fail if missing — no silent None
)

structured_llm = llm.with_structured_output(QuizOutput)


# ── Prompt ────────────────────────────────────────────────────────────────────
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert quiz generator and educator. Your goal is to help the user deeply understand and retain the topic by crafting questions that progressively build from foundational recall to advanced critical thinking.

Given a markdown document, generate exactly 10 MCQ questions in two groups:

GROUP 1 — Document-Based Questions (source: "document"), questions 1–5:
  - Q1 (Beginner):     Simple recall — a key term, definition, or fact directly stated in the document.
  - Q2 (Easy):         Basic comprehension — understanding a concept or relationship explained in the document.
  - Q3 (Intermediate): Application — applying a concept from the document to a slightly different scenario.
  - Q4 (Hard):         Analysis — identifying why something works, comparing ideas, or interpreting a nuanced point from the document.
  - Q5 (Expert):       Synthesis/Evaluation — connecting multiple concepts from the document, identifying edge cases, or critically evaluating a claim made in the document.

GROUP 2 — General Knowledge Questions (source: "llm"), questions 6–10:
  - Q6  (Beginner):     A simple, well-known fact about the broader topic.
  - Q7  (Easy):         A concept commonly associated with the topic that extends beyond the document.
  - Q8  (Intermediate): A practical or real-world application of the topic.
  - Q9  (Hard):         A nuanced or commonly misunderstood aspect of the topic.
  - Q10 (Expert):       An advanced question requiring deep domain knowledge — edge cases, trade-offs, or expert-level reasoning about the topic.

Rules:
- Each question must have exactly 4 options (A, B, C, D) with exactly one correct answer.
- Distractors (wrong answers) must be plausible — avoid obviously wrong options.
- Questions must escalate in cognitive demand within each group.
- Label each question with its difficulty level: Beginner | Easy | Intermediate | Hard | Expert.
- Return only valid structured output. No extra text."""),
    ("human", "Filename: {filename}\n\nContent:\n{content}")
])

chain = prompt | structured_llm


# ── Serialise QuizOutput → plain dict ────────────────────────────────────────
def quiz_to_dict(result: QuizOutput) -> dict:
    return {
        "file": result.file,
        "topic": result.topic,
        "questions": [
            {
                "question": q.question,
                "options": [{"label": o.label, "text": o.text} for o in q.options],
                "correct_answer": q.correct_answer,
                "explanation": q.explanation,
                "source": q.source,
            }
            for q in result.questions
        ],
    }


# ── Convert QuizOutput → Markdown ────────────────────────────────────────────
def quiz_to_markdown(result: QuizOutput) -> str:
    difficulty_map = {0: "Beginner", 1: "Easy", 2: "Intermediate", 3: "Hard", 4: "Expert"}
    lines = [
        f"# Quiz: {result.topic}",
        f"> Source file: `{result.file}`\n",
        "---\n",
        "## 📄 Group 1 — Document-Based Questions\n",
    ]

    for i, q in enumerate(result.questions):
        if i == 5:
            lines.append("## 🧠 Group 2 — General Knowledge Questions\n")

        difficulty = difficulty_map.get(i % 5, "")
        source_icon = "📄" if q.source == "document" else "🧠"
        lines.append(f"### Q{i+1} `{difficulty}` {source_icon}")
        lines.append(f"\n**{q.question}**\n")
        for opt in q.options:
            marker = "✅" if opt.label == q.correct_answer else "  "
            lines.append(f"- {marker} **{opt.label}.** {opt.text}")
        lines.append(f"\n> 💡 **Explanation:** {q.explanation}\n")
        lines.append("---\n")

    return "\n".join(lines)


# ── Tracker helpers ───────────────────────────────────────────────────────────
def get_processed_files(tracker_path: Path) -> set:
    if tracker_path.exists():
        return set(json.loads(tracker_path.read_text()))
    return set()


def mark_as_processed(tracker_path: Path, filename: str) -> None:
    processed = get_processed_files(tracker_path)
    processed.add(filename)
    tracker_path.write_text(json.dumps(list(processed), indent=2))


# ── Core processing ───────────────────────────────────────────────────────────
def process_folder(folder_path: str, output_dir: str) -> int:
    """
    Returns the number of files successfully processed (used as exit code signal).
    """
    folder = Path(folder_path).resolve()
    output = Path(output_dir).resolve()

    if not folder.exists():
        print(f"❌ Input folder not found: {folder}", flush=True)
        sys.exit(1)

    output.mkdir(parents=True, exist_ok=True)

    tracker = folder / ".processed.json"
    processed = get_processed_files(tracker)
    md_files = list(folder.rglob("*.md"))

    print(f"📂 Input:  {folder}", flush=True)
    print(f"📂 Output: {output}", flush=True)
    print(f"📄 Found {len(md_files)} markdown files. {len(processed)} already processed.\n", flush=True)

    success_count = 0

    for md_file in md_files:
        filename = md_file.name

        if filename in processed:
            print(f"  ⏭  Skipping (already processed): {filename}", flush=True)
            continue

        content = md_file.read_text(encoding="utf-8")

        if len(content.strip()) < 100:
            print(f"  ⚠  Skipping (too short): {filename}", flush=True)
            continue

        print(f"  ⚙  Processing: {filename}", flush=True)

        try:
            result: QuizOutput = chain.invoke({"filename": filename, "content": content})

            stem = md_file.stem

            # Save Markdown
            md_out = output / f"{stem}.md"
            md_out.write_text(quiz_to_markdown(result), encoding="utf-8")

            # Save JSON (for the web quiz player)
            json_out = output / f"{stem}.json"
            json_out.write_text(json.dumps(quiz_to_dict(result), indent=2, ensure_ascii=False), encoding="utf-8")

            mark_as_processed(tracker, filename)
            print(f"  ✅ Saved: {md_out.name}  +  {json_out.name}", flush=True)
            success_count += 1

        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}", flush=True)

    print(f"\n🏁 Done. {success_count} file(s) processed.", flush=True)
    return success_count


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Paths via env vars (GitHub Actions) with local fallbacks
    input_folder = os.environ.get(
        "QUIZ_INPUT_DIR",
        "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal/05-idea",
    )
    output_folder = os.environ.get(
        "QUIZ_OUTPUT_DIR",
        "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal/07-Apollo/02-idea",
    )

    process_folder(input_folder, output_folder)
    