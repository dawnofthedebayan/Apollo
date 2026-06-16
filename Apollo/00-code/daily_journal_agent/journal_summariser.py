import os
import glob
import json
import re
from datetime import datetime, date
from typing import Any, List, Optional, Dict, Tuple
from mlx_lm import load, stream_generate

from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.prompts import PromptTemplate

# ==========================================
# 1. Custom LangChain Wrapper for MLX
# ==========================================
class MLXLocalLLM(LLM):
    """A custom LangChain wrapper for Apple MLX models."""
    model: Any
    tokenizer: Any
    max_tokens: int = 2048

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        stop_sequences = stop or [
            "<|endoftext|>",
            "<|im_end|>",
            "\nUser:",
            "\nuser:",
            "\nHuman:",
            "\nAssistant:",
        ]

        output_tokens = []

        for response in stream_generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=self.max_tokens,
        ):
            # response.text is the newly decoded chunk (one or more chars)
            token_text = response.text
            print(token_text, end="", flush=True)

            output_tokens.append(token_text)
            current_output = "".join(output_tokens)

            # Check if any stop sequence has appeared in the accumulated output
            for seq in stop_sequences:
                if seq in current_output:
                    # Trim everything from the stop sequence onward
                    current_output = current_output[:current_output.index(seq)]
                    print()  # newline after streaming ends
                    return current_output.strip()

        print()  # newline after streaming ends
        return "".join(output_tokens).strip()

    @property
    def _llm_type(self) -> str:
        return "mlx_local"

# ==========================================
# 2. Processed Entries Database
# ==========================================
PROCESSED_DB_PATH = "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal/01-journals/processed_entries.json"

