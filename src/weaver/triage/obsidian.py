from __future__ import annotations

import os
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha1
from pathlib import Path
from typing import Iterable, Sequence

from weaver.triage.schema import SortMode, TriageItem

CORE_IGNORED_DIRS = frozenset({".obsidian", ".trash", ".git", "node_modules"})
ASSET_IGNORED_DIRS = frozenset({"assets", "attachments"})
PERIODIC_IGNORED_DIRS = frozenset({"daily", "weekly"})
DEFAULT_IGNORED_DIRS = CORE_IGNORED_DIRS | ASSET_IGNORED_DIRS | PERIODIC_IGNORED_DIRS
TINY_WORD_THRESHOLD = 25
LARGE_WORD_THRESHOLD = 5_000

_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
_TAG_RE = re.compile(r"(?<![\w/])#([A-Za-z0-9][A-Za-z0-9_/-]*)")
_WORD_RE = re.compile(r"\b[\w][\w'-]*\b")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class ObsidianScanSummary:
    vault_count: int
    total_markdown_files: int
    empty_or_tiny_files: int
    large_files: int
    ignored_dirs: tuple[str, ...]


@dataclass(frozen=True)
class _ScannedNote:
    item: TriageItem
    vault_path: Path
    relative_path: Path
    base_source_id: str


def scan_obsidian_vaults(
    vault_paths: Sequence[Path],
    *,
    include_assets: bool = False,
    include_periodic: bool = False,
) -> tuple[list[TriageItem], ObsidianScanSummary]:
    ignored_dirs = set(CORE_IGNORED_DIRS)
    if not include_assets:
        ignored_dirs.update(ASSET_IGNORED_DIRS)
    if not include_periodic:
        ignored_dirs.update(PERIODIC_IGNORED_DIRS)

    scanned: list[_ScannedNote] = []
    for vault_path in vault_paths:
        vault = vault_path.expanduser().resolve()
        if not vault.is_dir():
            raise NotADirectoryError(f"Obsidian vault does not exist: {vault}")

        for note_path in _iter_markdown_files(vault, ignored_dirs):
            scanned.append(_scan_note(vault, note_path))

    items = _dedupe_source_ids(scanned)
    empty_or_tiny = sum(1 for item in items if (item.word_count or 0) <= TINY_WORD_THRESHOLD)
    large = sum(1 for item in items if (item.word_count or 0) >= LARGE_WORD_THRESHOLD)
    summary = ObsidianScanSummary(
        vault_count=len(vault_paths),
        total_markdown_files=len(items),
        empty_or_tiny_files=empty_or_tiny,
        large_files=large,
        ignored_dirs=tuple(sorted(ignored_dirs)),
    )
    return items, summary


def sort_triage_items(items: Sequence[TriageItem], sort: SortMode) -> list[TriageItem]:
    if sort == SortMode.TITLE:
        return sorted(items, key=lambda item: (item.title.casefold(), item.path or ""))
    if sort == SortMode.MODIFIED_ASC:
        return sorted(items, key=lambda item: (item.updated_at or "", item.path or ""))
    if sort == SortMode.MODIFIED_DESC:
        return sorted(items, key=lambda item: (item.updated_at or "", item.path or ""), reverse=True)
    return sorted(items, key=lambda item: (item.path or "", item.title.casefold()))


def _iter_markdown_files(vault: Path, ignored_dirs: set[str]) -> Iterable[Path]:
    ignored_dir_keys = {dirname.casefold() for dirname in ignored_dirs}
    for root, dirnames, filenames in os.walk(vault):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if dirname.casefold() not in ignored_dir_keys and not dirname.startswith(".git")
        ]
        for filename in filenames:
            if filename.lower().endswith(".md"):
                yield Path(root) / filename


