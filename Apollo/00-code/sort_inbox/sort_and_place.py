import os
import re
import shutil
import glob
from datetime import datetime


# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────


def get_vault_path():
    is_github_actions = os.getenv("GITHUB_ACTIONS") == "true"
    if is_github_actions:
        return os.path.join(os.getenv("GITHUB_WORKSPACE", "."), "Debayan_Personal")
    else:
        return os.path.expanduser(
            "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal"
        )


# ─────────────────────────────────────────────
# TAG NORMALISATION
# ─────────────────────────────────────────────

TAG_ALIASES = {
    "type/book":       "type/book",
    "type/books":      "type/book",
    "type/article":    "type/article",
    "type/articles":   "type/article",
    "type/journal":    "type/journal",
    "type/daily":      "type/journal",
    "type/reflection": "type/reflection",
    "type/project":    "type/project",
    "type/projects":   "type/project",
    "type/course":     "type/course",
    "type/podcast":    "type/podcast",
    "type/person":     "type/person",
    "type/concept":    "type/concept",
    "type/learning":   "type/concept",
    "type/idea":       "type/concept",
    "type/consume":    "type/consume",
}


def normalise_tag(raw_tag: str) -> str:
    tag = raw_tag.lstrip("#").strip().lower()
    return TAG_ALIASES.get(tag, tag)


# ─────────────────────────────────────────────
# ROUTING RULES — type tag only
# ─────────────────────────────────────────────

TYPE_FOLDER_MAP = {
    "type/journal":    "01-journals/daily",
    "type/reflection": "01-journals/reflections",
    "type/project":    "02-projects/landing_area",
    "type/book":       "03-resources/books",
    "type/article":    "03-resources/articles",
    "type/course":     "03-resources/courses",
    "type/podcast":    "03-resources/podcast",
    "type/person":     "04-people/landing_area",
    "type/concept":    "06-concept/landing_area",
    "type/consume":    "07-consume/landing_area",
    "type/consumed":    "07-consume/landing_area",
}


# ─────────────────────────────────────────────
# TAG EXTRACTION
# ─────────────────────────────────────────────

def extract_inline_tags(content: str) -> list[str]:
    """Find all #tag/subtag patterns in the note body (outside frontmatter)."""
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, flags=re.DOTALL)
    return re.findall(r"(?<!\w)#([\w/-]+)", body)


def extract_frontmatter_tags(content: str) -> list[str]:
    """Extract tags from YAML frontmatter block."""
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not fm_match:
        return []
    fm_block = fm_match.group(1)
    list_tags = re.findall(r"^\s*-\s+(.+)$", fm_block, re.MULTILINE)
    inline_match = re.search(r"tags:\s*\[([^\]]+)\]", fm_block)
    if list_tags:
        return [t.strip() for t in list_tags]
    elif inline_match:
        return [t.strip() for t in inline_match.group(1).split(",")]
    return []


def get_all_tags(content: str) -> list[str]:
    """Merge inline + frontmatter tags, normalise, deduplicate."""
    raw = extract_inline_tags(content) + extract_frontmatter_tags(content)
    normalised = [normalise_tag(t) for t in raw]
    return list(dict.fromkeys(normalised))


# ─────────────────────────────────────────────
# FRONTMATTER INJECTION
# ─────────────────────────────────────────────

def inject_frontmatter(content: str, tags: list[str], filepath: str) -> str:
    """Rewrite or add YAML frontmatter with normalised tags."""
    filename_stem = os.path.splitext(os.path.basename(filepath))[0]
    today = datetime.now().strftime("%Y-%m-%d")
    tag_lines = "\n".join(f"  - {t}" for t in tags)
    new_fm = f"---\ntitle: \"{filename_stem}\"\ndate: {today}\ntags:\n{tag_lines}\n---\n"

    if re.match(r"^---\s*\n", content):
        return re.sub(r"^---\s*\n.*?\n---\s*\n", new_fm, content, flags=re.DOTALL)
    return new_fm + content


# ─────────────────────────────────────────────
# ROUTING — type tag only
# ─────────────────────────────────────────────

def resolve_destination(tags: list[str], vault_path: str) -> str | None:
    type_tag = next((t for t in tags if t.startswith("type/")), None)
    if type_tag and type_tag in TYPE_FOLDER_MAP:
        return os.path.join(vault_path, TYPE_FOLDER_MAP[type_tag])
    return None


# ─────────────────────────────────────────────
# FILE MOVE
# ─────────────────────────────────────────────

def move_and_update(src: str, dest_folder: str, updated_content: str, dry_run: bool) -> str:
    os.makedirs(dest_folder, exist_ok=True)
    filename = os.path.basename(src)
    dest_path = os.path.join(dest_folder, filename)

    if os.path.exists(dest_path):
        stem, ext = os.path.splitext(filename)
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        dest_path = os.path.join(dest_folder, f"{stem}_{ts}{ext}")

    if not dry_run:
        with open(src, "w", encoding="utf-8") as f:
            f.write(updated_content)
        shutil.move(src, dest_path)

    return dest_path


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def sort_inbox(dry_run: bool = True):
    vault_path = get_vault_path()
    inbox_path = os.path.join(vault_path, "00-inbox")

    print(f"{'[DRY RUN] ' if dry_run else ''}🔍 Scanning: {inbox_path}\n")

    md_files = glob.glob(os.path.join(inbox_path, "**/*.md"), recursive=True)
    if not md_files:
        print("📭 Inbox is empty.")
        return

    moved, unmatched, no_tags = [], [], []

    for filepath in sorted(md_files):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tags        = get_all_tags(content)
        destination = resolve_destination(tags, vault_path)
        filename    = os.path.basename(filepath)

        if not tags:
            print(f"❌ NO TAGS   {filename}\n")
            no_tags.append(filepath)
            continue

        if destination:
            updated_content = inject_frontmatter(content, tags, filepath)
            dest_path = move_and_update(filepath, destination, updated_content, dry_run)
            verb = "WOULD MOVE" if dry_run else "MOVED"
            print(f"🔀 {verb}  {filename}")
            print(f"   raw tags  : {re.findall(r'(?<!\w)#([\w/-]+)', content)}")
            print(f"   normalised: {tags}")
            print(f"   to        : {dest_path}\n")
            moved.append(filepath)
        else:
            print(f"⚠️  NO RULE   {filename}")
            print(f"   tags      : {tags}\n")
            unmatched.append(filepath)

    print("=" * 60)
    print(f"✅ {'Would move' if dry_run else 'Moved'} : {len(moved)}")
    print(f"⚠️  No matching rule : {len(unmatched)}")
    print(f"❌ No tags found     : {len(no_tags)}")
    if dry_run:
        print("\n💡 Set dry_run=False to execute.")


if __name__ == "__main__":
    sort_inbox(dry_run=False)