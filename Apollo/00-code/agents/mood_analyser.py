import os
import glob
import json
import re
from datetime import datetime, date
from typing import Any, List, Optional, Dict

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
JOURNAL_DIR      = os.path.join(VAULT_BASE, "01-journals")
DAILY_DIR        = os.path.join(JOURNAL_DIR, "daily")
MOOD_ANALYSIS_DIR = os.path.join(JOURNAL_DIR, "mood_analysis")
MOOD_DB_PATH      = os.path.join(MOOD_ANALYSIS_DIR, "mood_data.json")

# Reasoning models like R1 can burn a lot of tokens on the <think> block
# before ever reaching the final answer. Classification output is short,
# but the thinking can still be long, so keep this generous.
DEFAULT_MAX_TOKENS = 3072

# Allowed values -- kept here so the prompt and any downstream analysis
# scripts agree on the same vocabulary.
PRIMARY_EMOTIONS = [
    "happy", "content", "calm", "excited", "grateful",
    "sad", "anxious", "angry", "frustrated", "lonely",
    "stressed", "tired", "neutral", "mixed",
]
SOCIAL_CONTACT_VALUES = ["alone", "with_others", "mixed", "unclear"]

# ==========================================
# 1. Custom LangChain Wrapper for MLX
# ==========================================
class MLXLocalLLM(LLM):
    """A custom LangChain wrapper for Apple MLX models."""
    model: Any
    tokenizer: Any
    max_tokens: int = DEFAULT_MAX_TOKENS

    @property
    def _llm_type(self) -> str:
        return "mlx_local"

    def _format_prompt(self, prompt: str) -> str:
        """Apply the model's chat template so it's properly cued into a
        fresh assistant turn. Without this, reasoning models are less
        consistent about opening/closing the <think> block."""
        try:
            messages = [{"role": "user", "content": prompt}]
            return self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
            )
        except Exception as e:
            print(f"  [warn] apply_chat_template failed ({e}); using raw prompt")
            return prompt

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
        ]

        formatted_prompt = self._format_prompt(prompt)

        output_tokens = []

        for response in stream_generate(
            self.model,
            self.tokenizer,
            prompt=formatted_prompt,
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

        has_open_think = "<think>" in result
        has_close_think = "</think>" in result

        if has_open_think and not has_close_think:
            print(
                "  [WARNING] Output was truncated mid-<think> block "
                f"(max_tokens={self.max_tokens}). No final answer was reached.\n"
                "  Consider increasing max_tokens or shortening the input."
            )
            return "[GENERATION TRUNCATED]"

        match = re.search(r"</think>\s*(.*)", result, re.DOTALL)
        if match:
            result = match.group(1).strip()

        return result

# ==========================================
# 2. Processed Entries Database
# ==========================================
def load_mood_db() -> Dict[str, dict]:
    """Keyed by filename -> mood record, so we can skip already-processed
    entries and just append new ones on each run."""
    if not os.path.exists(MOOD_DB_PATH):
        return {}
    with open(MOOD_DB_PATH, "r", encoding="utf-8") as f:
        records = json.load(f)
    return {r["filename"]: r for r in records}

def save_mood_db(db: Dict[str, dict]) -> None:
    os.makedirs(MOOD_ANALYSIS_DIR, exist_ok=True)
    records = sorted(db.values(), key=lambda r: r.get("date") or "")
    with open(MOOD_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)

# ==========================================
# 3. Date Parsing from Filename
# ==========================================
DATE_IN_FILENAME_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

def parse_date_from_file(filepath: str) -> str:
    """Prefer a YYYY-MM-DD date embedded in the filename (typical for daily
    notes). Fall back to the file's last-modified date if none is found."""
    basename = os.path.basename(filepath)
    match = DATE_IN_FILENAME_RE.search(basename)
    if match:
        return match.group(1)

    mtime = os.path.getmtime(filepath)
    return date.fromtimestamp(mtime).strftime("%Y-%m-%d")

# ==========================================
# 4. Discovering Entries to Process
# ==========================================
def discover_daily_entries(directory: str = DAILY_DIR) -> List[str]:
    all_md = glob.glob(os.path.join(directory, "*.md"))
    print("all_md:", all_md)
    return sorted(all_md)

def entries_needing_processing(files: List[str], db: Dict[str, dict]) -> List[str]:
    to_process = []
    for path in files:
        basename = os.path.basename(path)
        existing = db.get(basename)
        if existing is None:
            to_process.append(path)
            continue
        # Re-process if the file has changed since we last classified it.
        mtime = os.path.getmtime(path)
        if existing.get("_source_mtime") != mtime:
            to_process.append(path)
    return to_process

# ==========================================
# 5. Content Loading
# ==========================================
def load_entry(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# ==========================================
# 6. Prompt Engineering
# ==========================================
mood_classifier_prompt = PromptTemplate.from_template("""
You are an expert at reading personal journal entries and extracting structured mood
data for later quantitative analysis. Read the journal entry below and classify it.

Respond with ONLY a single valid JSON object. No preamble, no explanation, no markdown
code fences, no text before or after the JSON. Just the raw JSON object.

Use exactly this schema:

{{
  "primary_emotion": one of {emotion_list},
  "secondary_emotions": [list of 0-3 additional emotions from the same list, or empty list],
  "valence": integer from -5 (very negative) to 5 (very positive),
  "arousal": one of "low", "medium", "high" (how energised/activated vs. calm/flat the entry feels),
  "topics": [list of short lowercase tags, e.g. "work", "health", "family", "finance", "travel", "hobbies", "relationships"],
  "sleep_mentioned": true or false,
  "sleep_quality": one of "poor", "ok", "good", or null if not mentioned,
  "social_contact": one of {social_list},
  "notable_event": true or false (was there a significant/unusual event this day),
  "summary": a single plain-English sentence (max 25 words) capturing the gist of the day,
  "confidence": float from 0.0 to 1.0 representing how confident you are in this classification given the entry's clarity and length
}}

If the entry is very short or ambiguous, still fill in your best judgment and lower the confidence score accordingly.

Journal entry:

{journal_entry}

JSON object:
""")

# ==========================================
# 7. Response Parsing
# ==========================================
def extract_json(raw_text: str) -> Optional[dict]:
    """The model is asked for raw JSON only, but strip common wrapping
    (code fences, stray prose) defensively before parsing."""
    text = raw_text.strip()

    # Strip markdown code fences if present.
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    # If there's still leading/trailing prose, grab the outermost {...}.
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace == -1 or last_brace == -1 or last_brace < first_brace:
        return None
    candidate = text[first_brace:last_brace + 1]

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None

def validate_and_clean(record: dict) -> dict:
    """Coerce fields to expected types/ranges so bad LLM output doesn't
    silently corrupt the dataset."""
    cleaned = dict(record)

    if cleaned.get("primary_emotion") not in PRIMARY_EMOTIONS:
        cleaned["primary_emotion"] = "unclear"

    secondary = cleaned.get("secondary_emotions")
    if not isinstance(secondary, list):
        cleaned["secondary_emotions"] = []
    else:
        cleaned["secondary_emotions"] = [
            e for e in secondary if e in PRIMARY_EMOTIONS
        ][:3]

    try:
        valence = int(cleaned.get("valence"))
        cleaned["valence"] = max(-5, min(5, valence))
    except (TypeError, ValueError):
        cleaned["valence"] = 0

    if cleaned.get("arousal") not in ("low", "medium", "high"):
        cleaned["arousal"] = "medium"

    topics = cleaned.get("topics")
    if not isinstance(topics, list):
        cleaned["topics"] = []
    else:
        cleaned["topics"] = [str(t).lower().strip() for t in topics if t]

    cleaned["sleep_mentioned"] = bool(cleaned.get("sleep_mentioned", False))
    if cleaned.get("sleep_quality") not in ("poor", "ok", "good"):
        cleaned["sleep_quality"] = None

    if cleaned.get("social_contact") not in SOCIAL_CONTACT_VALUES:
        cleaned["social_contact"] = "unclear"

    cleaned["notable_event"] = bool(cleaned.get("notable_event", False))

    summary = cleaned.get("summary")
    cleaned["summary"] = str(summary).strip() if summary else ""

    try:
        confidence = float(cleaned.get("confidence"))
        cleaned["confidence"] = max(0.0, min(1.0, confidence))
    except (TypeError, ValueError):
        cleaned["confidence"] = 0.5

    return cleaned

# ==========================================
# 8. Per-Entry Processing
# ==========================================
def process_entry(filepath: str, llm, db: Dict[str, dict]) -> None:
    basename = os.path.basename(filepath)
    entry_date = parse_date_from_file(filepath)

    print(f"\n{'=' * 60}")
    print(f"  Classifying {basename}  (date: {entry_date})")
    print(f"{'=' * 60}")

    journal_text = load_entry(filepath)

    if not journal_text.strip():
        print("  Empty entry, skipping.")
        return

    chain = mood_classifier_prompt | llm
    raw_response = chain.invoke({
        "journal_entry": journal_text,
        "emotion_list": json.dumps(PRIMARY_EMOTIONS),
        "social_list": json.dumps(SOCIAL_CONTACT_VALUES),
    })

    if raw_response == "[GENERATION TRUNCATED]":
        print(f"  Skipping {basename}: generation was truncated. Will retry next run.")
        return

    parsed = extract_json(raw_response)
    if parsed is None:
        print(f"  [ERROR] Could not parse JSON from model output for {basename}. "
              f"Skipping (will retry next run).")
        print("  Raw output was:")
        print(raw_response)
        return

    cleaned = validate_and_clean(parsed)
    cleaned["filename"] = basename
    cleaned["date"] = entry_date
    cleaned["_source_mtime"] = os.path.getmtime(filepath)
    cleaned["_classified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db[basename] = cleaned
    save_mood_db(db)

    print(f"  -> mood={cleaned['primary_emotion']} valence={cleaned['valence']} "
          f"arousal={cleaned['arousal']} confidence={cleaned['confidence']}")
    print(f"  Database updated ({len(db)} total entries recorded)")

# ==========================================
# 9. Main Execution
# ==========================================
def main():
    print(f"Mood Classifier - running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    db = load_mood_db()

    files = discover_daily_entries(DAILY_DIR)
    if not files:
        print("No journal entries found. Nothing to do.")
        return

    to_process = entries_needing_processing(files, db)
    print(f"Entries requiring classification: {len(to_process)} of {len(files)}\n")

    if not to_process:
        print("All journal entries are up to date. Nothing to do.")
        return

    print("Loading MLX Model...")
    model, tokenizer = load("lmstudio-community/DeepSeek-R1-0528-Qwen3-8B-MLX-4bit")
    llm = MLXLocalLLM(model=model, tokenizer=tokenizer, max_tokens=DEFAULT_MAX_TOKENS)

    for filepath in to_process:
        process_entry(filepath, llm, db)

    print(f"\nDone. Classified {len(to_process)} entr{'y' if len(to_process) == 1 else 'ies'}.")
    print(f"Mood data written to: {MOOD_DB_PATH}")

if __name__ == "__main__":
    main()