from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Sequence

from weaver.triage.obsidian import ObsidianScanSummary
from weaver.triage.schema import DECISION_OPTIONS, TriageItem


def render_obsidian_triage(
    items: Sequence[TriageItem],
    summary: ObsidianScanSummary,
    *,
    generated_on: date | None = None,
) -> str:
    generated = generated_on or date.today()
    lines: list[str] = [
        "# Obsidian Vault Triage",
        "",
        f"Generated: {generated.isoformat()}",
        "",
        "Instructions:",
        "Mark one decision for each note. Add brief comments where useful.",
        "",
        "Decision options:",
    ]
    lines.extend(f"- {decision}" for decision in DECISION_OPTIONS)
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Vaults scanned: {summary.vault_count}",
            f"- Total markdown files: {summary.total_markdown_files}",
            f"- Notes listed: {len(items)}",
            f"- Empty or tiny files: {summary.empty_or_tiny_files}",
            f"- Large files: {summary.large_files}",
            f"- Ignored directories: {', '.join(summary.ignored_dirs)}",
            "",
            "## Notes",
            "",
        ]
    )

    for index, item in enumerate(items, start=1):
        lines.extend(_render_item(index, item))

    return "\n".join(lines).rstrip() + "\n"


def write_manifest_csv(path: Path, items: Sequence[TriageItem]) -> None:
    fieldnames = [
        "source_id",
        "source_kind",
        "title",
        "path",
        "created_at",
        "updated_at",
        "size_bytes",
        "word_count",
        "summary_hint",
        "tags",
        "suggested_decision",
        "metadata",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            row = asdict(item)
            row["tags"] = json.dumps(item.tags, ensure_ascii=False)
            row["metadata"] = json.dumps(item.metadata, ensure_ascii=False)
            writer.writerow(row)


def _render_item(index: int, item: TriageItem) -> list[str]:
    lines = [
        f"<!-- triage-item: {item.source_id} -->",
        f"### {index:03d}. {_single_line(item.title)}",
        f"- source_id: {item.source_id}",
    ]
    if item.path is not None:
        lines.append(f"- path: {item.path}")
    if item.word_count is not None:
        lines.append(f"- words: {item.word_count}")
    if item.size_bytes is not None:
        lines.append(f"- size_bytes: {item.size_bytes}")
    if item.updated_at is not None:
        lines.append(f"- modified: {item.updated_at}")
    if item.tags:
        lines.append(f"- tags: {', '.join(item.tags)}")
    if item.summary_hint:
        lines.append(f"- hint: {_single_line(item.summary_hint)}")
    if item.suggested_decision:
        lines.append(f"- suggested_decision: {item.suggested_decision}")

    lines.extend(["", "Decision:"])
    lines.extend(f"- [ ] {decision}" for decision in DECISION_OPTIONS)
    lines.extend(["", "Comments:", ">", ""])
    return lines


def _single_line(value: str) -> str:
    return " ".join(value.split())
