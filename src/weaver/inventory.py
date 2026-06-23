from __future__ import annotations

import csv
import os
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Sequence

import yaml

CATEGORY_ALIASES = {
    "cogitive": "cognitive",
    "cogntive": "cognitive",
    "cognition": "cognitive",
    "creative": "creativity",
    "ideas": "idea",
    "quantc": "quant",
    "quatn": "quant",
}


@dataclass(frozen=True)
class ProjectInfo:
    key: str
    status: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class ChatGPTProjectInfo:
    project_id: str
    inferred_name: str
    project_labels: tuple[str, ...]
    description: str | None = None
    confidence: str | None = None


@dataclass(frozen=True)
class InventoryRecord:
    source_id: str
    source_kind: str
    decision: str
    title: str
    artifact_path: Path
    source_path: str | None
    category_labels: tuple[str, ...]
    normalized_category_labels: tuple[str, ...]
    source_tags: tuple[str, ...]
    project_labels: tuple[str, ...]
    project_reasons: tuple[str, ...]
    project_id: str | None = None
    chatgpt_project_name: str | None = None
    chatgpt_project_confidence: str | None = None
    triage_comments: str | None = None


@dataclass(frozen=True)
class SourceInventory:
    records: tuple[InventoryRecord, ...]
    projects: tuple[ProjectInfo, ...]
    generated_on: date = field(default_factory=date.today)


def build_source_inventory(
    artifact_dirs: Sequence[Path],
    *,
    project_glossary_path: Path = Path("ops/context/project-glossary.yaml"),
    chatgpt_project_glossary_path: Path = Path("ops/context/chatgpt-project-glossary.yaml"),
    generated_on: date | None = None,
) -> SourceInventory:
    projects = load_project_glossary(project_glossary_path)
    chatgpt_projects = load_chatgpt_project_glossary(chatgpt_project_glossary_path)
    records = [
        _record_from_artifact(path, projects=projects, chatgpt_projects=chatgpt_projects)
        for path in _artifact_files(artifact_dirs)
    ]
    return SourceInventory(
        records=tuple(sorted(records, key=lambda record: (record.source_kind, record.title.casefold()))),
        projects=tuple(projects.values()),
        generated_on=generated_on or date.today(),
    )


def load_project_glossary(path: Path) -> dict[str, ProjectInfo]:
    if not path.exists():
        return {}
    data = _load_yaml_mapping(path)
    raw_projects = data.get("projects", {})
    if not isinstance(raw_projects, dict):
        raise ValueError(f"Expected 'projects' mapping in {path}")

    projects: dict[str, ProjectInfo] = {}
    for key, raw_info in raw_projects.items():
        info = raw_info if isinstance(raw_info, dict) else {}
        project_key = str(key)
        projects[project_key] = ProjectInfo(
            key=project_key,
            status=_optional_str(info.get("status")),
            description=_optional_str(info.get("description")),
        )
    return projects


def load_chatgpt_project_glossary(path: Path) -> dict[str, ChatGPTProjectInfo]:
    if not path.exists():
        return {}
    data = _load_yaml_mapping(path)
    raw_projects = data.get("chatgpt_projects", {})
    if not isinstance(raw_projects, dict):
        raise ValueError(f"Expected 'chatgpt_projects' mapping in {path}")

    projects: dict[str, ChatGPTProjectInfo] = {}
    for project_id, raw_info in raw_projects.items():
        info = raw_info if isinstance(raw_info, dict) else {}
        projects[str(project_id)] = ChatGPTProjectInfo(
            project_id=str(project_id),
            inferred_name=str(info.get("inferred_name") or project_id),
            project_labels=tuple(_list_of_str(info.get("project_labels"))),
            description=_optional_str(info.get("description")),
            confidence=_optional_str(info.get("confidence")),
        )
    return projects


def write_inventory_qmd(inventory: SourceInventory, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_inventory_qmd(inventory, output_path=path), encoding="utf-8")


