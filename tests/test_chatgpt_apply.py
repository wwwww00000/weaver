from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from weaver.cli import app
from weaver.triage.chatgpt_apply import apply_chatgpt_triage, parse_chatgpt_triage_path


def test_parse_chatgpt_triage_path_reads_split_index_sibling_dir(tmp_path: Path) -> None:
    triage_index = tmp_path / "chatgpt.md"
    triage_dir = tmp_path / "chatgpt"
    triage_dir.mkdir()
    triage_index.write_text("# ChatGPT Conversation Triage\n", encoding="utf-8")
    (triage_dir / "part-001.md").write_text(_triage_doc(), encoding="utf-8")

    items = parse_chatgpt_triage_path(triage_index)

    assert len(items) == 2
    assert items[0].source_id == "chatgpt:abc"
    assert items[0].decision == "include"
    assert items[1].decision == "skip"


def test_apply_chatgpt_triage_writes_json_transcript_and_artifact(tmp_path: Path) -> None:
    triage_dir = tmp_path / "chatgpt"
    triage_dir.mkdir()
    (triage_dir / "part-001.md").write_text(_triage_doc(), encoding="utf-8")
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations-000.json").write_text(
        json.dumps(
            [
                _conversation("abc", "Useful Chat", "How should I organize notes?"),
                _conversation("def", "Skipped Chat", "Should this be skipped?"),
            ]
        ),
        encoding="utf-8",
    )
    raw_out = tmp_path / "raw" / "chatgpt"
    artifact_out = tmp_path / "ops" / "artifacts" / "chatgpt"

    summary = apply_chatgpt_triage(
        triage_dir,
        export_path=export,
        raw_out=raw_out,
        artifact_out=artifact_out,
        selected_decisions=("include", "extract-insights"),
    )

    assert summary.total_items == 2
    assert summary.selected_items == 1
    assert (raw_out / "json" / "abc.json").exists()
    transcript = (raw_out / "transcripts" / "abc.md").read_text(encoding="utf-8")
    assert "How should I organize notes?" in transcript
    artifact = (artifact_out / "abc.md").read_text(encoding="utf-8")
    assert "source_id: chatgpt:abc" in artifact
    assert "project_id: project-123" in artifact
    assert not (raw_out / "json" / "def.json").exists()
    assert "Total selected conversations: 1" in (artifact_out / "index.md").read_text(
        encoding="utf-8"
    )


def test_cli_apply_chatgpt_writes_selected_artifacts(tmp_path: Path) -> None:
    triage_dir = tmp_path / "chatgpt"
    triage_dir.mkdir()
    (triage_dir / "part-001.md").write_text(_triage_doc(), encoding="utf-8")
    export = tmp_path / "export"
    export.mkdir()
    (export / "conversations-000.json").write_text(
        json.dumps(
            [
                _conversation("abc", "Useful Chat", "How should I organize notes?"),
                _conversation("def", "Skipped Chat", "Should this be skipped?"),
            ]
        ),
        encoding="utf-8",
    )
    raw_out = tmp_path / "raw"
    artifact_out = tmp_path / "artifacts"

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "apply-chatgpt",
            str(triage_dir),
            "--export-path",
            str(export),
            "--raw-out",
            str(raw_out),
            "--artifact-out",
            str(artifact_out),
        ],
    )

    assert result.exit_code == 0
    assert "Applied 1 of 2 triage items" in result.stdout
    assert (raw_out / "json" / "abc.json").exists()
    assert (raw_out / "transcripts" / "abc.md").exists()
    assert (artifact_out / "abc.md").exists()


def _triage_doc() -> str:
    return """# ChatGPT Conversation Triage Part 001

<!-- triage-item: chatgpt:abc -->
### 001. Useful Chat
- source_id: chatgpt:abc
- path: conversations-000.json#abc
- source_file: conversations-000.json
- project_id: project-123

Category labels:
> research

Decision:
- [x] include
- [ ] extract-insights
- [ ] include-later
- [ ] skip
- [ ] sensitive / exclude

Comments:
> useful context

<!-- triage-item: chatgpt:def -->
### 002. Skipped Chat
- source_id: chatgpt:def
- path: conversations-000.json#def
- source_file: conversations-000.json

Category labels:
>

Decision:
- [ ] include
- [ ] extract-insights
- [ ] include-later
- [x] skip
- [ ] sensitive / exclude

Comments:
>
"""


def _conversation(conversation_id: str, title: str, user_message: str) -> dict[str, object]:
    return {
        "id": conversation_id,
        "conversation_id": conversation_id,
        "title": title,
        "create_time": 1.0,
        "update_time": 4.0,
        "conversation_template_id": "project-123",
        "mapping": {
            "user": {
                "id": "user",
                "parent": None,
                "message": {
                    "id": "user",
                    "author": {"role": "user"},
                    "create_time": 2.0,
                    "content": {"content_type": "text", "parts": [user_message]},
                },
            },
            "assistant": {
                "id": "assistant",
                "parent": "user",
                "message": {
                    "id": "assistant",
                    "author": {"role": "assistant"},
                    "create_time": 3.0,
                    "content": {"content_type": "text", "parts": ["A useful answer."]},
                },
            },
        },
    }
