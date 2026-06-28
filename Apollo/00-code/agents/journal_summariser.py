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
# 0. Configuration
# ==========================================
VAULT_BASE = os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal"
)
print(VAULT_BASE)
JOURNAL_DIR     = os.path.join(VAULT_BASE, "01-journals")
DAILY_DIR       = os.path.join(JOURNAL_DIR, "daily")
WEEKLY_DIR      = os.path.join(JOURNAL_DIR, "weekly")
PROCESSED_DB_PATH = os.path.join(JOURNAL_DIR, "processed_entries.json")

# ==========================================
# 1. Custom LangChain Wrapper for MLX
# ==========================================
class MLXLocalLLM(LLM):
    """A custom LangChain wrapper for Apple MLX models."""
    model: Any
    tokenizer: Any
    max_tokens: int = 2048

    @property
    def _llm_type(self) -> str:
        return "mlx_local"


    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        stop_sequences = stop or [
            "<|im_end|>",
            "<|endoftext|>",
            "</think>",
        ]

        output_tokens = []

        for response in stream_generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=self.max_tokens,
        ):
            token_text = response.text
            output_tokens.append(token_text)
            print(token_text, end="", flush=True)

            current_output = "".join(output_tokens)
            if any(seq in current_output for seq in stop_sequences):
                break

        print()
        result = "".join(output_tokens).strip()

        for seq in stop_sequences:
            if seq in result:
                result = result[:result.index(seq)].strip()

        return result

# ==========================================
# 2. Processed Entries Database
# ==========================================
def load_processed_db() -> dict:
    if not os.path.exists(PROCESSED_DB_PATH):
        return {}
    with open(PROCESSED_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_processed_db(db: dict) -> None:
    with open(PROCESSED_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

def get_report_key(year: int, week: int) -> str:
    return f"{year}-WEEK-{week:02d}"

# ==========================================
# 3. Week Parsing from Filenames
# ==========================================
def parse_year_week_from_file(filepath: str) -> Optional[Tuple[int, int]]:
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
def discover_all_entries(directory: str = DAILY_DIR) -> Dict[Tuple[int, int], List[str]]:
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
    needs_run = []

    for (year, week), files in grouped.items():
        key = get_report_key(year, week)
        processed_basenames = set(db.get(key, []))
        all_basenames = {os.path.basename(f) for f in files}

        has_new = bool(all_basenames - processed_basenames)

        if has_new:
            needs_run.append((year, week))

    needs_run.sort()
    return needs_run

# ==========================================
# 6. Content Loading
# ==========================================
def load_entries(file_paths: List[str]) -> str:
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
    output_dir: str = WEEKLY_DIR,
) -> str:
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{report_key}.md")

    frontmatter = (
        "---\n"
        f"title: \"Weekly Therapeutic Summary - {report_key}\"\n"
        f"date: \"{datetime.now().strftime('%Y-%m-%d')}\"\n"
        "tags:\n"
        "  - type/journal\n"
        "  - generated\n"
        "  - llm/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit\n"
        "---\n\n"
    )

    heading = (
        f"# Weekly Therapeutic Summary - {report_key}\n"
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
    report_key = get_report_key(year, week)
    chain = therapist_prompt | llm

    print(f"\n{'=' * 60}")
    print(f"  Processing {report_key}  ({len(files)} entries)")
    print(f"{'=' * 60}")

    journal_text = load_entries(files)
    print(journal_text)

    print("  Analysing patterns and generating summary...")
    response = chain.invoke({"journal_entries": journal_text})

    output_path = write_weekly_report(report_key, response)
    print(f"  Report written -> {output_path}")

    db[report_key] = sorted(os.path.basename(f) for f in files)
    save_processed_db(db)
    print(f"  Database updated ({len(db[report_key])} entries recorded)")

# ==========================================
# 10. Main Execution
# ==========================================
def main():
    current_yw = get_current_year_week()
    current_key = get_report_key(*current_yw)

    print(f"Journal Therapist - running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current ISO period : {current_key}\n")

    db = load_processed_db()

    grouped = discover_all_entries(DAILY_DIR)
    print("grouped:", grouped)
    if not grouped:
        print("No journal entries found. Nothing to do.")
        return

    to_process = weeks_needing_processing(grouped, db, current_yw)
    print("Weeks to process:", to_process)

    if not to_process:
        print("All journal entries are up to date. Nothing to do.")
        return

    print(f"Weeks requiring processing: {[get_report_key(y, w) for y, w in to_process]}\n")

    print("Loading MLX Model...")
    model, tokenizer = load("lmstudio-community/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit")
    llm = MLXLocalLLM(model=model, tokenizer=tokenizer, max_tokens=1200)

    for year, week in to_process:
        process_week(year, week, grouped[(year, week)], llm, db)

    print(f"\nDone. Processed {len(to_process)} week(s).")

if __name__ == "__main__":
    main()