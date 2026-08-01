#!/usr/bin/env python3
"""
MiGraph Script: migrate_skill_kwonledge

Purpose:
- One-shot migration of skill-kwonledge content into a MiGraph vault.
- Maps: category -> tags, types -> MiGraph types, related -> text + review note.

Usage:
- python scripts/migrate_skill_kwonledge.py \\
    --source /path/to/skill-kwonledge/examples/knowledge \\
    --target /path/to/migraph-vault
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from utils import parse_frontmatter, read_text, write_text, today_str

# --- Type mapping ---

TYPE_MAP = {
    "concept": "concept",
    "guide": "source",
    "reference": "source",
    "example": "source",
    "pattern": "pattern",
    "runbook": "runbook",
    "architecture": "architecture",
}


def _slugify(text: str) -> str:
    slug = text.lower().replace(" ", "-").replace("_", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug.strip("-") or "untitled"


def _resolve_type(raw_type: str) -> str:
    return TYPE_MAP.get(raw_type, "topic")


def _map_related(related: list[str]) -> str:
    """Convert related wikilinks to text block with review note."""
    if not related:
        return ""
    lines = ["", "**Related (review manually):**"]
    for item in related:
        if not isinstance(item, str):
            continue
        clean = item.strip().strip("[").strip("]").strip()
        lines.append(f"- {clean}")
    return "\n".join(lines)


def _extract_category(content: str) -> str:
    """Try to infer category from file path (e.g., .../IaC/terraform/... -> IaC)."""
    if not isinstance(content, str):
        return ""
    return ""


def migrate(source_dir: Path, target_dir: Path, dry_run: bool = False) -> dict:
    report = {
        "total": 0,
        "migrated": 0,
        "skipped_empty": 0,
        "skipped_index": 0,
        "type_mapped": 0,
        "related_unresolved": 0,
        "pages": [],
    }

    source_root = Path(source_dir).resolve()
    target_wiki = Path(target_dir).resolve()

    if not source_root.exists():
        raise SystemExit(f"Source directory not found: {source_root}")

    for md_path in sorted(source_root.rglob("*.md")):
        if md_path.name == "INDEX.md":
            report["skipped_index"] += 1
            continue

        raw = read_text(md_path)
        if len(raw) < 50:
            report["skipped_empty"] += 1
            continue

        report["total"] += 1
        meta, body = parse_frontmatter(raw)

        title = str(meta.get("title", "") or md_path.stem)
        raw_type = str(meta.get("type", "") or "concept")
        mapped_type = _resolve_type(raw_type)
        if mapped_type != raw_type:
            report["type_mapped"] += 1

        category = str(meta.get("category", "") or "")
        tags = [str(t) for t in (meta.get("tags") or []) if str(t).strip()]
        if category and category.lower() not in [str(t).lower() for t in tags]:
            tags.insert(0, category)

        related = [str(r) for r in (meta.get("related") or []) if str(r).strip()]
        if related:
            report["related_unresolved"] += 1

        slug = _slugify(title)
        dest_dir = target_wiki / "wiki" / _type_to_dir(mapped_type)
        target_path = dest_dir / f"{slug}.md"

        sources = [str(s) for s in (meta.get("sources") or []) if str(s).strip()]
        source_url = str(meta.get("source", "") or "").strip()
        if source_url and source_url not in sources:
            sources.append(source_url)

        fm_lines = [
            "---",
            f'title: "{title}"',
            f"type: {mapped_type}",
            f"created: {today_str()}",
            f"updated: {today_str()}",
            f'summary: "{_first_line(body)}"',
            "sources:" + ("".join(f'\n  - "{s}"' for s in sources) if sources else " []"),
            "tags:" + ("".join(f'\n  - "{t}"' for t in tags) if tags else " []"),
            "confidence: medium",
            "status: active",
            "---",
        ]

        related_block = _map_related(related)
        page_content = "\n".join(fm_lines) + "\n\n" + body.strip() + "\n" + related_block + "\n"

        if not dry_run:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            write_text(target_path, page_content)

        report["migrated"] += 1
        report["pages"].append({
            "source": md_path.relative_to(source_root).as_posix(),
            "target": target_path.relative_to(target_wiki).as_posix(),
            "type": mapped_type,
            "related_unresolved": len(related),
        })

    return report


def _type_to_dir(page_type: str) -> str:
    mapping = {
        "concept": "concepts",
        "topic": "topics",
        "source": "sources",
        "synthesis": "syntheses",
        "query": "queries",
        "decision": "decisions",
        "pattern": "patterns",
        "runbook": "runbooks",
        "architecture": "architectures",
    }
    return mapping.get(page_type, "topics")


def _first_line(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("```"):
            return stripped[:120]
    return "(no summary)"


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate skill-kwonledge content into MiGraph vault")
    parser.add_argument("--source", required=True, help="Path to skill-kwonledge examples/knowledge")
    parser.add_argument("--target", required=True, help="Path to target MiGraph vault root")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be migrated without writing")
    args = parser.parse_args()

    report = migrate(Path(args.source), Path(args.target), args.dry_run)

    print(f"\nMigration {'preview' if args.dry_run else 'complete'}:")
    print(f"  Total files found: {report['total']}")
    print(f"  Migrated: {report['migrated']}")
    print(f"  Skipped (empty): {report['skipped_empty']}")
    print(f"  Skipped (INDEX.md): {report['skipped_index']}")
    print(f"  Type mapped: {report['type_mapped']}")
    print(f"  Related unresolved: {report['related_unresolved']}")
    print()
    for page in report["pages"]:
        resolved = "review" if page["related_unresolved"] else "ok"
        print(f"  [{page['type']}] {page['source']} -> {page['target']} ({resolved})")


if __name__ == "__main__":
    main()
