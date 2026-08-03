#!/usr/bin/env python3

"""
MiGraph Script: create_page

Purpose:
- Create a new wiki page through the single canonical path and validate it
  before committing it to the wiki. Blocks on failure (removes the file and
  exits non-zero) so no unreliable page ever lands in the wiki.

Usage:
- Run as `python scripts/migraph create --root <wiki-root> --title "..." --type reference ...`
- Requires: --title, --type, --domain, --summary
- Optional: --category, --tags, --source, --connections, --content, --status, --confidence

Validation (blocking):
- Frontmatter against validators/schema.json (id, type, domain, tags, summary)
- Required fields (title, type, created, updated, source, tags, confidence, status)
- Required sections for the page type (from templates/pages/{type}.md)
- At least one `## Connections` markdown link that resolves to an existing page
- No placeholder text / weak summary
- No duplicate title or duplicate id in the wiki
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from utils import (
    PAGE_TYPE_TO_DIR,
    WIKI_DIRS,
    markdown_links,
    missing_required_fields,
    parse_frontmatter,
    read_text,
    slugify,
    today_str,
    write_text,
)

PLACEHOLDER_RE = re.compile(r"\bnone yet\b|\btodo\b|\bwhat should this source update\b|\bno relevant pages found\b", re.IGNORECASE)

# Minimal sections every page of a given type must contain (from templates/pages/ and wiki conventions).
# Each group is a list of case-insensitive alternatives: a group passes when ANY of its strings
# appears in a `## ` heading. This accepts both the plain template headings and the emoji-style
# headings used across the demo-wiki.
REQUIRED_SECTIONS: dict[str, list[list[str]]] = {
    "concept": [["definition"], ["explanation"], ["key insights"], ["usage context"]],
    "topic": [["summary"], ["related pages"]],
    "source": [["summary"], ["connections"]],
    "synthesis": [["summary"], ["related pages"]],
    "query": [["answer"], ["follow-ups"]],
    "decision": [["decision"], ["reasoning"]],
    "pattern": [["problem"], ["solution"], ["architecture"]],
    "runbook": [["context"], ["steps"], ["recovery"]],
    "architecture": [["overview"], ["components"], ["data flow"]],
    "guide": [["overview"], ["purpose"], ["usage"]],
    "reference": [["definition", "overview"], ["explanation", "quick reference"], ["references"]],
    "example": [["overview"], ["code"], ["explanation"]],
    "entity": [["summary"], ["evidence sources"]],
}

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "validators" / "schema.json"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "pages"


def load_schema() -> dict[str, object]:
    try:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"error: cannot read schema at {SCHEMA_PATH}: {exc}") from exc


def section_headings(body: str) -> list[str]:
    return [line[3:].strip() for line in body.splitlines() if line.strip().startswith("## ")]


def collect_existing_pages(root: Path) -> dict[Path, dict[str, object]]:
    existing: dict[Path, dict[str, object]] = {}
    for subdir in WIKI_DIRS:
        for page in sorted((root / "wiki" / subdir).glob("*.md")):
            meta, _body = parse_frontmatter(read_text(page))
            existing[page.resolve()] = meta
    return existing


def validate_page(root: Path, page: Path, meta: dict[str, object], body: str) -> list[str]:
    """Return a list of blocking validation errors. Empty list means the page is valid."""
    errors: list[str] = []
    schema = load_schema()
    schema_required = [str(field) for field in schema.get("required", [])]

    missing = missing_required_fields(meta)
    if missing:
        errors.append(f"missing required frontmatter: {', '.join(missing)}")
    missing_schema = [field for field in schema_required if field not in meta]
    if missing_schema:
        errors.append(f"missing schema-required fields: {', '.join(missing_schema)}")

    page_type = str(meta.get("type") or "")
    valid_types = PAGE_TYPE_TO_DIR
    if page_type not in valid_types:
        errors.append(f"invalid type '{page_type}' (must be one of: {', '.join(sorted(valid_types))})")
    else:
        expected_dir = valid_types[page_type]
        if page.parent.name != expected_dir:
            errors.append(f"type '{page_type}' must live in wiki/{expected_dir}/ (found {page.parent.name}/)")

    page_id = str(meta.get("id") or "")
    if not re.fullmatch(r"[a-z0-9-]+\.[a-z0-9-]+\.[a-z0-9-]+", page_id):
        errors.append(f"invalid id '{page_id}' (expected domain.type.slug)")

    domain = str(meta.get("domain") or "")
    if not re.fullmatch(r"[a-z0-9-]+", domain):
        errors.append(f"invalid domain '{domain}' (expected lowercase slug)")

    tags = meta.get("tags")
    if not isinstance(tags, list) or not tags:
        errors.append("tags must be a non-empty list")
    else:
        bad_tags = [t for t in tags if not re.fullmatch(r"[a-z0-9-]+", str(t))]
        if bad_tags:
            errors.append(f"invalid tags: {', '.join(map(str, bad_tags))} (expected lowercase slugs)")

    summary = str(meta.get("summary") or "")
    if len(summary.strip()) < 10:
        errors.append("summary must be at least 10 characters")

    if PLACEHOLDER_RE.search(body):
        errors.append("body contains placeholder text (todo/none yet/no relevant pages)")

    headings = section_headings(body)
    for group in REQUIRED_SECTIONS.get(page_type, []):
        if not any(any(alt in heading.casefold() for alt in group) for heading in headings):
            errors.append(f"missing required section: one of {group}")

    connections = [link for link in markdown_links(body) if not link.startswith(("http://", "https://", "mailto:", "#"))]
    if not connections:
        errors.append("page must have at least one '## Connections' markdown link to another wiki page")
    else:
        existing = collect_existing_pages(root)
        for link in connections:
            target = (page.parent / link).resolve()
            if target not in existing:
                errors.append(f"broken connection link '{link}' -> no wiki page at {target.relative_to(root)}")

    for other_page, other_meta in collect_existing_pages(root).items():
        if other_page == page.resolve():
            continue
        if str(other_meta.get("id")) == page_id and page_id:
            errors.append(f"duplicate id '{page_id}' already used by {other_page.relative_to(root)}")
        title = str(other_meta.get("title") or "")
        if title and title.casefold() == str(meta.get("title") or "").casefold():
            errors.append(f"duplicate title '{meta.get('title')}' already used by {other_page.relative_to(root)}")

    return errors


def build_page(
    *,
    root: Path,
    title: str,
    page_type: str,
    domain: str,
    category: str,
    summary: str,
    tags: list[str],
    source: str,
    connections: list[str],
    content: str,
    status: str,
    confidence: str,
    version: str,
) -> tuple[Path, str]:
    if page_type not in PAGE_TYPE_TO_DIR:
        raise SystemExit(f"error: invalid type '{page_type}'. Valid: {', '.join(sorted(PAGE_TYPE_TO_DIR))}")

    slug = slugify(title)
    page_id = f"{slugify(domain)}.{page_type}.{slug}"
    target_dir = root / "wiki" / PAGE_TYPE_TO_DIR[page_type]
    target = target_dir / f"{slug}.md"

    if target.exists():
        raise SystemExit(f"error: page already exists at {target.relative_to(root)}")

    if not content.strip():
        template = TEMPLATES_DIR / f"{page_type}.md"
        content = read_text(template) if template.exists() else f"# {title}\n"
        content = (
            content.replace("{{title}}", title)
            .replace("{{category}}", category)
            .replace("{{domain}}", slugify(domain))
            .replace("{{date}}", today_str())
            .replace("{{tag1}}", tags[0] if tags else "general")
            .replace("{{slug}}", slug)
            .replace("{{source}}", source)
            .replace("{{summary}}", summary.replace("\n", " ").strip())
        )

    connections_block = "\n".join(f"- [{Path(link).stem.title()}]({link})" for link in connections) if connections else ""

    lines = [
        "---",
        f"title: {title}",
        f"type: {page_type}",
        f"category: {category}",
        f"domain: {slugify(domain)}",
        f"created: {today_str()}",
        f"updated: {today_str()}",
        *(["tags:"] if tags else []),
        *[f"  - {tag}" for tag in tags],
        f"status: {status}",
        f"id: {page_id}",
        f'version: "{version}"',
        f"confidence: {confidence}",
    ]
    if not source.strip():
        raise SystemExit(f"error: --source is required for type '{page_type}'")
    lines.append(f"source: {source}")
    lines.extend(["summary: " + summary.replace("\n", " ").strip(), "---", "", f"# {title}"])

    body_parts = [part.strip() for part in content.split(f"# {title}", 1) if part.strip()]
    body = body_parts[-1] if body_parts else content.strip()

    # Normalize: ensure Connections section exists at the end if links were provided
    if connections_block and not re.search(r"^## Connections\b", body, re.MULTILINE):
        body = body.rstrip() + "\n\n## Connections\n\n" + connections_block + "\n"

    full = "\n".join(lines) + "\n\n" + body.rstrip() + "\n"
    return target, full


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new wiki page with blocking validation.")
    parser.add_argument("--root", default=".", help="Wiki root path")
    parser.add_argument("--title", required=True, help="Page title")
    parser.add_argument("--type", required=True, help=f"Page type (one of: {', '.join(sorted(PAGE_TYPE_TO_DIR))})")
    parser.add_argument("--domain", required=True, help="Knowledge domain slug")
    parser.add_argument("--category", default="general", help="Category slug")
    parser.add_argument("--summary", required=True, help="1-2 sentence summary")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--source", default="", help="Source documentation URL")
    parser.add_argument("--connections", default="", help="Comma-separated relative markdown links to wiki pages")
    parser.add_argument("--content", default="", help="Markdown body (defaults to the type template)")
    parser.add_argument("--status", default="active", help="Status (draft|active|deprecated|archived)")
    parser.add_argument("--confidence", default="high", help="Confidence (low|medium|high|verified)")
    parser.add_argument("--version", default="1.0.0", help="Version string")
    parser.add_argument("--no-rebuild", action="store_true", help="Skip graph/viewer/report rebuild after creation")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not (root / "wiki").is_dir():
        raise SystemExit(f"error: {root} does not look like a wiki root (missing wiki/ dir)")

    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
    connections = [link.strip() for link in args.connections.split(",") if link.strip()]

    target, content = build_page(
        root=root,
        title=args.title,
        page_type=args.type,
        domain=args.domain,
        category=args.category,
        summary=args.summary,
        tags=tags,
        source=args.source,
        connections=connections,
        content=args.content,
        status=args.status,
        confidence=args.confidence,
        version=args.version,
    )

    meta, body = parse_frontmatter(content)
    errors = validate_page(root, target, meta, body)
    if errors:
        print(f"error: page {target.relative_to(root)} FAILED validation:")
        for error in errors:
            print(f"  - {error}")
        print("No file was written.")
        return 1

    write_text(target, content)
    print(f"created {target.relative_to(root)} (validated OK)")

    log_path = root / "log.md"
    entry = f"- {today_str()} created [{args.title}](wiki/{target.relative_to(root / 'wiki')}) ({args.type})\n"
    write_text(log_path, read_text(log_path).rstrip() + "\n" + entry)

    if not args.no_rebuild:
        import subprocess
        import sys as _sys

        script_dir = Path(__file__).resolve().parent
        python = _sys.executable
        for script in ("build_graph.py", "build_viewer.py", "build_inbox.py", "graph_report.py"):
            subprocess.run([python, str(script_dir / script), "--root", str(root)], check=False)

    return 0


if __name__ == "__main__":
    sys.exit(main())
