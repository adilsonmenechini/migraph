#!/usr/bin/env python3
from __future__ import annotations

"""
MiGraph Script: dedupe_pages

Purpose:
- Detect and report duplicate/similar pages across all wiki page types.
- Extends entity-merge-review (entity-only) to cover concept, topic, synthesis, source, pattern, runbook, architecture.
- Fixes the skill-kwonledge deduplicate.py bug: pairs with same category AND same type were skipped.

Usage:
- Run as `python scripts/migraph dedupe-pages --root <wiki-root>`.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from utils import (
    collect_wiki_pages,
    parse_frontmatter,
    read_text,
    write_text,
)

# ---------------------------------------------------------------------------
# Similarity helpers
# ---------------------------------------------------------------------------


def _normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _title_similarity(a: str, b: str) -> float:
    from difflib import SequenceMatcher

    na, nb = _normalize_text(a), _normalize_text(b)
    if na == nb:
        return 1.0
    return SequenceMatcher(None, na, nb).ratio()


def _content_similarity(a: str, b: str) -> float:
    wa = set(_normalize_text(a).split())
    wb = set(_normalize_text(b).split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def _tag_similarity(a: list[str], b: list[str]) -> float:
    sa = set(t.lower() for t in a)
    sb = set(t.lower() for t in b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def _combined_score(title: float, content: float, tags: float, semantic: float = 0.0) -> float:
    if semantic > 0:
        return title * 0.3 + content * 0.3 + tags * 0.15 + semantic * 0.25
    return title * 0.4 + content * 0.4 + tags * 0.2


def _level(score: float) -> str:
    if score >= 0.7:
        return "HIGH"
    if score >= 0.4:
        return "MEDIUM"
    return "LOW"


# ---------------------------------------------------------------------------
# Embedding cache
# ---------------------------------------------------------------------------


def _cache_path(root: Path) -> Path:
    return root / "state" / "page-embeddings.json"


def _load_cache(root: Path) -> dict[str, Any]:
    path = _cache_path(root)
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_cache(root: Path, cache: dict[str, Any]) -> None:
    path = _cache_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=2) + "\n", encoding="utf-8")


def _content_hash(text: str) -> str:
    normalized = _normalize_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Semantic similarity (optional, degrades gracefully)
# ---------------------------------------------------------------------------


def _semantic_scores(pages: list[dict[str, Any]], root: Path) -> dict[tuple[str, str], float]:
    """Compute cosine similarity for page content using embeddings.
    Returns dict mapping (page_a_path, page_b_path) -> score.
    Falls back to empty dict if embedding is not configured or fails."""
    try:
        from ai_config import embed_is_configured

        if not embed_is_configured():
            return {}
        from embed_client import cosine_similarity, embed_texts
    except Exception:
        return {}

    cache = _load_cache(root)
    texts_to_embed: list[tuple[int, str]] = []
    for i, page in enumerate(pages):
        h = _content_hash(page["content"])
        cache_key = f"{page['path']}:{h}"
        if cache_key not in cache:
            texts_to_embed.append((i, page["content"][:2000]))

    if texts_to_embed:
        try:
            embeddings = embed_texts([t for _, t in texts_to_embed])
            for (idx, _), emb in zip(texts_to_embed, embeddings):
                h = _content_hash(pages[idx]["content"])
                cache_key = f"{pages[idx]['path']}:{h}"
                cache[cache_key] = emb
            _save_cache(root, cache)
        except Exception as exc:
            print(f"Warning: embedding batch failed ({exc}). Using lexica scores only.", file=sys.stderr)
            return {}

    scores: dict[tuple[str, str], float] = {}
    for i, a in enumerate(pages):
        ha = _content_hash(a["content"])
        ca = cache.get(f"{a['path']}:{ha}")
        if not ca:
            continue
        for j in range(i + 1, len(pages)):
            b = pages[j]
            hb = _content_hash(b["content"])
            cb = cache.get(f"{b['path']}:{hb}")
            if not cb:
                continue
            scores[(a["path"], b["path"])] = cosine_similarity(ca, cb)

    return scores


# ---------------------------------------------------------------------------
# Main logic
# ---------------------------------------------------------------------------


def _load_pages(root: Path) -> list[dict[str, Any]]:
    pages: list[dict[str, Any]] = []
    for md_path in collect_wiki_pages(root):
        raw = read_text(md_path)
        if len(raw) < 50:
            continue
        meta, body = parse_frontmatter(raw)
        rel = md_path.relative_to(root).as_posix()
        pages.append({
            "path": rel,
            "title": str(meta.get("title", "") or md_path.stem),
            "type": str(meta.get("type", "") or "page"),
            "tags": [str(t) for t in (meta.get("tags") or []) if str(t).strip()],
            "content": body,
        })
    return pages


def find_duplicates(root: Path, threshold_high: float = 0.7, threshold_medium: float = 0.4) -> dict[str, Any]:
    pages = _load_pages(root)
    if len(pages) < 2:
        return {"total_pages": len(pages), "pairs": []}

    semantic = _semantic_scores(pages, root)

    pairs: list[dict[str, Any]] = []
    for i, a in enumerate(pages):
        for j in range(i + 1, len(pages)):
            b = pages[j]
            ts = _title_similarity(a["title"], b["title"])
            cs = _content_similarity(a["content"], b["content"])
            tg = _tag_similarity(a["tags"], b["tags"])
            sem = semantic.get((a["path"], b["path"]), 0.0)
            combined = _combined_score(ts, cs, tg, sem)
            if combined < threshold_medium:
                continue
            pairs.append({
                "note_a": a["path"],
                "note_b": b["path"],
                "title_score": round(ts, 3),
                "content_score": round(cs, 3),
                "tag_score": round(tg, 3),
                "semantic_score": round(sem, 3),
                "combined_score": round(combined, 3),
                "level": _level(combined),
            })

    pairs.sort(key=lambda p: p["combined_score"], reverse=True)
    return {"total_pages": len(pages), "pairs": pairs}


def _generate_report(data: dict[str, Any]) -> str:
    lines = ["# Page Dedup Report\n"]
    total = data["total_pages"]
    pairs = data["pairs"]
    high = [p for p in pairs if p["level"] == "HIGH"]
    medium = [p for p in pairs if p["level"] == "MEDIUM"]

    lines.append("## Summary")
    lines.append(f"- Total pages analyzed: {total}")
    lines.append(f"- Similar pairs found: {len(pairs)}")
    lines.append(f"  - HIGH similarity: {len(high)}")
    lines.append(f"  - MEDIUM similarity: {len(medium)}")
    lines.append("")

    if high:
        lines.append("## HIGH Similarity (likely duplicates)")
        for p in high:
            lines.append(f"- [[{Path(p['note_a']).stem}]] <-> [[{Path(p['note_b']).stem}]]")
            lines.append(f"  - Combined: {p['combined_score']:.1%} (title: {p['title_score']:.1%}, content: {p['content_score']:.1%}, tags: {p['tag_score']:.1%}, semantic: {p['semantic_score']:.1%})")
        lines.append("")

    if medium:
        lines.append("## MEDIUM Similarity (related)")
        for p in medium:
            lines.append(f"- [[{Path(p['note_a']).stem}]] <-> [[{Path(p['note_b']).stem}]]")
            lines.append(f"  - Combined: {p['combined_score']:.1%}")
        lines.append("")

    if high:
        lines.append("## Recommendations")
        for p in high:
            lines.append(f"- Consider merging [[{Path(p['note_a']).stem}]] and [[{Path(p['note_b']).stem}]]")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect duplicate/similar pages in the wiki")
    parser.add_argument("--root", required=True, help="Path to wiki root")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--report", help="Output markdown report file path")
    parser.add_argument("--threshold-high", type=float, default=0.7)
    parser.add_argument("--threshold-medium", type=float, default=0.4)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Wiki root not found: {root}")

    data = find_duplicates(root, args.threshold_high, args.threshold_medium)
    report = _generate_report(data)

    print(f"Analyzed {data['total_pages']} pages, found {len(data['pairs'])} similar pairs.")
    for p in data["pairs"]:
        if p["level"] == "HIGH":
            print(f"  HIGH: {p['note_a']} <-> {p['note_b']} ({p['combined_score']:.1%})")

    if args.output:
        Path(args.output).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    if args.report:
        write_text(Path(args.report), report)
    else:
        print()
        print(report)

    high_count = sum(1 for p in data["pairs"] if p["level"] == "HIGH")
    raise SystemExit(1 if high_count else 0)


if __name__ == "__main__":
    main()
