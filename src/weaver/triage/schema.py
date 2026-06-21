from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

SourceKind = Literal["obsidian", "chatgpt"]

DECISION_OPTIONS: tuple[str, ...] = (
    "include",
    "extract-insights",
    "include-later",
    "skip",
    "sensitive / exclude",
)


class SortMode(str, Enum):
    PATH = "path"
    TITLE = "title"
    MODIFIED_ASC = "modified-asc"
    MODIFIED_DESC = "modified-desc"


@dataclass(frozen=True)
class TriageItem:
    source_id: str
    source_kind: SourceKind
    title: str
    path: str | None
    created_at: str | None
    updated_at: str | None
    size_bytes: int | None
    word_count: int | None
    summary_hint: str | None
    tags: list[str] = field(default_factory=list)
    category_labels: list[str] = field(default_factory=list)
    suggested_decision: str | None = None
    metadata: dict[str, str | int | None] = field(default_factory=dict)
