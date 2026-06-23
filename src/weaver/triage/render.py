from __future__ import annotations

import csv
import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Sequence

from weaver.triage.chatgpt import ChatGPTScanSummary
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
        "Use Category labels for comma-separated labels you assign during triage.",
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


def render_chatgpt_triage(
    items: Sequence[TriageItem],
    summary: ChatGPTScanSummary,
    *,
    generated_on: date | None = None,
    title: str = "ChatGPT Conversation Triage",
) -> str:
    generated = generated_on or date.today()
    lines: list[str] = [
        f"# {title}",
        "",
        f"Generated: {generated.isoformat()}",
        "",
        "Instructions:",
        "Mark one decision for each conversation. Prefer extract-insights for conversations with durable ideas that should not be imported verbatim.",
        "Use Category labels for comma-separated labels you assign during triage.",
        "",
        "Decision options:",
    ]
    lines.extend(f"- {decision}" for decision in DECISION_OPTIONS)
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Export path: {summary.export_path}",
            f"- Conversation files: {summary.conversation_files}",
            f"- Total conversations: {summary.total_conversations}",
            f"- Conversations listed: {len(items)}",
            f"- Total visible messages: {summary.total_messages}",
            f"- Total user messages: {summary.total_user_messages}",
            f"- Long conversations: {summary.long_conversations}",
            f"- Untitled conversations: {summary.untitled_conversations}",
            "",
            "## Conversations",
            "",
        ]
    )

    for index, item in enumerate(items, start=1):
        lines.extend(_render_chatgpt_item(index, item))

    return "\n".join(lines).rstrip() + "\n"


def render_chatgpt_split_index(
    *,
    summary: ChatGPTScanSummary,
    parts: Sequence[tuple[Path, int, int]],
    generated_on: date | None = None,
) -> str:
    generated = generated_on or date.today()
    lines: list[str] = [
        "# ChatGPT Conversation Triage",
        "",
        f"Generated: {generated.isoformat()}",
        "",
        "This triage document is split into part files for easier manual editing.",
        "",
        "## Summary",
        "",
        f"- Export path: {summary.export_path}",
        f"- Conversation files: {summary.conversation_files}",
        f"- Total conversations: {summary.total_conversations}",
        f"- Total visible messages: {summary.total_messages}",
        f"- Total user messages: {summary.total_user_messages}",
        f"- Long conversations: {summary.long_conversations}",
        f"- Untitled conversations: {summary.untitled_conversations}",
        f"- Parts: {len(parts)}",
        "",
        "## Parts",
        "",
    ]
    for path, start, end in parts:
        label = f"{start:03d}-{end:03d}"
        lines.append(f"- [{label}]({path.as_posix()})")
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
        "category_labels",
        "suggested_decision",
        "metadata",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item in items:
            row = asdict(item)
            row["tags"] = json.dumps(item.tags, ensure_ascii=False)
            row["category_labels"] = json.dumps(item.category_labels, ensure_ascii=False)
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

    lines.extend(["", "Category labels:", ">"])
    lines.extend(["", "Decision:"])
    lines.extend(f"- [ ] {decision}" for decision in DECISION_OPTIONS)
    lines.extend(["", "Comments:", ">", ""])
    return lines


def _render_chatgpt_item(index: int, item: TriageItem) -> list[str]:
    metadata = item.metadata
    lines = [
        f"<!-- triage-item: {item.source_id} -->",
        f"### {index:03d}. {_single_line(item.title)}",
        f"- source_id: {item.source_id}",
    ]
    if item.path is not None:
        lines.append(f"- path: {item.path}")
    source_file = metadata.get("source_file")
    if source_file is not None:
        lines.append(f"- source_file: {source_file}")
    if item.created_at is not None:
        lines.append(f"- created: {item.created_at}")
    if item.updated_at is not None:
        lines.append(f"- updated: {item.updated_at}")
    if metadata.get("message_count") is not None:
        lines.append(f"- messages: {metadata['message_count']}")
    if metadata.get("user_message_count") is not None:
        lines.append(f"- user_messages: {metadata['user_message_count']}")
    if metadata.get("assistant_message_count") is not None:
        lines.append(f"- assistant_messages: {metadata['assistant_message_count']}")
    if item.word_count is not None:
        lines.append(f"- approx_words: {item.word_count}")
    if metadata.get("model"):
        lines.append(f"- model: {metadata['model']}")
    if metadata.get("project_id"):
        lines.append(f"- project_id: {metadata['project_id']}")
    if item.suggested_decision:
        lines.append(f"- suggested_decision: {item.suggested_decision}")

    first_user_excerpt = metadata.get("first_user_excerpt")
    if first_user_excerpt:
        lines.extend(["", "First user message:", f"> {_single_line(str(first_user_excerpt))}"])
    last_user_excerpt = metadata.get("last_user_excerpt")
    if last_user_excerpt and last_user_excerpt != first_user_excerpt:
        lines.extend(["", "Last user message:", f"> {_single_line(str(last_user_excerpt))}"])

    lines.extend(["", "Category labels:", ">"])
    lines.extend(["", "Decision:"])
    lines.extend(f"- [ ] {decision}" for decision in DECISION_OPTIONS)
    lines.extend(["", "Comments:", ">", ""])
    return lines


def _single_line(value: str) -> str:
    return " ".join(value.split())
