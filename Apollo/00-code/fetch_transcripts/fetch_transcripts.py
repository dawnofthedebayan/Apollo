#!/usr/bin/env python3
"""
Recursively scans Debayan_Personal/07-consume/landing_area for .md files,
finds YouTube URLs, fetches transcripts, and saves _transcripts.md files.
"""

import os
import re
import sys

# ── Path resolution ───────────────────────────────────────────────────────────
def get_root():
    if os.getenv("GITHUB_ACTIONS"):
        return os.path.join(os.environ["GITHUB_WORKSPACE"], "Debayan_Personal")
    return os.path.expanduser(
        "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal"
    )

SCAN_DIR = os.path.join(get_root(), "07-consume", "landing_area")

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_video_id(url):
    patterns = [
        r'(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})',
        r'(?:embed/)([A-Za-z0-9_-]{11})'
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None

def fetch_transcript(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
    try:
        ytt = YouTubeTranscriptApi()                    # instantiate — new v1.0 API
        fetched = ytt.fetch(video_id)                   # replaces get_transcript()
        segments = fetched.to_raw_data()                # convert to list of dicts
        return "\n".join(
            f"[{int(s['start']//60):02d}:{int(s['start']%60):02d}] {s['text']}"
            for s in segments
        )
    except TranscriptsDisabled:
        return None, "Transcripts are disabled for this video"
    except NoTranscriptFound:
        return None, "No transcript found for this video"
    except Exception as e:
        return None, str(e)

def extract_tags(content):
    """Extract tags, strip # prefix, skip transcripts tag."""
    return [m.lstrip("#") for m in re.findall(r'(?<!\S)#[\w\/]+', content)
            if not m.startswith("#type/consume/transcripts")]

def extract_youtube_url(content):
    urls = re.findall(r'https?://[^\s\)"]+', content)
    for url in urls:
        if "youtu" in url:
            return url
    return None

# ── Main scan ─────────────────────────────────────────────────────────────────
def scan_and_fetch(dry_run=False):
    if not os.path.isdir(SCAN_DIR):
        print(f"ERROR: Directory not found: {SCAN_DIR}")
        sys.exit(1)

    print(f"📂 Scanning: {SCAN_DIR}\n")

    found = skipped = created = failed = 0

    for dirpath, _, filenames in os.walk(SCAN_DIR):
        for filename in filenames:
            # Skip non-md and already-transcript files
            if not filename.endswith(".md"):
                continue
            if filename.endswith("_transcripts.md"):
                continue

            filepath = os.path.join(dirpath, filename)
            stem = filename[:-3]  # strip .md
            transcript_filename = stem + "_transcripts.md"
            transcript_path = os.path.join(dirpath, transcript_filename)

            # Skip if transcript already exists
            if os.path.exists(transcript_path):
                print(f"  ⏭  Already exists: {transcript_filename}")
                skipped += 1
                continue

            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            url = extract_youtube_url(content)
            if not url:
                print(f"  ➖ No YouTube URL: {filename}")
                skipped += 1
                continue

            found += 1
            video_id = get_video_id(url)
            if not video_id:
                print(f"  ⚠️  Could not extract video ID from: {url}")
                failed += 1
                continue

            print(f"  ▶  Fetching transcript for: {filename}")
            print(f"     URL: {url}")

            result = fetch_transcript(video_id)

            # fetch_transcript returns tuple on error, string on success
            if isinstance(result, tuple):
                _, err = result
                print(f"     ❌ Failed: {err}\n")
                failed += 1
                continue

            transcript_text = result
            tags = extract_tags(content)
            tags.append("type/consume/transcripts")  # no # prefix
            tags_yaml = "\n  - ".join(tags)

            note_content = f"""---
tags:
  - {tags_yaml}
source_note: "[[{stem}]]"
youtube_url: "{url}"
---

# Transcript: {stem}

{transcript_text}
"""
            if not dry_run:
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(note_content)
                print(f"     ✅ Saved: {transcript_filename}\n")
            else:
                print(f"     🔍 [DRY RUN] Would save: {transcript_filename}\n")
            created += 1

    print("─" * 50)
    print(f"  Found:   {found} notes with YouTube URLs")
    print(f"  Created: {created} transcript files")
    print(f"  Skipped: {skipped} (no URL or already exists)")
    print(f"  Failed:  {failed}")
    if dry_run:
        print("\n  💡 Set dry_run=False to write files.")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    scan_and_fetch(dry_run=dry_run)