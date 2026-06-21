from __future__ import annotations

import os
import re
import shutil
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Iterable, Sequence

import yaml

from weaver.triage.schema import DECISION_OPTIONS

_TRIAGE_MARKER_RE = re.compile(r"^<!--\s*triage-item:\s*(?P<source_id>[^>]+?)\s*-->$")
_TITLE_RE = re.compile(r"^###\s+\d+\.\s+(?P<title>.+?)\s*$")
_CHECKBOX_RE = re.compile(r"^-\s+\[(?P<checked>[ xX])\]\s+(?P<decision>.+?)\s*$")
_METADATA_RE = re.compile(r"^-\s+(?P<key>[A-Za-z_]+):\s*(?P<value>.*)\s*$")
_SAFE_ARTIFACT_RE = re.compile(r"[^A-Za-z0-9_.-]+")


@dataclass(frozen=True)
class ParsedTriageItem:
    source_id: str
    source_kind: str
    title: str
    path: str
    decision: str
    category_labels: list[str] = field(default_factory=list)
    source_tags: list[str] = field(default_factory=list)
    comments: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ApplySummary:
    total_items: int
    selected_items: int
    copied_notes: int
    written_artifacts: int
    skipped_items: int
    selected_decisions: tuple[str, ...]
    index_path: Path | None


def parse_decisions(value: str) -> tuple[str, ...]:
    decisions = tuple(decision.strip() for decision in value.split(",") if decision.strip())
    unknown = [decision for decision in decisions if decision not in DECISION_OPTIONS]
    if unknown:
        raise ValueError(f"Unknown triage decisions: {', '.join(unknown)}")
    if not decisions:
        raise ValueError("At least one decision must be selected")
    return decisions


def parse_triage_document(path: Path) -> list[ParsedTriageItem]:
    text = path.read_text(encoding="utf-8")
    blocks = _split_item_blocks(text)
    items = [_parse_item_block(block) for block in blocks]
    _validate_items(items)
    return items


def apply_triage_document(
    triage_doc: Path,
    *,
    source_root: Path,
    raw_out: Path,
    artifact_out: Path,
    selected_decisions: Sequence[str],
    dry_run: bool = False,
) -> ApplySummary:
    items = parse_triage_document(triage_doc)
    selected = [item for item in items if item.decision in selected_decisions]

    if dry_run:
        return ApplySummary(
            total_items=len(items),
            selected_items=len(selected),
            copied_notes=0,
            written_artifacts=0,
            skipped_items=len(items) - len(selected),
            selected_decisions=tuple(selected_decisions),
            index_path=artifact_out / "index.md",
        )

    raw_out.mkdir(parents=True, exist_ok=True)
    artifact_out.mkdir(parents=True, exist_ok=True)

    copied = 0
    written = 0
    artifact_rows: list[tuple[ParsedTriageItem, Path, Path]] = []
    source_root = source_root.expanduser().resolve()

    for item in selected:
        source_path = _resolve_source_path(source_root, item.path)
        copied_path = raw_out / item.path
        copied_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, copied_path)
        copied += 1

        artifact_path = artifact_out / f"{_artifact_stem(item)}.md"
        artifact_path.write_text(
            _render_artifact(item, copied_path=copied_path, artifact_path=artifact_path),
            encoding="utf-8",
        )
        written += 1
        artifact_rows.append((item, copied_path, artifact_path))

    index_path = artifact_out / "index.md"
    index_path.write_text(
        _render_index(artifact_rows, selected_decisions=selected_decisions),
        encoding="utf-8",
    )

    return ApplySummary(
        total_items=len(items),
        selected_items=len(selected),
        copied_notes=copied,
        written_artifacts=written,
        skipped_items=len(items) - len(selected),
        selected_decisions=tuple(selected_decisions),
        index_path=index_path,
    )


def _split_item_blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] | None = None
    for line in text.splitlines():
        if _TRIAGE_MARKER_RE.match(line):
            if current is not None:
                blocks.append(current)
            current = [line]
        elif current is not None:
            current.append(line)
    if current is not None:
        blocks.append(current)
    return blocks


def _parse_item_block(lines: Sequence[str]) -> ParsedTriageItem:
    marker = _TRIAGE_MARKER_RE.match(lines[0])
    if marker is None:
        raise ValueError("Triage item block is missing a source marker")
    source_id = marker.group("source_id").strip()
    metadata: dict[str, str] = {}
    title = source_id
    decisions: list[str] = []

    for line in lines:
        title_match = _TITLE_RE.match(line)
        if title_match:
            title = title_match.group("title").strip()
            continue

        metadata_match = _METADATA_RE.match(line)
        if metadata_match:
            metadata[metadata_match.group("key")] = metadata_match.group("value").strip()
            continue

        checkbox_match = _CHECKBOX_RE.match(line)
        if checkbox_match and checkbox_match.group("checked").strip().casefold() == "x":
            decisions.append(checkbox_match.group("decision").strip())

    if len(decisions) != 1:
        raise ValueError(
            f"{source_id} must have exactly one checked decision; found {len(decisions)}"
        )

    item_source_id = metadata.get("source_id", source_id)
    source_kind = item_source_id.split(":", 1)[0] if ":" in item_source_id else "unknown"
    path = metadata.get("path")
    if not path:
        raise ValueError(f"{source_id} is missing a source path")

    return ParsedTriageItem(
        source_id=item_source_id,
        source_kind=source_kind,
        title=title,
        path=path,
        decision=decisions[0],
        category_labels=_split_labels(_extract_blockquote(lines, "Category labels:")),
        source_tags=_split_labels(metadata.get("tags", "")),
        comments=_empty_to_none(_extract_blockquote(lines, "Comments:")),
        metadata=metadata,
    )


