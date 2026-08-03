#!/usr/bin/env python3
"""MiGraph Script: update_schema

Purpose:
- Backfill unified frontmatter fields (id, version, confidence, source) on
  existing wiki pages that predate the unified schema.

Usage:
- Prefer `python scripts/migraph update-schema --root /path/to/my-wiki`.
- Run `python scripts/update_schema.py --help` for direct CLI details.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from utils import PAGE_TYPE_TO_DIR, collect_wiki_pages, parse_frontmatter, read_text, write_text

DIR_TO_TYPE = {value: key for key, value in PAGE_TYPE_TO_DIR.items()}

VERSION = '"1.0.0"'
CONFIDENCE = "high"
SOURCE = "docs"


def get_id(meta: dict[str, object], filepath: Path, page_type: str) -> str:
    domain = str(meta.get("domain") or "").strip()
    if not domain:
        domain = str(meta.get("category") or "").strip().lower()
    slug = filepath.stem
    return f"{domain or slug}.{page_type}.{slug}"


def ensure_field(content: str, field: str, value: str) -> str:
    if f"{field}:" in content:
        return content

    lines = content.split("\n")
    new_lines = []
    inserted = False

    for _i, line in enumerate(lines):
        new_lines.append(line)
        if line.strip().startswith("updated:") and not inserted:
            new_lines.append(f"{field}: {value}")
            inserted = True

    if not inserted:
        new_lines.append(f"{field}: {value}")
    return "\n".join(new_lines)


def process_file(filepath: Path, page_type: str) -> bool:
    try:
        content = read_text(filepath)
    except Exception:
        return False

    if not content.startswith("---"):
        return False

    meta, _body = parse_frontmatter(content)
    if meta.get("id") and meta.get("version") and meta.get("confidence") and meta.get("source"):
        return False

    page_id = str(meta.get("id") or get_id(meta, filepath, page_type))
    updated = content
    if not meta.get("id"):
        updated = ensure_field(updated, "id", page_id)
    if not meta.get("version"):
        updated = ensure_field(updated, "version", VERSION)
    if not meta.get("confidence"):
        updated = ensure_field(updated, "confidence", CONFIDENCE)
    if not meta.get("source"):
        updated = ensure_field(updated, "source", SOURCE)

    if updated != content:
        write_text(filepath, updated)
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill unified frontmatter fields on wiki pages.")
    parser.add_argument("--root", default=".", help="Wiki root path")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    wiki = root / "wiki"
    if not wiki.is_dir():
        print(f"No wiki/ directory found under {root}", file=sys.stderr)
        return 1

    total = 0
    for page in collect_wiki_pages(root):
        page_type = DIR_TO_TYPE.get(page.parent.name)
        if page_type is None:
            continue
        if args.dry_run:
            meta, _body = parse_frontmatter(read_text(page))
            missing = [f for f in ("id", "version", "confidence", "source") if not meta.get(f)]
            if missing:
                print(f"Would update {page.relative_to(root)}: missing {', '.join(missing)}")
                total += 1
            continue
        if process_file(page, page_type):
            total += 1
            print(f"Updated: {page.relative_to(root)}")

    print(f"\nTotal: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
