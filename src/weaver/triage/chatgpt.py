from __future__ import annotations

import json
import re
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Iterable, Iterator, Sequence

from weaver.triage.schema import ChatGPTSortMode, TriageItem

_WORD_RE = re.compile(r"\b[\w][\w'-]*\b")
_WHITESPACE_RE = re.compile(r"\s+")


@dataclass(frozen=True)
class ChatGPTScanSummary:
    export_path: str
    conversation_files: int
    total_conversations: int
    total_messages: int
    total_user_messages: int
    long_conversations: int
    untitled_conversations: int


@dataclass(frozen=True)
class _Message:
    role: str
    text: str
    created_at: float | None


@dataclass(frozen=True)
class ChatGPTConversationRecord:
    conversation_id: str
    source_file: str
    title: str
    conversation: dict[str, Any]
    messages: tuple[_Message, ...]


def scan_chatgpt_export(
    export_path: Path,
    *,
    max_excerpt_chars: int = 500,
) -> tuple[list[TriageItem], ChatGPTScanSummary]:
    export_path = export_path.expanduser().resolve()
    if export_path.is_file() and export_path.suffix.casefold() == ".zip":
        with TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(export_path) as archive:
                archive.extractall(tmpdir)
            return _scan_chatgpt_path(
                Path(tmpdir),
                export_label=export_path.as_posix(),
                max_excerpt_chars=max_excerpt_chars,
            )

    return _scan_chatgpt_path(
        export_path,
        export_label=export_path.as_posix(),
        max_excerpt_chars=max_excerpt_chars,
    )


def load_chatgpt_conversation_records(
    export_path: Path,
) -> dict[str, ChatGPTConversationRecord]:
    export_path = export_path.expanduser().resolve()
    if export_path.is_file() and export_path.suffix.casefold() == ".zip":
        with TemporaryDirectory() as tmpdir:
            with zipfile.ZipFile(export_path) as archive:
                archive.extractall(tmpdir)
            return _load_chatgpt_conversation_records(Path(tmpdir))
    return _load_chatgpt_conversation_records(export_path)


def render_conversation_transcript(record: ChatGPTConversationRecord) -> str:
    lines = [
        f"# {record.title}",
        "",
        f"- conversation_id: {record.conversation_id}",
        f"- source_file: {record.source_file}",
        "",
        "## Transcript",
        "",
    ]
    for message in record.messages:
        if not message.text:
            continue
        role = message.role.title() if message.role else "Unknown"
        lines.extend([f"### {role}", "", message.text, ""])
    return "\n".join(lines).rstrip() + "\n"


def sort_chatgpt_items(
    items: Sequence[TriageItem],
    sort: ChatGPTSortMode,
) -> list[TriageItem]:
    if sort == ChatGPTSortMode.UPDATED_ASC:
        return sorted(items, key=lambda item: (item.updated_at or "", item.title.casefold()))
    if sort == ChatGPTSortMode.CREATED_DESC:
        return sorted(
            items,
            key=lambda item: (item.created_at or "", item.updated_at or "", item.title.casefold()),
            reverse=True,
        )
    if sort == ChatGPTSortMode.CREATED_ASC:
        return sorted(items, key=lambda item: (item.created_at or "", item.title.casefold()))
    if sort == ChatGPTSortMode.TITLE:
        return sorted(items, key=lambda item: (item.title.casefold(), item.updated_at or ""))
    return sorted(
        items,
        key=lambda item: (item.updated_at or "", item.created_at or "", item.title.casefold()),
        reverse=True,
    )


def _load_chatgpt_conversation_records(
    export_path: Path,
) -> dict[str, ChatGPTConversationRecord]:
    records: dict[str, ChatGPTConversationRecord] = {}
    for conversation_file in _conversation_files(export_path):
        for conversation in _load_conversations(conversation_file):
            conversation_id = str(
                conversation.get("conversation_id")
                or conversation.get("id")
                or conversation.get("current_node")
                or "unknown"
            )
            records[conversation_id] = ChatGPTConversationRecord(
                conversation_id=conversation_id,
                source_file=_relative_to_export(conversation_file, export_path),
                title=_clean_title(conversation.get("title")),
                conversation=conversation,
                messages=tuple(_messages(conversation)),
            )
    return records


def _scan_chatgpt_path(
    export_path: Path,
    *,
    export_label: str,
    max_excerpt_chars: int,
) -> tuple[list[TriageItem], ChatGPTScanSummary]:
    conversation_files = list(_conversation_files(export_path))
    if not conversation_files:
        raise FileNotFoundError(f"No ChatGPT conversation JSON files found under {export_path}")

    items: list[TriageItem] = []
    total_messages = 0
    total_user_messages = 0
    long_conversations = 0
    untitled_conversations = 0

    for conversation_file in conversation_files:
        conversations = _load_conversations(conversation_file)
        for conversation in conversations:
            item, message_count, user_message_count = _conversation_to_item(
                conversation,
                conversation_file=conversation_file,
                export_path=export_path,
                max_excerpt_chars=max_excerpt_chars,
            )
            items.append(item)
            total_messages += message_count
            total_user_messages += user_message_count
            if message_count >= 40 or (item.word_count or 0) >= 5_000:
                long_conversations += 1
            if _is_untitled(item.title):
                untitled_conversations += 1

    summary = ChatGPTScanSummary(
        export_path=export_label,
        conversation_files=len(conversation_files),
        total_conversations=len(items),
        total_messages=total_messages,
        total_user_messages=total_user_messages,
        long_conversations=long_conversations,
        untitled_conversations=untitled_conversations,
    )
    return items, summary