def load_processed_db() -> dict:
    """
    Loads the JSON database of processed weekly reports.
    Structure: { "2025-WEEK-03": ["file1.md", "file2.md", ...], ... }
    """
    if not os.path.exists(PROCESSED_DB_PATH):
        return {}
    with open(PROCESSED_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_processed_db(db: dict) -> None:
    """Persists the processed entries database to disk."""
    with open(PROCESSED_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def get_report_key(year: int, week: int) -> str:
    """Returns the canonical key/filename stem, e.g. '2025-WEEK-03'."""
    return f"{year}-WEEK-{week:02d}"

# ==========================================
# 3. Week Parsing from Filenames
# ==========================================
def parse_year_week_from_file(filepath: str) -> Optional[Tuple[int, int]]:
    """
    Extracts (ISO year, ISO week) from the file's last-modified timestamp.
    Returns None if the path does not exist or the stat call fails.
    """
    try:
        mtime = os.path.getmtime(filepath)
        modified_date = date.fromtimestamp(mtime)
        iso = modified_date.isocalendar()
        return iso.year, iso.week
    except OSError:
        return None

# ==========================================
# 4. Discovering All Entries, Grouped by Week
# ==========================================
def discover_all_entries(directory: str = "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal/01-journals") -> Dict[Tuple[int, int], List[str]]:
    """
    Scans `directory` for all .md files (non-recursively) and groups them
    by (year, week). Files that cannot be dated are silently skipped.

    Returns: { (year, week): [sorted list of absolute paths], ... }
    """
    all_md = glob.glob(os.path.join(directory, "*.md"))
    grouped: Dict[Tuple[int, int], List[str]] = {}
    print("all_md:", all_md)

    for path in sorted(all_md):
        result = parse_year_week_from_file(path)
        if result is None:
            continue
        year, week = result
        grouped.setdefault((year, week), []).append(path)

    return grouped

def get_current_year_week() -> Tuple[int, int]:
    """Returns the ISO (year, week) for today."""
    iso = date.today().isocalendar()
    return iso.year, iso.week

# ==========================================
# 5. Deciding Which Weeks Need Processing
# ==========================================
def weeks_needing_processing(
    grouped: Dict[Tuple[int, int], List[str]],
    db: dict,
    current_year_week: Tuple[int, int],
) -> List[Tuple[int, int]]:
    """
    Returns a sorted list of (year, week) tuples that require a (re-)run.

    A week needs processing when:
      - It is the current ISO week AND at least one of its files is not yet
        recorded in the database  (new entry added mid-week → overwrite report).
      - It is a past week AND it has at least one file not recorded in the
        database  (week was never processed, or new files were back-filled).

    Weeks are returned in chronological order so older gaps are filled first.
    """
    needs_run = []
    current_key = get_report_key(*current_year_week)

    for (year, week), files in grouped.items():
        key = get_report_key(year, week)
        processed_basenames = set(db.get(key, []))
        all_basenames = {os.path.basename(f) for f in files}

        has_new = bool(all_basenames - processed_basenames)

        if has_new:
            needs_run.append((year, week))

    # Chronological order: older weeks first, current week last
    needs_run.sort()
    return needs_run

# ==========================================
# 6. Content Loading
# ==========================================
def load_entries(file_paths: List[str]) -> str:
    """Concatenates content from a list of .md file paths with separators."""
    combined = []
    for path in sorted(file_paths):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        filename = os.path.basename(path)
        combined.append(f"--- Entry: {filename} ---\n{content}\n")
    return "\n".join(combined)

# ==========================================
# 7. Prompt Engineering
# ==========================================
therapist_prompt = PromptTemplate.from_template("""
You are an insightful, empathetic, and highly trained personal therapist. Your client is sharing their personal journal entries from a specific week.

Your task is to read these entries and provide an ELABORATE, deep, and constructive summary that helps the client self-reflect.

Focus on the following:
1. Emotional Arcs: What were the dominant emotions this week? How did they shift from the beginning to the end?
2. Behavioral & Cognitive Patterns: Are there recurring thoughts, triggers, or habits (positive or negative) that the client should be aware of?
3. Unspoken Themes: Read between the lines. What underlying needs, anxieties, or desires might be driving their experiences?
4. Reflective Questions: Conclude with 2-3 gentle but profound questions for the client to ponder to foster growth.

Maintain a warm, objective, and supportive tone. Do not judge; simply observe and guide.

Here are the journal entries for this week:

{journal_entries}

Please provide your elaborate therapeutic summary below:
""")

# ==========================================
# 8. Output
# ==========================================
def write_weekly_report(
    report_key: str,
    content: str,
    output_dir: str = "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal/01-journals/weekly"
) -> str:
    """
    Writes (or overwrites) the weekly summary .md file.
    Returns the path of the written file.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{report_key}.md")

    # Frontmatter: ONLY valid YAML between the --- fences.
    # The heading and body go AFTER the closing fence.
    frontmatter = (
        "---\n"
        f"title: \"Weekly Therapeutic Summary — {report_key}\"\n"
        f"date: \"{datetime.now().strftime('%Y-%m-%d')}\"\n"
        "tags:\n"
        "  - type/journal\n"
        "  - generated\n"
        "  - llm/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit\n"
        "---\n\n"
    )

    heading = (
        f"# Weekly Therapeutic Summary — {report_key}\n"
        f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(frontmatter + heading + content.strip() + "\n")

    return output_path


# ==========================================
# 9. Per-Week Processing
# ==========================================
def process_week(
    year: int,
    week: int,
    files: List[str],
    llm,
    db: dict,
) -> None:
    """
    Generates (or regenerates) the therapeutic summary for a single week
    and updates the database entry for that week.
    """
    report_key = get_report_key(year, week)
    chain = therapist_prompt | llm

    print(f"\n{'=' * 60}")
    print(f"  Processing {report_key}  ({len(files)} entries)")
    print(f"{'=' * 60}")

    journal_text = load_entries(files)
    print(journal_text)

    print("  Analysing patterns and generating summary…")
    response = chain.invoke({"journal_entries": journal_text})

    output_path = write_weekly_report(report_key, response)
    print(f"  ✓ Report written → {output_path}")

    # Record ALL files for this week so future runs skip them (unless new
    # files appear, in which case the diff check above will catch them).
    db[report_key] = sorted(os.path.basename(f) for f in files)
    save_processed_db(db)
    print(f"  ✓ Database updated ({len(db[report_key])} entries recorded)")

# ==========================================
# 10. Main Execution
# ==========================================
def main():
    journal_dir = "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal/01-journals"
    current_yw = get_current_year_week()
    current_key = get_report_key(*current_yw)

    print(f"Journal Therapist — running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current ISO period : {current_key}\n")

    # Load database of already-processed entries
    db = load_processed_db()

    # Discover every dateable .md file, grouped by (year, week)
    grouped = discover_all_entries(journal_dir + "/daily")
    print("grouped:", grouped)
    if not grouped:
        print("No journal entries found in 01-journal/. Nothing to do.")
        return

    # Work out which weeks actually need a (re-)run
    to_process = weeks_needing_processing(grouped, db, current_yw)
    print("Weeks to process:", to_process)

    if not to_process:
        print("All journal entries are up to date. Nothing to do.")
        return

    print(f"Weeks requiring processing: {[get_report_key(y, w) for y, w in to_process]}\n")

    # Load the model once and reuse it across all weeks
    print("Loading MLX Model…")
    model, tokenizer = load("lmstudio-community/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit")
    llm = MLXLocalLLM(model=model, tokenizer=tokenizer, max_tokens=500)

    for year, week in to_process:
        process_week(year, week, grouped[(year, week)], llm, db)

    print(f"\nDone. Processed {len(to_process)} week(s).")

if __name__ == "__main__":
    main()