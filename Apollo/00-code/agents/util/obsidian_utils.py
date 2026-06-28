import os
import re
from datetime import date

VAULT_BASE = "/Users/debayanbhattacharya/Library/Mobile Documents/iCloud~md~obsidian/Documents/Debayan_Personal"
def write_obsidian_note(
    title: str,
    sections: dict,
    vault_subfolder: str,
    tags: list[str] = None,
    extra_frontmatter: dict = None,
):
    """
    Write an Obsidian-friendly markdown note.

    Args:
        title:             Note title — used as filename and H1 heading.
        sections:          Ordered dict of {heading: content} for the note body.
        vault_subfolder:   Path relative to VAULT_BASE, e.g. "03-resources/books/book-summaries".
        tags:              List of tags, e.g. ["resource/book", "title/my-book"].
                           Strings with spaces are auto-slugified.
        extra_frontmatter: Any additional YAML frontmatter fields, e.g. {"author": "Chip Huyen"}.
    """
    tags = tags or []
    extra_frontmatter = extra_frontmatter or {}

    output_dir = os.path.join(VAULT_BASE, vault_subfolder)
    os.makedirs(output_dir, exist_ok=True)

    # Sanitise filename — strip characters that cause issues on macOS/iCloud
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    output_path = os.path.join(output_dir, f"{safe_title}.md")

    today = date.today().isoformat()
    slugified_tags = [slugify(t) if " " in t else t for t in tags]

    # Build YAML frontmatter
    lines = [
        "---",
        f'title: "{title}"',
        f"date: {today}",
    ]

    for key, value in extra_frontmatter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f'{key}: "{value}"')

    if slugified_tags:
        lines.append("tags:")
        for tag in slugified_tags:
            lines.append(f"  - {tag}")

    lines += ["---", "", f"# {title}", ""]

    # Build body
    for heading, content in sections.items():
        lines.append(f"## {heading}")
        lines.append("")
        lines.append(content.strip())
        lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Note written: {output_path}")
    return output_path