def _conversation_files(export_path: Path) -> Iterable[Path]:
    if export_path.is_file():
        if export_path.name == "conversations.json" or export_path.name.startswith("conversations-"):
            yield export_path
        return

    single_file = export_path / "conversations.json"
    if single_file.exists():
        yield single_file
        return

    yield from sorted(export_path.glob("conversations-*.json"))


def _load_conversations(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected a list of conversations in {path}")
    conversations = [conversation for conversation in data if isinstance(conversation, dict)]
    if len(conversations) != len(data):
        raise ValueError(f"Unexpected non-object conversation entries in {path}")
    return conversations


def _conversation_to_item(
    conversation: dict[str, Any],
    *,
    conversation_file: Path,
    export_path: Path,
    max_excerpt_chars: int,
) -> tuple[TriageItem, int, int]:
    conversation_id = str(
        conversation.get("conversation_id")
        or conversation.get("id")
        or conversation.get("current_node")
        or "unknown"
    )
    title = _clean_title(conversation.get("title"))
    messages = _messages(conversation)
    visible_messages = [message for message in messages if message.text]
    user_messages = [message for message in visible_messages if message.role == "user"]
    assistant_messages = [message for message in visible_messages if message.role == "assistant"]
    all_text = "\n".join(message.text for message in visible_messages)
    word_count = len(_WORD_RE.findall(all_text))
    source_file = _relative_to_export(conversation_file, export_path)
    first_user_excerpt = _excerpt(user_messages[0].text, max_excerpt_chars) if user_messages else None
    last_user_excerpt = _excerpt(user_messages[-1].text, max_excerpt_chars) if user_messages else None
    created_at = _timestamp_to_date(conversation.get("create_time"))
    updated_at = _timestamp_to_date(conversation.get("update_time"))

    metadata: dict[str, str | int | None] = {
        "source_file": source_file,
        "conversation_id": conversation_id,
        "project_id": _string_or_none(conversation.get("conversation_template_id")),
        "message_count": len(visible_messages),
        "user_message_count": len(user_messages),
        "assistant_message_count": len(assistant_messages),
        "model": _string_or_none(conversation.get("default_model_slug")),
        "first_user_excerpt": first_user_excerpt,
        "last_user_excerpt": last_user_excerpt,
    }

    item = TriageItem(
        source_id=f"chatgpt:{conversation_id}",
        source_kind="chatgpt",
        title=title,
        path=f"{source_file}#{conversation_id}",
        created_at=created_at,
        updated_at=updated_at,
        size_bytes=None,
        word_count=word_count,
        summary_hint=first_user_excerpt,
        tags=[],
        category_labels=[],
        suggested_decision="extract-insights" if word_count >= 250 else None,
        metadata=metadata,
    )
    return item, len(visible_messages), len(user_messages)


def _messages(conversation: dict[str, Any]) -> list[_Message]:
    mapping = conversation.get("mapping")
    if not isinstance(mapping, dict):
        return []

    messages: list[_Message] = []
    for node in mapping.values():
        if not isinstance(node, dict):
            continue
        message = node.get("message")
        if not isinstance(message, dict):
            continue
        role = ((message.get("author") or {}).get("role") or "").strip()
        text = _content_text(message.get("content"))
        created_at = message.get("create_time")
        messages.append(
            _Message(
                role=role,
                text=text,
                created_at=created_at if isinstance(created_at, (int, float)) else None,
            )
        )
    return sorted(messages, key=lambda message: (message.created_at is None, message.created_at or 0))


def _content_text(content: object) -> str:
    if not isinstance(content, dict):
        return ""
    content_type = content.get("content_type")
    if content_type not in {"text", "multimodal_text"}:
        return ""

    parts = content.get("parts")
    if not isinstance(parts, list):
        return ""

    strings: list[str] = []
    for part in parts:
        if isinstance(part, str):
            strings.append(part)
        elif isinstance(part, dict):
            text = part.get("text")
            if isinstance(text, str):
                strings.append(text)
    return _clean_text("\n".join(strings))


def _clean_title(value: object) -> str:
    title = _clean_text(value if isinstance(value, str) else "")
    return title or "Untitled conversation"


def _clean_text(value: str) -> str:
    return _WHITESPACE_RE.sub(" ", value).strip()


def _excerpt(value: str, max_chars: int) -> str:
    text = _clean_text(value)
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def _timestamp_to_date(value: object) -> str | None:
    if not isinstance(value, (int, float)):
        return None
    return datetime.fromtimestamp(value).date().isoformat()


def _string_or_none(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _relative_to_export(path: Path, export_path: Path) -> str:
    if export_path.is_file():
        return path.name
    return path.relative_to(export_path).as_posix()


def _is_untitled(title: str) -> bool:
    return title.strip().casefold() in {"", "untitled", "untitled conversation", "new chat"}
