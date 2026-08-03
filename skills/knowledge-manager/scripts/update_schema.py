#!/usr/bin/env python3
import os
import re
from pathlib import Path

VERSION = '"1.0.0"'
CONFIDENCE = "high"
SOURCE = "docs"

def get_id(filepath: Path, category: str) -> str:
    slug = filepath.stem.replace(f"{category}-", "")
    return f"{category}.{slug}"

def update_frontmatter(content: str, filepath: Path, category: str) -> str:
    if "confidence:" in content or "source:" in content:
        return content
    
    lines = content.split("\n")
    new_lines = []
    inserted = False
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        if line.strip().startswith("updated:") and not inserted:
            slug_id = get_id(filepath, category)
            if "id:" not in "\n".join(lines[:20]):
                new_lines.append(f"id: {slug_id}")
            new_lines.append(f"version: {VERSION}")
            new_lines.append(f"confidence: {CONFIDENCE}")
            new_lines.append(f"source: {SOURCE}")
            inserted = True
    
    return "\n".join(new_lines)

def process_file(filepath: Path, category: str) -> bool:
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return False
    
    if not content.startswith("---"):
        return False
    
    updated = update_frontmatter(content, filepath, category)
    
    if updated != content:
        filepath.write_text(updated, encoding='utf-8')
        return True
    return False

def main():
    base = Path("examples/knowledge")
    categories = ["kubernetes", "terraform", "argocd", "deepagents", "langchain-ai"]
    total = 0
    
    for category in categories:
        cat_dir = base / category
        if not cat_dir.exists():
            continue
        
        for md_file in cat_dir.rglob("*.md"):
            if md_file.name == "INDEX.md":
                continue
            
            if process_file(md_file, category):
                total += 1
                print(f"Updated: {md_file.relative_to(base)}")
    
    print(f"\nTotal: {total}")

if __name__ == "__main__":
    main()