def write_inventory_manifest_csv(inventory: SourceInventory, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_id",
        "source_kind",
        "decision",
        "title",
        "project_labels",
        "project_reasons",
        "category_labels",
        "normalized_category_labels",
        "artifact_path",
        "source_path",
        "project_id",
        "chatgpt_project_name",
        "chatgpt_project_confidence",
        "triage_comments",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for record in inventory.records:
            writer.writerow(
                {
                    "source_id": record.source_id,
                    "source_kind": record.source_kind,
                    "decision": record.decision,
                    "title": record.title,
                    "project_labels": ", ".join(record.project_labels),
                    "project_reasons": "; ".join(record.project_reasons),
                    "category_labels": ", ".join(record.category_labels),
                    "normalized_category_labels": ", ".join(record.normalized_category_labels),
                    "artifact_path": record.artifact_path.as_posix(),
                    "source_path": record.source_path or "",
                    "project_id": record.project_id or "",
                    "chatgpt_project_name": record.chatgpt_project_name or "",
                    "chatgpt_project_confidence": record.chatgpt_project_confidence or "",
                    "triage_comments": record.triage_comments or "",
                }
            )


def render_inventory_qmd(inventory: SourceInventory, *, output_path: Path) -> str:
    records = inventory.records
    source_counts = Counter(record.source_kind for record in records)
    decision_counts = Counter(record.decision for record in records)
    category_counts: Counter[str] = Counter()
    project_counts: Counter[str] = Counter()
    alias_counts: Counter[tuple[str, str]] = Counter()

    for record in records:
        category_counts.update(record.normalized_category_labels or ["uncategorized"])
        project_counts.update(record.project_labels or ["unassigned"])
        for original, normalized in zip(record.category_labels, record.normalized_category_labels):
            if original != normalized:
                alias_counts[(original, normalized)] += 1

    lines = [
        "---",
        'title: "Source Inventory Workbench"',
        f"date: {inventory.generated_on.isoformat()}",
        "format: gfm",
        "---",
        "",
        "This is a deterministic staging view over applied source artifacts. It does not perform synthesis.",
        "",
        "## Summary",
        "",
        f"- Generated: {inventory.generated_on.isoformat()}",
        f"- Total artifacts: {len(records)}",
        f"- Source kinds: {_counter_inline(source_counts)}",
        f"- Decisions: {_counter_inline(decision_counts)}",
        f"- Project assignments: {_counter_inline(project_counts)}",
        f"- Normalized categories: {_counter_inline(category_counts)}",
        "",
        "## Project Overview",
        "",
        "| Project | Status | Artifacts | Sources | Decisions | Top Categories |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]

    for project in inventory.projects:
        project_records = [record for record in records if project.key in record.project_labels]
        lines.append(_project_overview_row(project.key, project.status, project_records))
    unassigned = [record for record in records if not record.project_labels]
    if unassigned:
        lines.append(_project_overview_row("unassigned", None, unassigned))

    lines.extend(
        [
            "",
            "## Category Overview",
            "",
            "| Category | Artifacts | Sources | Projects |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for category, _count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0])):
        category_records = [
            record
            for record in records
            if category in (record.normalized_category_labels or ("uncategorized",))
        ]
        project_values: Counter[str] = Counter()
        for record in category_records:
            project_values.update(record.project_labels or ["unassigned"])
        lines.append(
            "| "
            + " | ".join(
                [
                    _table_cell(category),
                    str(len(category_records)),
                    _table_cell(_counter_inline(Counter(record.source_kind for record in category_records))),
                    _table_cell(_counter_inline(project_values, limit=5)),
                ]
            )
            + " |"
        )

    lines.extend(["", "## Label Normalization", ""])
    if alias_counts:
        lines.extend(["| Original | Normalized | Artifacts |", "| --- | --- | ---: |"])
        for (original, normalized), count in sorted(alias_counts.items(), key=lambda item: (-item[1], item[0])):
            lines.append(f"| {_table_cell(original)} | {_table_cell(normalized)} | {count} |")
    else:
        lines.append("_No label aliases were applied._")

    lines.extend(["", "## Project Bundles", ""])
    for project in inventory.projects:
        project_records = [record for record in records if project.key in record.project_labels]
        if not project_records:
            continue
        lines.extend(_render_record_bundle(project.key, project_records, output_path=output_path))
    if unassigned:
        lines.extend(_render_record_bundle("unassigned", unassigned, output_path=output_path))

    attention_records = [
        record
        for record in records
        if not record.project_labels or not record.normalized_category_labels
    ]
    lines.extend(["", "## Attention Queue", ""])
    if attention_records:
        lines.extend(_render_record_table(attention_records, output_path=output_path))
    else:
        lines.append("_No unassigned or uncategorized artifacts._")

    lines.extend(["", "## Complete Artifact Index", ""])
    lines.extend(_render_record_table(records, output_path=output_path))
    return "\n".join(lines).rstrip() + "\n"


def _artifact_files(artifact_dirs: Sequence[Path]) -> Iterable[Path]:
    for artifact_dir in artifact_dirs:
        if not artifact_dir.exists():
            continue
        if not artifact_dir.is_dir():
            raise NotADirectoryError(f"Artifact path is not a directory: {artifact_dir}")
        for path in sorted(artifact_dir.glob("*.md")):
            if path.name == "index.md":
                continue
            yield path


def _record_from_artifact(
    path: Path,
    *,
    projects: dict[str, ProjectInfo],
    chatgpt_projects: dict[str, ChatGPTProjectInfo],
) -> InventoryRecord:
    data, body = _read_artifact(path)
    source_id = str(data.get("source_id") or path.stem)
    source_kind = str(data.get("source_kind") or source_id.split(":", 1)[0])
    title = str(data.get("title") or path.stem)
    category_labels = tuple(_list_of_str(data.get("category_labels")))
    normalized_categories = tuple(_normalize_categories(category_labels))
    source_tags = tuple(_list_of_str(data.get("source_tags")))
    project_id = _optional_str(data.get("project_id"))
    chatgpt_project = chatgpt_projects.get(project_id or "")
    source_path = _source_path(data)
    triage_comments = _optional_str(data.get("triage_comments"))
    project_labels, project_reasons = _infer_projects(
        data,
        projects=projects,
        chatgpt_project=chatgpt_project,
        category_labels=category_labels,
        source_tags=source_tags,
        source_path=source_path,
        title=title,
        triage_comments=triage_comments,
        artifact_body=body,
    )
    return InventoryRecord(
        source_id=source_id,
        source_kind=source_kind,
        decision=str(data.get("decision") or ""),
        title=title,
        artifact_path=path,
        source_path=source_path,
        category_labels=category_labels,
        normalized_category_labels=normalized_categories,
        source_tags=source_tags,
        project_labels=tuple(project_labels),
        project_reasons=tuple(project_reasons),
        project_id=project_id,
        chatgpt_project_name=chatgpt_project.inferred_name if chatgpt_project else None,
        chatgpt_project_confidence=chatgpt_project.confidence if chatgpt_project else None,
        triage_comments=triage_comments,
    )


def _read_artifact(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Artifact is missing YAML frontmatter: {path}")
    try:
        _start, frontmatter, body = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"Artifact has invalid YAML frontmatter: {path}") from exc
    data = yaml.safe_load(frontmatter) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Artifact frontmatter must be a mapping: {path}")
    return data, body


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected YAML mapping in {path}")
    return data


def _source_path(data: dict[str, Any]) -> str | None:
    for key in ("original_path", "copied_path", "transcript_path", "raw_json_path"):
        value = _optional_str(data.get(key))
        if value:
            return value
    return None


def _infer_projects(
    data: dict[str, Any],
    *,
    projects: dict[str, ProjectInfo],
    chatgpt_project: ChatGPTProjectInfo | None,
    category_labels: Sequence[str],
    source_tags: Sequence[str],
    source_path: str | None,
    title: str,
    triage_comments: str | None,
    artifact_body: str,
) -> tuple[list[str], list[str]]:
    labels: list[str] = []
    reasons: list[str] = []

    if chatgpt_project is not None:
        for label in chatgpt_project.project_labels:
            _append_unique(labels, label)
            reasons.append(f"project_id:{chatgpt_project.project_id}->{label}")

    searchable_fields = {
        "title": title,
        "source_path": source_path or "",
        "triage_comments": triage_comments or "",
        "source_id": str(data.get("source_id") or ""),
        "category_labels": " ".join(category_labels),
        "source_tags": " ".join(source_tags),
        "artifact_body": artifact_body,
    }
    for project_key in projects:
        pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(project_key.casefold())}(?![A-Za-z0-9])")
        for field, value in searchable_fields.items():
            if pattern.search(value.casefold()):
                _append_unique(labels, project_key)
                reasons.append(f"{field}:{project_key}")
                break

    return labels, _dedupe(reasons)


def _normalize_categories(labels: Sequence[str]) -> list[str]:
    normalized: list[str] = []
    for label in labels:
        cleaned = " ".join(label.strip().split()).casefold()
        mapped = CATEGORY_ALIASES.get(cleaned, cleaned)
        if mapped:
            _append_unique(normalized, mapped)
    return normalized


def _project_overview_row(
    project_key: str,
    status: str | None,
    records: Sequence[InventoryRecord],
) -> str:
    source_counts = Counter(record.source_kind for record in records)
    decision_counts = Counter(record.decision for record in records)
    category_counts: Counter[str] = Counter()
    for record in records:
        category_counts.update(record.normalized_category_labels or ["uncategorized"])
    return (
        "| "
        + " | ".join(
            [
                _table_cell(project_key),
                _table_cell(status or ""),
                str(len(records)),
                _table_cell(_counter_inline(source_counts)),
                _table_cell(_counter_inline(decision_counts)),
                _table_cell(_counter_inline(category_counts, limit=5)),
            ]
        )
        + " |"
    )


def _render_record_bundle(
    heading: str,
    records: Sequence[InventoryRecord],
    *,
    output_path: Path,
) -> list[str]:
    source_counts = Counter(record.source_kind for record in records)
    decision_counts = Counter(record.decision for record in records)
    lines = [
        f"### {heading}",
        "",
        f"- Artifacts: {len(records)}",
        f"- Sources: {_counter_inline(source_counts)}",
        f"- Decisions: {_counter_inline(decision_counts)}",
        "",
    ]
    lines.extend(_render_record_table(records, output_path=output_path))
    lines.append("")
    return lines


def _render_record_table(records: Sequence[InventoryRecord], *, output_path: Path) -> list[str]:
    lines = [
        "| Title | Source | Decision | Projects | Categories | Artifact | Hints |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in sorted(
        records,
        key=lambda item: (
            item.source_kind,
            item.decision,
            ", ".join(item.project_labels),
            item.title.casefold(),
        ),
    ):
        lines.append(
            "| "
            + " | ".join(
                [
                    _table_cell(record.title),
                    _table_cell(record.source_kind),
                    _table_cell(record.decision),
                    _table_cell(", ".join(record.project_labels) or "unassigned"),
                    _table_cell(", ".join(record.normalized_category_labels) or "uncategorized"),
                    _table_cell(_artifact_link(record, output_path=output_path)),
                    _table_cell("; ".join(record.project_reasons)),
                ]
            )
            + " |"
        )
    return lines


def _artifact_link(record: InventoryRecord, *, output_path: Path) -> str:
    rel_path = Path(os.path.relpath(record.artifact_path.resolve(), output_path.resolve().parent))
    return f"[{record.artifact_path.name}]({rel_path.as_posix()})"


def _counter_inline(counter: Counter[str], *, limit: int | None = None) -> str:
    if not counter:
        return ""
    items = sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    if limit is not None:
        items = items[:limit]
    return ", ".join(f"{key} {count}" for key, count in items)


def _table_cell(value: str) -> str:
    return " ".join(value.split()).replace("|", "\\|")


def _append_unique(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)


def _dedupe(values: Sequence[str]) -> list[str]:
    deduped: list[str] = []
    for value in values:
        _append_unique(deduped, value)
    return deduped


def _list_of_str(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(value)]


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