def _scan_note(vault: Path, note_path: Path) -> _ScannedNote:
    relative_path = note_path.relative_to(vault)
    stat = note_path.stat()
    text = note_path.read_text(encoding="utf-8", errors="replace")
    frontmatter, body = _split_frontmatter(text)
    frontmatter_tags = _extract_frontmatter_tags(frontmatter)
    inline_tags = _extract_inline_tags(body)
    tags = _merge_tags(frontmatter_tags, inline_tags)
    word_count = len(_WORD_RE.findall(body))
    first_heading = _extract_first_heading(body)
    title = first_heading or note_path.stem
    updated_at = datetime.fromtimestamp(stat.st_mtime).date().isoformat()
    summary_hint = _summary_hint(first_heading, note_path.stem, word_count)
    base_source_id = f"obsidian:{_slugify(relative_path.with_suffix('').as_posix())}"

    item = TriageItem(
        source_id=base_source_id,
        source_kind="obsidian",
        title=title,
        path=relative_path.as_posix(),
        created_at=None,
        updated_at=updated_at,
        size_bytes=stat.st_size,
        word_count=word_count,
        summary_hint=summary_hint,
        tags=tags,
        suggested_decision="skip" if word_count == 0 else None,
        metadata={"first_heading": first_heading},
    )
    return _ScannedNote(
        item=item,
        vault_path=vault,
        relative_path=relative_path,
        base_source_id=base_source_id,
    )


def _dedupe_source_ids(scanned: Sequence[_ScannedNote]) -> list[TriageItem]:
    counts = Counter(note.base_source_id for note in scanned)
    items: list[TriageItem] = []
    for note in scanned:
        source_id = note.base_source_id
        if counts[note.base_source_id] > 1:
            digest = sha1(
                f"{note.vault_path.as_posix()}::{note.relative_path.as_posix()}".encode("utf-8")
            ).hexdigest()[:8]
            source_id = f"{note.base_source_id}-{digest}"
        items.append(TriageItem(**{**note.item.__dict__, "source_id": source_id}))
    return items


def _split_frontmatter(text: str) -> tuple[list[str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :])
    return [], text


def _extract_frontmatter_tags(frontmatter: Sequence[str]) -> list[str]:
    tags: list[str] = []
    index = 0
    while index < len(frontmatter):
        raw_line = frontmatter[index]
        stripped = raw_line.strip()
        if not stripped.startswith("tags:"):
            index += 1
            continue

        value = stripped.partition(":")[2].strip()
        if value:
            tags.extend(_parse_tag_value(value))
            index += 1
            continue

        index += 1
        while index < len(frontmatter):
            candidate = frontmatter[index]
            candidate_stripped = candidate.strip()
            if not candidate.startswith((" ", "\t")):
                break
            if candidate_stripped.startswith("- "):
                tags.extend(_parse_tag_value(candidate_stripped[2:]))
            index += 1
    return _merge_tags(tags)


def _parse_tag_value(value: str) -> list[str]:
    cleaned = value.strip().strip("[]")
    if not cleaned:
        return []
    if "," in cleaned:
        parts = cleaned.split(",")
    else:
        parts = cleaned.split()
    return [_clean_tag(part) for part in parts if _clean_tag(part)]


def _extract_inline_tags(text: str) -> list[str]:
    return [_clean_tag(match.group(1)) for match in _TAG_RE.finditer(text)]


def _clean_tag(tag: str) -> str:
    return tag.strip().strip("'\"").lstrip("#").strip()


def _merge_tags(*tag_groups: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for group in tag_groups:
        for tag in group:
            cleaned = _clean_tag(tag)
            key = cleaned.casefold()
            if cleaned and key not in seen:
                seen.add(key)
                merged.append(cleaned)
    return merged


def _extract_first_heading(text: str) -> str | None:
    for line in text.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            return match.group(1).strip()
    return None


def _summary_hint(first_heading: str | None, file_stem: str, word_count: int) -> str | None:
    hints: list[str] = []
    if first_heading and first_heading != file_stem:
        hints.append(f"first heading: {first_heading}")
    if word_count == 0:
        hints.append("empty note")
    elif word_count <= TINY_WORD_THRESHOLD:
        hints.append("very short note")
    elif word_count >= LARGE_WORD_THRESHOLD:
        hints.append("large note")
    return "; ".join(hints) if hints else None


def _slugify(value: str) -> str:
    slug = _SLUG_RE.sub("-", value.casefold()).strip("-")
    return slug or "untitled"