def _validate_items(items: Sequence[ParsedTriageItem]) -> None:
    invalid = [item for item in items if item.decision not in DECISION_OPTIONS]
    if invalid:
        details = ", ".join(f"{item.source_id}: {item.decision}" for item in invalid[:10])
        raise ValueError(f"Unknown checked decisions found: {details}")

    duplicate_counts = Counter(item.source_id for item in items)
    duplicates = [source_id for source_id, count in duplicate_counts.items() if count > 1]
    if duplicates:
        raise ValueError(f"Duplicate source IDs in triage document: {', '.join(duplicates[:10])}")


def _extract_blockquote(lines: Sequence[str], label: str) -> str:
    in_block = False
    block_lines: list[str] = []
    for line in lines:
        if line == label:
            in_block = True
            continue
        if not in_block:
            continue
        if line.startswith(">"):
            block_lines.append(line[1:].strip())
            continue
        if line.strip() == "":
            if block_lines:
                break
            continue
        break
    return "\n".join(block_lines).strip()


def _split_labels(value: str | None) -> list[str]:
    if not value:
        return []
    labels: list[str] = []
    seen: set[str] = set()
    for label in re.split(r"[,\n]", value):
        cleaned = label.strip()
        key = cleaned.casefold()
        if cleaned and key not in seen:
            labels.append(cleaned)
            seen.add(key)
    return labels


def _empty_to_none(value: str) -> str | None:
    return value if value else None


def _resolve_source_path(source_root: Path, relative_path: str) -> Path:
    source_path = (source_root / relative_path).resolve()
    try:
        source_path.relative_to(source_root)
    except ValueError as exc:
        raise ValueError(f"Source path escapes source root: {relative_path}") from exc
    if not source_path.is_file():
        raise FileNotFoundError(f"Source note does not exist: {source_path}")
    return source_path


def _artifact_stem(item: ParsedTriageItem) -> str:
    source_id_stem = item.source_id.split(":", 1)[-1]
    stem = _SAFE_ARTIFACT_RE.sub("-", source_id_stem).strip("-")
    return stem or "untitled"


def _render_artifact(
    item: ParsedTriageItem,
    *,
    copied_path: Path,
    artifact_path: Path,
) -> str:
    frontmatter = {
        "source_id": item.source_id,
        "source_kind": item.source_kind,
        "decision": item.decision,
        "title": item.title,
        "original_path": item.path,
        "copied_path": copied_path.as_posix(),
        "category_labels": item.category_labels,
        "source_tags": item.source_tags,
        "triage_comments": item.comments,
    }
    rel_source = _relative_markdown_link(artifact_path, copied_path)
    lines = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip(),
        "---",
        "",
        f"# {item.title}",
        "",
        f"- source_id: {item.source_id}",
        f"- decision: {item.decision}",
        f"- original_path: {item.path}",
        f"- copied_source: [{copied_path.name}]({rel_source})",
        f"- category_labels: {', '.join(item.category_labels) if item.category_labels else ''}",
        f"- source_tags: {', '.join(item.source_tags) if item.source_tags else ''}",
        "",
        "## Triage Comments",
        "",
        item.comments or "_None._",
        "",
        "## Synthesis Notes",
        "",
        "- ",
    ]
    return "\n".join(lines).rstrip() + "\n"


def _render_index(
    rows: Sequence[tuple[ParsedTriageItem, Path, Path]],
    *,
    selected_decisions: Sequence[str],
) -> str:
    generated = date.today().isoformat()
    decision_counts = Counter(item.decision for item, _copied_path, _artifact_path in rows)
    category_counts: Counter[str] = Counter()
    for item, _copied_path, _artifact_path in rows:
        category_counts.update(item.category_labels or ["uncategorized"])

    lines = [
        "# Obsidian Applied Triage",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Selected decisions: {', '.join(selected_decisions)}",
        f"- Total selected notes: {len(rows)}",
    ]
    for decision in selected_decisions:
        lines.append(f"- {decision}: {decision_counts.get(decision, 0)}")

    lines.extend(["", "## Categories", ""])
    for category, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Artifacts", ""])
    for item, copied_path, artifact_path in sorted(rows, key=lambda row: (row[0].decision, row[0].path)):
        artifact_link = artifact_path.name
        categories = ", ".join(item.category_labels) if item.category_labels else "uncategorized"
        lines.append(
            f"- [{item.title}]({artifact_link}) "
            f"- `{item.decision}` - {categories} - source `{copied_path.as_posix()}`"
        )

    return "\n".join(lines).rstrip() + "\n"


def _relative_markdown_link(from_path: Path, to_path: Path) -> str:
    return Path(os.path.relpath(to_path.resolve(), from_path.resolve().parent)).as_posix()
