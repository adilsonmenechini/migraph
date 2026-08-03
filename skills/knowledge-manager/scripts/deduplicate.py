#!/usr/bin/env python3
"""Knowledge Base Duplicate Checker - analyzes notes for similarity."""
import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from difflib import SequenceMatcher
    HAS_DIFFLIB = True
except ImportError:
    HAS_DIFFLIB = False

try:
    import nltk
    from nltk.corpus import stopwords
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False


@dataclass
class Note:
    """Represents a knowledge note."""
    path: str
    title: str
    category: str
    tags: list[str]
    content: str
    type: str
    
    @property
    def slug(self) -> str:
        return Path(self.path).stem


@dataclass
class SimilarityResult:
    """Similarity between two notes."""
    note_a: str
    note_b: str
    title_score: float
    content_score: float
    tag_score: float
    combined_score: float
    level: str
    
    def to_dict(self) -> dict:
        return {
            "note_a": self.note_a,
            "note_b": self.note_b,
            "title_score": round(self.title_score, 3),
            "content_score": round(self.content_score, 3),
            "tag_score": round(self.tag_score, 3),
            "combined_score": round(self.combined_score, 3),
            "level": self.level
        }


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def title_similarity(title_a: str, title_b: str) -> float:
    if not HAS_DIFFLIB:
        return 1.0 if title_a.lower() == title_b.lower() else 0.0
    norm_a = normalize_text(title_a)
    norm_b = normalize_text(title_b)
    if norm_a == norm_b:
        return 1.0
    return SequenceMatcher(None, norm_a, norm_b).ratio()


def content_similarity(content_a: str, content_b: str) -> float:
    if not content_a or not content_b:
        return 0.0
    words_a = set(normalize_text(content_a).split())
    words_b = set(normalize_text(content_b).split())
    if HAS_NLTK:
        try:
            sw = set(stopwords.words('english'))
            words_a -= sw
            words_b -= sw
        except:
            pass
    if not words_a or not words_b:
        return 0.0
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union) if union else 0.0


def tag_similarity(tags_a: list[str], tags_b: list[str]) -> float:
    if not tags_a or not tags_b:
        return 0.0
    set_a = set(t.lower() for t in tags_a)
    set_b = set(t.lower() for t in tags_b)
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def combined_similarity(title: float, content: float, tags: float) -> float:
    return (title * 0.4) + (content * 0.4) + (tags * 0.2)


def similarity_level(score: float) -> str:
    if score >= 0.7:
        return "HIGH"
    elif score >= 0.4:
        return "MEDIUM"
    return "LOW"


def extract_frontmatter(content: str) -> dict:
    frontmatter = {}
    pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(pattern, content, re.DOTALL)
    if match:
        fm_text = match.group(1)
        for line in fm_text.split('\n'):
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                if key in ('tags', 'aliases'):
                    items = re.findall(r'[-\[]?\s*["\']?([^"\']+)["\']?', value)
                    frontmatter[key] = items
                else:
                    frontmatter[key] = value
    return frontmatter


def extract_title(content: str, fallback_filename: str) -> str:
    fm = extract_frontmatter(content)
    if 'title' in fm:
        return fm['title']
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1)
    return fallback_filename


def scan_knowledge_base(base_path: str) -> list[Note]:
    notes = []
    base = Path(base_path)
    for md_file in base.rglob("*.md"):
        if md_file.name == "INDEX.md":
            continue
        if any(part.startswith('.') for part in md_file.parts):
            continue
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception:
            continue
        if len(content) < 100:
            continue
        fm = extract_frontmatter(content)
        title = extract_title(content, md_file.stem)
        category = fm.get('category', md_file.parent.name)
        tags = fm.get('tags', [])
        note_type = fm.get('type', 'unknown')
        content_clean = re.sub(r'^---.*?---', '', content, flags=re.DOTALL).strip()
        note = Note(
            path=str(md_file.relative_to(base)),
            title=title,
            category=category,
            tags=tags,
            content=content_clean,
            type=note_type
        )
        notes.append(note)
    return notes


