from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from weaver.cli import app
from weaver.triage.apply import apply_triage_document, parse_triage_document


def test_parse_triage_document_reads_decisions_labels_and_comments(tmp_path: Path) -> None:
    triage_doc = tmp_path / "triage.md"
    triage_doc.write_text(_triage_doc(), encoding="utf-8")

    items = parse_triage_document(triage_doc)

    assert len(items) == 2
    assert items[0].source_id == "obsidian:alpha"
    assert items[0].decision == "include"
    assert items[0].category_labels == ["research", "writing"]
    assert items[0].comments == "keep this one"
    assert items[1].decision == "skip"


def test_apply_triage_document_copies_selected_notes_and_writes_artifacts(
    tmp_path: Path,
) -> None:
    triage_doc = tmp_path / "triage.md"
    triage_doc.write_text(_triage_doc(), encoding="utf-8")
    source_root = tmp_path / "vault"
    source_root.mkdir()
    (source_root / "alpha.md").write_text("# Alpha\nUseful source.", encoding="utf-8")
    (source_root / "beta.md").write_text("# Beta\nSkipped source.", encoding="utf-8")
    raw_out = tmp_path / "raw" / "obsidian"
    artifact_out = tmp_path / "ops" / "artifacts" / "obsidian"

    summary = apply_triage_document(
        triage_doc,
        source_root=source_root,
        raw_out=raw_out,
        artifact_out=artifact_out,
        selected_decisions=("include", "extract-insights"),
    )

    assert summary.total_items == 2
    assert summary.selected_items == 1
    assert (raw_out / "alpha.md").read_text(encoding="utf-8") == "# Alpha\nUseful source."
    artifact = (artifact_out / "alpha.md").read_text(encoding="utf-8")
    assert "source_id: obsidian:alpha" in artifact
    assert "decision: include" in artifact
    assert "## Synthesis Notes" in artifact
    assert not (raw_out / "beta.md").exists()
    assert "Total selected notes: 1" in (artifact_out / "index.md").read_text(encoding="utf-8")


def test_cli_apply_writes_selected_artifacts(tmp_path: Path) -> None:
    triage_doc = tmp_path / "triage.md"
    triage_doc.write_text(_triage_doc(), encoding="utf-8")
    source_root = tmp_path / "vault"
    source_root.mkdir()
    (source_root / "alpha.md").write_text("# Alpha", encoding="utf-8")
    (source_root / "beta.md").write_text("# Beta", encoding="utf-8")
    raw_out = tmp_path / "raw"
    artifact_out = tmp_path / "artifacts"

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "apply",
            str(triage_doc),
            "--source-root",
            str(source_root),
            "--raw-out",
            str(raw_out),
            "--artifact-out",
            str(artifact_out),
        ],
    )

    assert result.exit_code == 0
    assert "Applied 1 of 2 triage items" in result.stdout
    assert (raw_out / "alpha.md").exists()
    assert (artifact_out / "alpha.md").exists()


def _triage_doc() -> str:
    return """# Obsidian Vault Triage

<!-- triage-item: obsidian:alpha -->
### 001. Alpha
- source_id: obsidian:alpha
- path: alpha.md
- tags: idea, source

Category labels:
> research, writing

Decision:
- [x] include
- [ ] extract-insights
- [ ] include-later
- [ ] skip
- [ ] sensitive / exclude

Comments:
> keep this one

<!-- triage-item: obsidian:beta -->
### 002. Beta
- source_id: obsidian:beta
- path: beta.md

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
