from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from weaver.cli import app
from weaver.triage.chatgpt import scan_chatgpt_export, sort_chatgpt_items
from weaver.triage.render import render_chatgpt_triage, write_manifest_csv
from weaver.triage.schema import ChatGPTSortMode


def test_scan_chatgpt_export_reads_sharded_conversations(tmp_path: Path) -> None:
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations-000.json").write_text(
        json.dumps([_conversation("abc", "Useful Chat", "How should I organize notes?")]),
        encoding="utf-8",
    )

    items, summary = scan_chatgpt_export(export, max_excerpt_chars=100)

    assert summary.conversation_files == 1
    assert summary.total_conversations == 1
    assert summary.total_user_messages == 1
    assert items[0].source_id == "chatgpt:abc"
    assert items[0].title == "Useful Chat"
    assert items[0].path == "conversations-000.json#abc"
    assert items[0].metadata["project_id"] == "project-123"
    assert items[0].metadata["first_user_excerpt"] == "How should I organize notes?"


def test_render_chatgpt_triage_contains_excerpts_and_decisions(tmp_path: Path) -> None:
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations.json").write_text(
        json.dumps([_conversation("abc", "Useful Chat", "First prompt", "Last prompt")]),
        encoding="utf-8",
    )
    items, summary = scan_chatgpt_export(export)
    items = sort_chatgpt_items(items, ChatGPTSortMode.UPDATED_DESC)
    markdown = render_chatgpt_triage(items, summary)
    manifest = tmp_path / "chatgpt.csv"
    write_manifest_csv(manifest, items)

    assert "# ChatGPT Conversation Triage" in markdown
    assert "<!-- triage-item: chatgpt:abc -->" in markdown
    assert "First user message:" in markdown
    assert "Last user message:" in markdown
    assert "- project_id: project-123" in markdown
    assert "- [ ] extract-insights" in markdown
    assert "chatgpt:abc" in manifest.read_text(encoding="utf-8")


def test_cli_writes_chatgpt_triage_and_manifest(tmp_path: Path) -> None:
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations-000.json").write_text(
        json.dumps([_conversation("abc", "Useful Chat", "How should I organize notes?")]),
        encoding="utf-8",
    )
    out = tmp_path / "triage" / "chatgpt.md"
    manifest = tmp_path / "manifests" / "chatgpt.csv"

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "chatgpt",
            str(export),
            "--out",
            str(out),
            "--manifest",
            str(manifest),
        ],
    )

    assert result.exit_code == 0
    assert "Wrote 1 conversations" in result.stdout
    assert "ChatGPT Conversation Triage" in out.read_text(encoding="utf-8")
    assert "chatgpt:abc" in manifest.read_text(encoding="utf-8")


def test_cli_writes_split_chatgpt_triage(tmp_path: Path) -> None:
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations-000.json").write_text(
        json.dumps(
            [
                _conversation("abc", "Useful Chat", "How should I organize notes?"),
                _conversation("def", "Second Chat", "What should I do next?"),
            ]
        ),
        encoding="utf-8",
    )
    out = tmp_path / "triage" / "chatgpt.md"
    manifest = tmp_path / "manifests" / "chatgpt.csv"

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "chatgpt",
            str(export),
            "--out",
            str(out),
            "--manifest",
            str(manifest),
            "--split-size",
            "1",
        ],
    )

    assert result.exit_code == 0
    assert "across 2 parts" in result.stdout
    assert "part-001.md" in out.read_text(encoding="utf-8")
    assert (tmp_path / "triage" / "chatgpt" / "part-001.md").exists()
    assert (tmp_path / "triage" / "chatgpt" / "part-002.md").exists()


def _conversation(
    conversation_id: str,
    title: str,
    first_user_message: str,
    last_user_message: str | None = None,
) -> dict[str, object]:
    messages = [
        ("root", "assistant", "Welcome", 1.0),
        ("user-1", "user", first_user_message, 2.0),
        ("assistant-1", "assistant", "A useful answer.", 3.0),
    ]
    if last_user_message is not None:
        messages.append(("user-2", "user", last_user_message, 4.0))

    mapping = {
        message_id: {
            "id": message_id,
            "parent": None,
            "message": {
                "id": message_id,
                "author": {"role": role},
                "create_time": created_at,
                "content": {"content_type": "text", "parts": [text]},
            },
        }
        for message_id, role, text, created_at in messages
    }
    return {
        "id": conversation_id,
        "conversation_id": conversation_id,
        "title": title,
        "create_time": 1.0,
        "update_time": 4.0,
        "default_model_slug": "gpt-test",
        "conversation_template_id": "project-123",
        "mapping": mapping,
    }
