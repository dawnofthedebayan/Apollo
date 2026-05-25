#!/usr/bin/env python3
"""
generate_manifest.py
Scans 07-Apollo/ for quiz JSON files and writes docs/manifest.json.
Run locally or via GitHub Actions.
"""

import json
import re
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).resolve().parent          # 00-code/knowledge_agent/
APOLLO_DIR   = SCRIPT_DIR.parent.parent                 # 07-Apollo/
QUIZZES_ROOT = APOLLO_DIR                               # scan subfolders of 07-Apollo/
DOCS_DIR     = APOLLO_DIR / "docs"
MANIFEST_OUT = DOCS_DIR / "manifest.json"

# Folders to skip when scanning for quiz JSON files
SKIP_FOLDERS = {"00-code", "docs", ".git"}

# Human-friendly labels for folder names (optional — auto-generated if not listed)
FOLDER_LABELS = {
    "01-journals":  "Journals",
    "05-idea":      "Ideas",
    "03-references": "References",
    "04-people":    "People",
    "02-projects":  "Projects",
}

# ── Scan ──────────────────────────────────────────────────────────────────────
def humanise(folder_name: str) -> str:
    """02-idea → Ideas  (falls back to title-cased name if not in FOLDER_LABELS)"""
    if folder_name in FOLDER_LABELS:
        return FOLDER_LABELS[folder_name]
    return re.sub(r"^\d+-", "", folder_name).replace("-", " ").title()


def build_manifest() -> list[dict]:
    manifest = []

    for folder in sorted(QUIZZES_ROOT.iterdir()):
        if not folder.is_dir():
            continue
        if folder.name in SKIP_FOLDERS or folder.name.startswith("."):
            continue

        json_files = sorted(f.name for f in folder.glob("*.json"))
        if not json_files:
            continue

        manifest.append({
            "folder": folder.name,
            "label":  humanise(folder.name),
            "files":  json_files,
        })
        print(f"  📂 {folder.name}: {len(json_files)} file(s)")

    return manifest


# ── Write ─────────────────────────────────────────────────────────────────────
def write_manifest(manifest: list[dict]) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_OUT.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n✅ manifest.json written → {MANIFEST_OUT}")
    print(f"   {len(manifest)} folder(s), "
          f"{sum(len(f['files']) for f in manifest)} quiz file(s) total")


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"🔍 Scanning: {QUIZZES_ROOT}\n")
    manifest = build_manifest()

    if not manifest:
        print("⚠️  No quiz JSON files found. Nothing written.")
    else:
        write_manifest(manifest)