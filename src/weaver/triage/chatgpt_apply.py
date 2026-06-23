from __future__ import annotations

import json
import os
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Sequence

import yaml

from weaver.triage.apply import ParsedTriageItem, parse_triage_document
from weaver.triage.chatgpt import (
    ChatGPTConversationRecord,
    load_chatgpt_conversation_records,
    render_conversation_transcript,
)


@dataclass(frozen=True)
class ChatGPTApplySummary:
    total_items: int
    selected_items: int
    copied_conversations: int
    written_transcripts: int
    written_artifacts: int
    skipped_items: int
    selected_decisions: tuple[str, ...]
    index_path: Path | None


def apply_chatgpt_triage(
    triage_path: Path,
    *,
    export_path: Path,
    raw_out: Path,
    artifact_out: Path,
    selected_decisions: Sequence[str],
    dry_run: bool = False,
) -> ChatGPTApplySummary:
    items = parse_chatgpt_triage_path(triage_path)
    selected = [item for item in items if item.decision in selected_decisions]

    if dry_run:
        return ChatGPTApplySummary(
            total_items=len(items),
            selected_items=len(selected),
            copied_conversations=0,
            written_transcripts=0,
            written_artifacts=0,
            skipped_items=len(items) - len(selected),
            selected_decisions=tuple(selected_decisions),
            index_path=artifact_out / "index.md",
        )

    records = load_chatgpt_conversation_records(export_path)
    raw_json_out = raw_out / "json"
    transcript_out = raw_out / "transcripts"
    raw_json_out.mkdir(parents=True, exist_ok=True)
    transcript_out.mkdir(parents=True, exist_ok=True)
    artifact_out.mkdir(parents=True, exist_ok=True)

    rows: list[tuple[ParsedTriageItem, Path, Path, Path]] = []
    for item in selected:
        conversation_id = _conversation_id(item)
        record = records.get(conversation_id)
        if record is None:
            raise KeyError(f"Conversation not found in export: {conversation_id}")

        stem = _artifact_stem(item)
        raw_json_path = raw_json_out / f"{stem}.json"
        transcript_path = transcript_out / f"{stem}.md"
        artifact_path = artifact_out / f"{stem}.md"

        raw_json_path.write_text(
            json.dumps(record.conversation, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        transcript_path.write_text(render_conversation_transcript(record), encoding="utf-8")
        artifact_path.write_text(
            _render_chatgpt_artifact(
                item,
                record=record,
                raw_json_path=raw_json_path,
                transcript_path=transcript_path,
                artifact_path=artifact_path,
            ),
            encoding="utf-8",
        )
        rows.append((item, raw_json_path, transcript_path, artifact_path))

    index_path = artifact_out / "index.md"
    index_path.write_text(
        _render_chatgpt_index(rows, selected_decisions=selected_decisions),
        encoding="utf-8",
    )

    return ChatGPTApplySummary(
        total_items=len(items),
        selected_items=len(selected),
        copied_conversations=len(rows),
        written_transcripts=len(rows),
        written_artifacts=len(rows),
        skipped_items=len(items) - len(selected),
        selected_decisions=tuple(selected_decisions),
        index_path=index_path,
    )


def parse_chatgpt_triage_path(path: Path) -> list[ParsedTriageItem]:
    path = path.expanduser()
    if path.is_dir():
        part_paths = sorted(path.glob("part-*.md"))
        if not part_paths:
            raise FileNotFoundError(f"No split ChatGPT triage part files found in {path}")
        return _parse_many(part_paths)

    items = parse_triage_document(path)
    if items:
        return items

    split_dir = path.with_suffix("")
    if split_dir.is_dir():
        part_paths = sorted(split_dir.glob("part-*.md"))
        if part_paths:
            return _parse_many(part_paths)
    return items


def _parse_many(paths: Sequence[Path]) -> list[ParsedTriageItem]:
    items: list[ParsedTriageItem] = []
    for path in paths:
        items.extend(parse_triage_document(path))
    return items


def _conversation_id(item: ParsedTriageItem) -> str:
    if "conversation_id" in item.metadata:
        return item.metadata["conversation_id"]
    return item.source_id.split(":", 1)[-1]


def _artifact_stem(item: ParsedTriageItem) -> str:
    return item.source_id.split(":", 1)[-1]


def _render_chatgpt_artifact(
    item: ParsedTriageItem,
    *,
    record: ChatGPTConversationRecord,
    raw_json_path: Path,
    transcript_path: Path,
    artifact_path: Path,
) -> str:
    frontmatter = {
        "source_id": item.source_id,
        "source_kind": item.source_kind,
        "decision": item.decision,
        "title": item.title,
        "conversation_id": record.conversation_id,
        "source_file": record.source_file,
        "project_id": item.metadata.get("project_id"),
        "raw_json_path": raw_json_path.as_posix(),
        "transcript_path": transcript_path.as_posix(),
        "category_labels": item.category_labels,
        "triage_comments": item.comments,
    }
    transcript_link = _relative_markdown_link(artifact_path, transcript_path)
    raw_json_link = _relative_markdown_link(artifact_path, raw_json_path)
    lines = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True).strip(),
        "---",
        "",
        f"# {item.title}",
        "",
        f"- source_id: {item.source_id}",
        f"- decision: {item.decision}",
        f"- conversation_id: {record.conversation_id}",
        f"- source_file: {record.source_file}",
        f"- project_id: {item.metadata.get('project_id', '')}",
        f"- transcript: [{transcript_path.name}]({transcript_link})",
        f"- raw_json: [{raw_json_path.name}]({raw_json_link})",
        f"- category_labels: {', '.join(item.category_labels) if item.category_labels else ''}",
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


def _render_chatgpt_index(
    rows: Sequence[tuple[ParsedTriageItem, Path, Path, Path]],
    *,
    selected_decisions: Sequence[str],
) -> str:
    generated = date.today().isoformat()
    decision_counts = Counter(item.decision for item, _json, _transcript, _artifact in rows)
    category_counts: Counter[str] = Counter()
    project_counts: Counter[str] = Counter()
    for item, _json, _transcript, _artifact in rows:
        category_counts.update(item.category_labels or ["uncategorized"])
        project_counts.update([item.metadata.get("project_id") or "no-project-id"])

    lines = [
        "# ChatGPT Applied Triage",
        "",
        f"Generated: {generated}",
        "",
        "## Summary",
        "",
        f"- Selected decisions: {', '.join(selected_decisions)}",
        f"- Total selected conversations: {len(rows)}",
    ]
    for decision in selected_decisions:
        lines.append(f"- {decision}: {decision_counts.get(decision, 0)}")

    lines.extend(["", "## Categories", ""])
    for category, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {category}: {count}")

    lines.extend(["", "## Project IDs", ""])
    for project_id, count in sorted(project_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {project_id}: {count}")

    lines.extend(["", "## Artifacts", ""])
    for item, _json, transcript_path, artifact_path in sorted(
        rows,
        key=lambda row: (row[0].decision, row[0].metadata.get("project_id") or "", row[0].title),
    ):
        categories = ", ".join(item.category_labels) if item.category_labels else "uncategorized"
        project_id = item.metadata.get("project_id") or "no-project-id"
        lines.append(
            f"- [{item.title}]({artifact_path.name}) - `{item.decision}` - "
            f"{categories} - `{project_id}` - transcript `{transcript_path.as_posix()}`"
        )
    return "\n".join(lines).rstrip() + "\n"


def _relative_markdown_link(from_path: Path, to_path: Path) -> str:
    return Path(os.path.relpath(to_path.resolve(), from_path.resolve().parent)).as_posix()
