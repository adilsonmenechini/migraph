#!/usr/bin/env python3
"""
MiGraph Script: digest

Purpose:
- Create a synthesis page that combines multiple source pages into one reusable artifact.

Usage:
- Prefer `python scripts/migraph digest ...`.
- Run `python scripts/<script> --help` for direct CLI details when the file exposes its own arguments.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from ai_config import llm_is_configured, resolve_llm_config
from crystallize import first_meaningful_line, write_page
from llm_client import llm_digest
from utils import (
    file_uri,
    find_repo_root,
    normalize_repo_path,
    parse_frontmatter,
    read_text,
    refresh_output_home_if_present,
)


def ordered_unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        clean = " ".join(item.split()).strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        result.append(clean)
    return result


def extract_title(body: str, fallback: str) -> str:
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("# "):
            return line[2:].strip() or fallback
    return fallback


def source_page_companion(root: Path, page_path: Path) -> Path | None:
    if page_path.parent.name != "sources":
        return None
    text = read_text(page_path)
    meta, _body = parse_frontmatter(text)
    source_values = meta.get("sources", [])
    if not isinstance(source_values, list) or not source_values:
        return None
    raw_path = Path(str(source_values[0]))
    if len(raw_path.parts) < 3 or raw_path.parts[0] != "raw":
        return None
    normalized_path = root / Path("normalized", *raw_path.parts[1:]).with_suffix(".md")
    if normalized_path.exists():
        return normalized_path
    return None


def resolve_input_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    normalized = normalize_repo_path(root, value)
    return root / normalized


def collect_related_paths(root: Path, body: str, page_path: Path) -> list[str]:
    related: list[str] = []
    for match in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
        if match.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = (page_path.parent / match).resolve()
        try:
            related.append(target.relative_to(root.resolve()).as_posix())
        except ValueError:
            continue
    return ordered_unique([item for item in related if item.startswith("wiki/") and item.endswith(".md")])


def source_record(root: Path, raw_path: Path, summary_kind: str = "synthesis") -> dict[str, object]:
    text = read_text(raw_path)
    if not text:
        raise SystemExit(f"Cannot read source content: {raw_path}")
    title = raw_path.stem
    source_paths: list[str] = []
    related_paths: list[str] = []

    if raw_path.suffix.lower() == ".md" and "wiki" in raw_path.parts:
        meta, body = parse_frontmatter(text)
        title = str(meta.get("title") or raw_path.stem)
        source_values = meta.get("sources", [])
        if isinstance(source_values, list):
            source_paths = [normalize_repo_path(root, str(item)) for item in source_values]
        related_paths = collect_related_paths(root, body, raw_path)
    else:
        body = text
        title = extract_title(body, raw_path.stem)
        if raw_path.is_relative_to(root):
            source_paths = [raw_path.relative_to(root).as_posix()]

    companion = source_page_companion(root, raw_path)
    companion_text = read_text(companion) if companion else ""
    primary_body = companion_text or body

    return {
        "path": raw_path,
        "title": title,
        "source_paths": ordered_unique(source_paths),
        "related_paths": ordered_unique(related_paths),
        "source_data": {"title": title, "body": primary_body},
    }


_HEURISTIC_BLOCKED_SECTIONS = {
    "Connections",
    "Related Pages",
    "Open Questions",
    "Consulted Pages",
    "Sources",
    "Raw Source",
    "Extracted Markdown",
    "Extracted Excerpt",
}
_HEURISTIC_META_PREFIXES = ("Source:", "Author:", "Published:", "Original link:")
_HEURISTIC_LOW_VALUE_SUMMARY_PATTERNS = (
    "the following is",
    "click to view",
    "original link",
)
_HEURISTIC_TENSION_HINTS = (
    "but",
    "however",
    "yet",
    "need",
    "risk",
    "problem",
    "challenge",
    "difficult",
    "conflict",
    "trade-off",
    "boundary",
    "verify",
    "confirm",
)
_HEURISTIC_LOW_VALUE_LINE_HINTS = (
    "this report aims to answer",
    "research question",
    "deputy director",
    "senior expert",
    "date:",
    "date:",
    "page ",
)
_HEURISTIC_DEFINITION_HINTS = ("is defined as", "essentially", "refers to", "means", "can be summarized as")
_HEURISTIC_DECISION_HINTS = (
    "is not suitable",
    "should",
    "should adopt",
    "recommend",
    "recommended",
    "in other words",
    "the key is",
    "core judgment",
)
_HEURISTIC_STRATEGY_HINTS = (
    "mitigation strategy",
    "primary evaluation criterion",
    "product management mindset",
    "developer experience (DevEx)",
    "developer experience(DevEx)",
)
_HEURISTIC_ROLE_HINTS = ("typical roles include", "responsibilities include", "roles include")
_HEURISTIC_SYNTHESIS_HINTS = (
    "this means",
    "therefore",
    "in other words",
    "core judgment",
    "indicates",
    "first is a",
    "essentially",
)
_HEURISTIC_ORGANIZATION_HINTS = (
    "team",
    "organization",
    "platform",
    "collaboration",
    "operating mechanism",
    "delivery system",
)
_HEURISTIC_CONTINUATION_ENDINGS = (
    "and",
    "but",
    "or",
    "with",
    "that",
    "which",
    "while",
    "when",
    "if",
    "because",
    "the",
    "of",
    "in",
    "on",
    "at",
    "to",
    "by",
    "for",
    "from",
    "than",
    "then",
    "so",
    "yet",
    "not",
    "is",
    "are",
    "was",
    "were",
    "be",
    "has",
    "have",
    "will",
    "would",
    "can",
    "could",
    "should",
    "may",
    "might",
    "must",
)


def _heuristic_normalize_text(text: str) -> str:
    return " ".join(text.replace("\r\n", "\n").replace("\r", "\n").split())


def _heuristic_plain_text(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[\[\d+\]\]\([^)]+\)", "", text)
    text = re.sub(r"\[\[\d+\]\]\(?", "", text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"[*_`~#>]+", " ", text)
    return _heuristic_normalize_text(text).strip(" -|,;")


def _heuristic_short_text(text: str, limit: int = 180) -> str:
    value = _heuristic_plain_text(text)
    if len(value) <= limit:
        return value
    window = value[: limit - 1]
    cut = max(window.rfind("."), window.rfind(";"), window.rfind(" "))
    if cut >= max(20, limit // 3):
        window = window[:cut]
    return window.rstrip() + "..."


def _heuristic_looks_like_placeholder(text: str) -> bool:
    compact = _heuristic_normalize_text(text).lower()
    if not compact:
        return True
    return compact in {"none yet", "todo", "- todo", "(no summary)"}


def _heuristic_cleaned_line(raw: str) -> str:
    return raw.strip().lstrip("-* ").strip()


def _heuristic_is_metadata_line(text: str) -> bool:
    return _heuristic_cleaned_line(text).startswith(_HEURISTIC_META_PREFIXES)


def _heuristic_is_link_only(text: str) -> bool:
    clean = _heuristic_cleaned_line(text)
    if clean.startswith(("http://", "https://", "<http://", "<https://")):
        return True
    return bool(re.fullmatch(r"\d+\.\s*https?://\S+", clean))


def _heuristic_low_value_summary(text: str) -> bool:
    clean = _heuristic_plain_text(text)
    if not clean:
        return True
    if _heuristic_is_metadata_line(clean) or _heuristic_is_link_only(clean):
        return True
    lowered = clean.lower()
    return any(clean.startswith(prefix) for prefix in _HEURISTIC_LOW_VALUE_SUMMARY_PATTERNS) or any(
        hint in lowered for hint in _HEURISTIC_LOW_VALUE_LINE_HINTS
    )


def _heuristic_split_sentences(text: str) -> list[str]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    merged_lines: list[str] = []
    buffer = ""
    for raw in normalized.split("\n"):
        line = raw.strip()
        if not line:
            continue
        if not buffer:
            buffer = line
            continue
        if buffer.endswith((".", "!", "?", ";", ":")):
            merged_lines.append(buffer.strip())
            buffer = line
            continue
        if re.match(r"^(?:[-*]|\d+[.)])\s*", line):
            merged_lines.append(buffer.strip())
            buffer = line
            continue
        buffer = f"{buffer} {line}"
    if buffer:
        merged_lines.append(buffer.strip())

    parts: list[str] = []
    for chunk in merged_lines:
        parts.extend(re.split(r"(?<=[.!?])\s+", chunk))
    return [part.strip(" -") for part in parts if part.strip(" -")]


def _heuristic_looks_incomplete_sentence(text: str) -> bool:
    clean = _heuristic_plain_text(text)
    if not clean:
        return True
    if clean.endswith((".", "!", "?")):
        return False
    if clean.endswith(("...", ";", ":")):
        return True
    if clean.split()[-1] in _HEURISTIC_CONTINUATION_ENDINGS:
        return True
    return len(clean) < 30


def _heuristic_is_low_value_sentence(text: str) -> bool:
    clean = _heuristic_plain_text(text)
    lowered = clean.lower()
    if len(clean) < 12:
        return True
    if _heuristic_looks_like_placeholder(clean):
        return True
    if _heuristic_is_metadata_line(clean) or _heuristic_is_link_only(clean):
        return True
    if any(hint in lowered for hint in _HEURISTIC_LOW_VALUE_LINE_HINTS):
        return True
    return bool(clean.endswith(":"))


def _heuristic_sentence_priority(text: str) -> int:
    clean = _heuristic_plain_text(text)
    score = 0
    if any(hint in clean for hint in _HEURISTIC_DEFINITION_HINTS):
        score += 8
    if any(hint in clean for hint in _HEURISTIC_DECISION_HINTS):
        score += 7
    if "is defined as" in clean:
        score += 8
    if "is not suitable" in clean or "should adopt" in clean or "recommended" in clean:
        score += 10
    if "essentially" in clean:
        score += 4
    if "refers to" in clean:
        score += 2
    if len(clean) >= 30:
        score += 2
    if len(clean) >= 80:
        score += 2
    if len(clean) > 200:
        score -= 2
    if "?" in clean:
        score -= 6
    return score


def _heuristic_summary_candidate_score(text: str) -> int:
    clean = _heuristic_plain_text(text)
    score = _heuristic_sentence_priority(clean)
    if len(clean) < 24:
        score -= 6
    elif len(clean) <= 140:
        score += 4
    elif len(clean) <= 220:
        score += 1
    else:
        score -= 4
    has_terminal_punctuation = clean.endswith((".", "!", "?"))
    if has_terminal_punctuation:
        score += 4
    else:
        score -= 14
    if clean.endswith(("...", ";", ":")):
        score -= 6
    if clean and clean.split()[-1] in _HEURISTIC_CONTINUATION_ENDINGS:
        score -= 30
    if re.search(r"\d+$", clean):
        score -= 4
    return score


def _heuristic_kind_summary_score(text: str, kind: str, title: str = "") -> int:
    clean = _heuristic_plain_text(text)
    score = _heuristic_summary_candidate_score(clean)
    normalized_kind = kind.strip().lower()
    title_clean = _heuristic_plain_text(title)

    if normalized_kind == "concept":
        if any(hint in clean for hint in _HEURISTIC_DEFINITION_HINTS):
            score += 18
        if "first is a" in clean or "can be summarized in one sentence" in clean:
            score += 10
        if "the key is not" in clean or "around executable specs" in clean:
            score += 10
        if "software delivery team" in clean or "its key is not" in clean:
            score += 12
        if title_clean and (clean.startswith(title_clean) or clean.startswith(f"{title_clean} (")):
            score += 14
        if (
            title_clean
            and title_clean in clean
            and any(hint in clean for hint in ("is defined as", "essentially", "refers to", "means", "first is a"))
        ):
            score += 8
        if clean.startswith("this report does not treat") or "as parallel independent concepts" in clean:
            score -= 24
        if "rather than a parallel methodology" in clean:
            score -= 10
        if "this report" in clean and ("systematic argument" in clean or "emerged" in clean):
            score -= 16
        if any(hint in clean for hint in _HEURISTIC_STRATEGY_HINTS):
            score -= 20
        if any(hint in clean for hint in _HEURISTIC_ROLE_HINTS):
            score -= 10
        if "the team should" in clean or "recommend" in clean:
            score -= 8
    elif normalized_kind == "decision":
        if any(hint in clean for hint in _HEURISTIC_DECISION_HINTS):
            score += 18
        if "is not suitable" in clean or "should" in clean or "should adopt" in clean or "recommended" in clean:
            score += 14
        if any(hint in clean for hint in _HEURISTIC_DEFINITION_HINTS):
            score -= 6
        if (
            clean.startswith(("mitigation strategy", "recommended"))
            and "is not suitable" not in clean
            and "should" not in clean
        ):
            score -= 12
    else:
        if any(hint in clean for hint in _HEURISTIC_SYNTHESIS_HINTS):
            score += 12
        if any(hint in clean for hint in _HEURISTIC_DEFINITION_HINTS):
            score += 8
        if any(hint in clean for hint in _HEURISTIC_DECISION_HINTS):
            score += 8
        if "first is an organizational pattern" in clean or "organizational pattern rather than a tool list" in clean:
            score += 16
        if "the key is not" in clean and "whether the team" in clean:
            score += 10
        if "cannot be understood only as" in clean or "the real difficulty is not" in clean:
            score += 12
        if clean.startswith("this report does not treat") or "as parallel independent concepts" in clean:
            score -= 20
        if "rather than a parallel methodology" in clean:
            score -= 10
        if any(hint in clean for hint in _HEURISTIC_STRATEGY_HINTS):
            score -= 18
        if any(hint in clean for hint in _HEURISTIC_ROLE_HINTS):
            score -= 10
        if any(hint in clean for hint in _HEURISTIC_ORGANIZATION_HINTS):
            score += 4
        if "the team should" in clean or "recommended" in clean:
            score -= 8
        if len(clean) > 180:
            score -= 12
        if len(clean) > 240:
            score -= 10
        if clean.count(".") >= 3:
            score -= 6

    if clean.count(";") >= 2:
        score -= 4
    return score


def _heuristic_summary_sentence_candidates(text: str, summary_kind: str, title: str, limit: int = 12) -> list[str]:
    candidates: list[tuple[int, int, str]] = []
    for index, part in enumerate(_heuristic_split_sentences(text)):
        clean = _heuristic_plain_text(part).strip(" -")
        if clean.startswith("#") or _heuristic_is_low_value_sentence(clean):
            continue
        candidates.append((_heuristic_kind_summary_score(clean, summary_kind, title), index, clean))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [item[2] for item in candidates[:limit]]


def _heuristic_choose_best_summary(summary: str, primary_body: str, title: str, summary_kind: str = "synthesis") -> str:
    candidates: list[str] = []
    summary_clean = _heuristic_plain_text(summary)
    if summary_clean and not _heuristic_low_value_summary(summary_clean):
        candidates.append(summary_clean)
    candidates.extend(_heuristic_summary_sentence_candidates(primary_body, summary_kind, title, limit=12))
    candidates = ordered_unique(candidates)
    if not candidates:
        return title
    scored = sorted(
        (
            (_heuristic_kind_summary_score(candidate, summary_kind, title), index, candidate)
            for index, candidate in enumerate(candidates)
        ),
        key=lambda item: (-item[0], item[1], item[2]),
    )
    return scored[0][2]


def _heuristic_extract_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "Overview"
    sections[current] = []
    for raw in body.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped[3:].strip() or "Overview"
            sections.setdefault(current, [])
            continue
        if stripped.startswith("### "):
            current = stripped[4:].strip() or current
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def _heuristic_clean_content_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line in {"---", "***"}:
            continue
        if line.startswith("#"):
            continue
        if line.startswith("![]("):
            continue
        if _heuristic_is_metadata_line(line):
            continue
        if line.startswith(("Published:", "Updated:")):
            continue
        if _heuristic_is_link_only(line):
            continue
        lines.append(line)
    return lines


def _heuristic_meaningful_sentences(text: str, limit: int = 8) -> list[str]:
    candidates: list[tuple[int, int, str]] = []
    for index, part in enumerate(_heuristic_split_sentences(text)):
        clean = _heuristic_plain_text(part).strip(" -")
        if clean.startswith("#") or _heuristic_is_low_value_sentence(clean):
            continue
        if _heuristic_looks_incomplete_sentence(clean):
            continue
        candidates.append((_heuristic_sentence_priority(clean), index, clean))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    return [item[2] for item in candidates[:limit]]


def _heuristic_likely_tension(text: str) -> bool:
    clean = _heuristic_plain_text(text)
    if len(clean) < 16:
        return False
    return any(hint in clean for hint in _HEURISTIC_TENSION_HINTS)


def _heuristic_source_record(root: Path, raw_path: Path, summary_kind: str = "synthesis") -> dict[str, object]:
    text = read_text(raw_path)
    if not text:
        raise SystemExit(f"Cannot read source content: {raw_path}")
    record_type = "normalized" if "normalized" in raw_path.parts else "page"
    title = raw_path.stem
    summary = ""
    source_paths: list[str] = []
    related_paths: list[str] = []

    if raw_path.suffix.lower() == ".md" and "wiki" in raw_path.parts:
        meta, body = parse_frontmatter(text)
        title = str(meta.get("title") or raw_path.stem)
        summary = str(meta.get("summary") or "").strip()
        source_values = meta.get("sources", [])
        if isinstance(source_values, list):
            source_paths = [normalize_repo_path(root, str(item)) for item in source_values]
        related_paths = collect_related_paths(root, body, raw_path)
    else:
        body = text
        title = extract_title(body, raw_path.stem)
        summary_candidates = _heuristic_clean_content_lines(body)
        summary = _heuristic_short_text(summary_candidates[0]) if summary_candidates else ""
        if raw_path.is_relative_to(root):
            source_paths = [raw_path.relative_to(root).as_posix()]

    companion = source_page_companion(root, raw_path) if record_type == "page" else None
    companion_text = read_text(companion) if companion else ""
    primary_body = companion_text or body
    companion_summary = (_heuristic_meaningful_sentences(primary_body, limit=1) or [""])[0]
    sections = _heuristic_extract_sections(primary_body)
    key_texts: list[tuple[int, str]] = []
    tension_texts: list[str] = []

    for section_name, section_body in sections.items():
        if section_name in _HEURISTIC_BLOCKED_SECTIONS:
            continue
        for line in _heuristic_meaningful_sentences(section_body, limit=6):
            clean = _heuristic_cleaned_line(line)
            if _heuristic_is_low_value_sentence(clean):
                continue
            if section_name in {"Open Questions", "Tensions", "Follow-ups"}:
                tension_texts.append(clean)
            else:
                key_texts.append((_heuristic_sentence_priority(clean), clean))

    key_sentences = _heuristic_meaningful_sentences(primary_body, limit=10)
    if not tension_texts:
        tension_texts.extend(
            [
                item
                for item in _heuristic_meaningful_sentences(primary_body, limit=12)
                if _heuristic_likely_tension(item)
            ][:3]
        )
    summary = _heuristic_short_text(
        _heuristic_choose_best_summary(summary or companion_summary, primary_body, title, summary_kind)
    )

    return {
        "path": raw_path,
        "title": title,
        "summary": summary,
        "type": record_type,
        "source_paths": ordered_unique(source_paths),
        "related_paths": ordered_unique(related_paths),
        "findings": ordered_unique(
            [item for _score, item in sorted(key_texts, key=lambda value: (-value[0], value[1]))] + key_sentences
        ),
        "tensions": ordered_unique(tension_texts),
    }


def _heuristic_auto_summary(records: list[dict[str, object]], fallback: str, summary_kind: str = "synthesis") -> str:
    parts = [str(record["summary"]).strip() for record in records if str(record["summary"]).strip()]
    parts = ordered_unique(parts)
    if not parts:
        return fallback
    if len(parts) == 1:
        return _heuristic_short_text(parts[0], limit=220)
    ranked = sorted(
        (
            (_heuristic_kind_summary_score(part, summary_kind, fallback), index, part)
            for index, part in enumerate(parts)
        ),
        key=lambda item: (-item[0], item[1], item[2]),
    )
    lead = ranked[0][2]
    if summary_kind == "synthesis":
        preferred = next(
            (
                part
                for score, _index, part in ranked
                if len(part) <= 180
                and part.endswith((".", "!", "?"))
                and (
                    any(hint in part for hint in _HEURISTIC_DECISION_HINTS)
                    or "first is an organizational pattern" in part
                    or "the key is not" in part
                    or "cannot be understood only as" in part
                    or "software delivery team" in part
                )
                and score >= ranked[0][0] - 6
            ),
            "",
        )
        if preferred:
            lead = preferred
    support = next((part for _score, _index, part in ranked[1:] if part != lead), "")
    if support:
        return _heuristic_short_text(
            f"{lead} This judgment is also supported by other sources, indicating cross-material consistency.",
            limit=220,
        )
    return _heuristic_short_text(lead, limit=220)


def _heuristic_auto_findings(records: list[dict[str, object]], limit: int = 6) -> list[str]:
    findings: list[str] = []
    for record in records:
        title = str(record["title"])
        for item in list(record["findings"])[:3]:
            item = _heuristic_short_text(item, limit=150)
            prefix = f"{title}: "
            findings.append(prefix + item if not item.startswith(title) else item)
            if len(findings) >= limit:
                return ordered_unique(findings)
    return ordered_unique(findings)


def _heuristic_auto_tensions(records: list[dict[str, object]], limit: int = 4) -> list[str]:
    tensions: list[str] = []
    for record in records:
        title = str(record["title"])
        for item in list(record["tensions"])[:2]:
            item = _heuristic_short_text(item, limit=150)
            tensions.append(f"{title}: {item}")
            if len(tensions) >= limit:
                return ordered_unique(tensions)
        if not list(record["tensions"]):
            hinted = [item for item in list(record["findings"]) if _heuristic_likely_tension(item)][:2]
            for item in hinted:
                item = _heuristic_short_text(item, limit=150)
                tensions.append(f"{title}: {item}")
                if len(tensions) >= limit:
                    return ordered_unique(tensions)
    summaries = ordered_unique([str(record["summary"]).strip() for record in records if str(record["summary"]).strip()])
    if len(summaries) > 1:
        tensions.append(
            "Different sources emphasize different points; human review is needed to confirm which conclusions should become stable knowledge."
        )
    if not tensions and len(records) >= 2:
        tensions.append(
            "The current digest mainly summarizes information; whether there are conflicts, staleness, or evidence gaps still requires further review."
        )
    if not tensions:
        tensions.append(
            "Current inputs are limited; no clear conflicts yet, but more material and cross-validation are still needed."
        )
    return ordered_unique(tensions[:limit])


def _heuristic_auto_content(summary: str, findings: list[str], tensions: list[str]) -> str:
    lines = [summary.strip()]
    if findings:
        lines.extend(["", "Findings:"])
        lines.extend(f"- {item}" for item in findings[:4])
    if tensions:
        lines.extend(["", "Tensions:"])
        lines.extend(f"- {item}" for item in tensions[:3])
    return "\n".join(line for line in lines if line is not None).strip()


def _fallback_digest(root: Path, source_paths: list[str], title: str, content_fallback: str = "") -> dict[str, object]:
    records: list[dict[str, object]] = []
    for raw in source_paths:
        path = resolve_input_path(root, raw)
        if not path.exists():
            continue
        records.append(_heuristic_source_record(root, path, summary_kind="synthesis"))
    fallback_str = first_meaningful_line(content_fallback, title)
    findings = _heuristic_auto_findings(records)
    tensions = _heuristic_auto_tensions(records)
    summary = _heuristic_auto_summary(records, fallback_str, summary_kind="synthesis")
    body = _heuristic_auto_content(summary, findings, tensions)
    return {
        "summary": summary,
        "key_points": [],
        "body": body,
        "findings": findings,
        "tensions": tensions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Persist a multi-page digest into wiki/syntheses.")
    parser.add_argument("--root", default=".", help="Wiki root path")
    parser.add_argument("--title", required=True, help="Digest title")
    parser.add_argument("--summary", default="", help="Short summary stored in frontmatter")
    parser.add_argument("--content", default="", help="Optional long-form digest body")
    parser.add_argument("--source-path", action="append", default=[], help="Consulted wiki page path")
    parser.add_argument("--related-path", action="append", default=[], help="Related wiki page path")
    parser.add_argument("--finding", action="append", default=[], help="Key finding")
    parser.add_argument("--tension", action="append", default=[], help="Open tension or conflict")
    parser.add_argument("--slug", default="", help="Explicit target slug")
    parser.add_argument(
        "--update", action="store_true", help="Update an existing digest page with the same title or slug"
    )
    parser.add_argument(
        "--merge-mode",
        choices=["append", "replace", "dedupe"],
        default="dedupe",
        help="How to merge fields when --update is used",
    )
    args = parser.parse_args()

    root = find_repo_root(Path(args.root))
    records: list[dict[str, object]] = []
    if args.source_path:
        for raw in args.source_path:
            path = resolve_input_path(root, raw)
            if not path.exists():
                raise SystemExit(f"Source path not found: {raw}")
            records.append(source_record(root, path, summary_kind="synthesis"))

    auto_source_paths = ordered_unique(
        [
            source_path
            for record in records
            for source_path in list(record["source_paths"])
            or ([record["path"].relative_to(root).as_posix()] if Path(record["path"]).is_relative_to(root) else [])
        ]
    )
    auto_related_paths = ordered_unique([item for record in records for item in list(record["related_paths"])])

    source_data_list = [record["source_data"] for record in records]
    if llm_is_configured():
        llm_config = resolve_llm_config()
        print(
            f"Notice: sending source content to configured LLM at {llm_config.base_url} (model: {llm_config.model}).",
            file=sys.stderr,
        )
        try:
            llm_result = llm_digest(source_data_list, args.title, raise_on_failure=True)
        except Exception:
            print("Warning: LLM failed, falling back to heuristic mode.", file=sys.stderr)
            llm_result = _fallback_digest(root, args.source_path, args.title, args.content)
    else:
        llm_result = _fallback_digest(root, args.source_path, args.title, args.content)

    summary = args.summary.strip() or str(llm_result["summary"])
    content = args.content.strip() or str(llm_result["body"])
    page_path, action = write_page(
        root=root,
        kind="synthesis",
        title=args.title,
        summary=summary,
        content=content,
        source_paths=ordered_unique(args.source_path + auto_source_paths) or ["index.md"],
        related_paths=ordered_unique(args.related_path + auto_related_paths),
        follow_ups=[],
        findings=ordered_unique(args.finding + list(llm_result["findings"])),
        tensions=ordered_unique(args.tension + list(llm_result["tensions"])),
        key_points=[],
        action_label="digest",
        slug=args.slug,
        update=args.update,
        merge_mode=args.merge_mode,
    )
    output_home = refresh_output_home_if_present(root)
    print(f"{action.title()} {page_path.relative_to(root).as_posix()}")
    if output_home is not None:
        print("Output hub: output/index.html")
        print(f"Output hub URI: {file_uri(output_home)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