def check_duplicates(notes: list[Note], threshold_high: float = 0.7, threshold_medium: float = 0.4) -> dict:
    high_sim = []
    med_sim = []
    low_sim = []
    for i, note_a in enumerate(notes):
        for note_b in notes[i+1:]:
            if note_a.category == note_b.category and note_a.type == note_b.type:
                continue
            title_score = title_similarity(note_a.title, note_b.title)
            content_score = content_similarity(note_a.content, note_b.content)
            tag_score = tag_similarity(note_a.tags, note_b.tags)
            combined = combined_similarity(title_score, content_score, tag_score)
            if combined < threshold_medium:
                continue
            level = similarity_level(combined)
            result = SimilarityResult(
                note_a=note_a.slug,
                note_b=note_b.slug,
                title_score=title_score,
                content_score=content_score,
                tag_score=tag_score,
                combined_score=combined,
                level=level
            )
            if level == "HIGH":
                high_sim.append(result)
            elif level == "MEDIUM":
                med_sim.append(result)
            else:
                low_sim.append(result)
    return {
        "high": [r.to_dict() for r in high_sim],
        "medium": [r.to_dict() for r in med_sim],
        "low": [r.to_dict() for r in low_sim]
    }


def generate_report(results: dict, notes: list[Note]) -> str:
    lines = ["# Duplicate Check Report\n"]
    total = len(results["high"]) + len(results["medium"]) + len(results["low"])
    lines.append("## Summary")
    lines.append(f"- Total pairs analyzed: {len(notes)} notes")
    lines.append(f"- Similar pairs found: {total}")
    lines.append(f"  - HIGH similarity: {len(results['high'])}")
    lines.append(f"  - MEDIUM similarity: {len(results['medium'])}")
    lines.append(f"  - LOW similarity: {len(results['low'])}")
    lines.append("")
    if results["high"]:
        lines.append("## HIGH Similarity (likely duplicates)")
        lines.append("")
        for item in results["high"]:
            lines.append(f"- [[{item['note_a']}]] ↔ [[{item['note_b']}]]")
            lines.append(f"  - Score: {item['combined_score']:.1%}")
        lines.append("")
    if results["medium"]:
        lines.append("## MEDIUM Similarity (related)")
        lines.append("")
        for item in results["medium"]:
            lines.append(f"- [[{item['note_a']}]] ↔ [[{item['note_b']}]]")
            lines.append(f"  - Score: {item['combined_score']:.1%}")
        lines.append("")
    if results["high"]:
        lines.append("## Recommendations")
        lines.append("")
        for item in results["high"]:
            lines.append(f"Consider merging [[{item['note_a']}]] and [[{item['note_b']}]]")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Check knowledge base for duplicates")
    parser.add_argument("base_path", help="Path to knowledge base")
    parser.add_argument("--output", "-o", help="Output JSON file")
    parser.add_argument("--report", "-r", help="Output report file")
    parser.add_argument("--threshold-high", "-tH", type=float, default=0.7)
    parser.add_argument("--threshold-medium", "-tM", type=float, default=0.4)
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()
    if not os.path.isdir(args.base_path):
        print(f"Error: {args.base_path} is not a directory", file=sys.stderr)
        sys.exit(1)
    notes = scan_knowledge_base(args.base_path)
    print(f"Found {len(notes)} notes")
    if len(notes) < 2:
        print("Not enough notes to compare")
        sys.exit(0)
    results = check_duplicates(notes, args.threshold_high, args.threshold_medium)
    if args.output:
        output = {"total_notes": len(notes), "results": results}
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
    if args.report or not args.json:
        report = generate_report(results, notes)
        if args.report:
            with open(args.report, 'w') as f:
                f.write(report)
        else:
            print("")
            print(report)
    sys.exit(1 if results["high"] else 0)


if __name__ == "__main__":
    main()