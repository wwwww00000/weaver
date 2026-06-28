from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from weaver.cli import app
from weaver.triage.obsidian import scan_markdown_sources


def test_scan_markdown_sources_uses_notes_source_kind_and_ignores_bulk_dirs(
    tmp_path: Path,
) -> None:
    source_root = tmp_path / "notes"
    (source_root / "projects").mkdir(parents=True)
    (source_root / "daily").mkdir()
    (source_root / "assets").mkdir()
    (source_root / "projects" / "Idea.md").write_text(
        "# New Project Idea\n\nThis is a durable note with a #genesis tag.",
        encoding="utf-8",
    )
    (source_root / "daily" / "2026-06-29.md").write_text("# Daily", encoding="utf-8")
    (source_root / "assets" / "Asset.md").write_text("# Asset", encoding="utf-8")

    items, summary = scan_markdown_sources(source_root)

    assert summary.total_markdown_files == 1
    assert items[0].source_id == "notes:projects-idea"
    assert items[0].source_kind == "notes"
    assert items[0].path == "projects/Idea.md"
    assert items[0].title == "New Project Idea"
    assert items[0].tags == ["genesis"]


def test_cli_notes_writes_triage_and_manifest_for_relative_paths(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    (source_root / "ideas").mkdir(parents=True)
    (source_root / "ideas" / "Project.md").write_text(
        "# Project\n\nSome useful words for triage.",
        encoding="utf-8",
    )
    out = tmp_path / "ops" / "triage" / "notes.md"
    manifest = tmp_path / "ops" / "manifests" / "notes.csv"

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "notes",
            "ideas",
            "--source-root",
            str(source_root),
            "--out",
            str(out),
            "--manifest",
            str(manifest),
        ],
    )

    assert result.exit_code == 0
    assert "Markdown Notes Triage" in out.read_text(encoding="utf-8")
    assert "notes:ideas-project" in manifest.read_text(encoding="utf-8")


def test_cli_apply_notes_writes_selected_artifacts(tmp_path: Path) -> None:
    source_root = tmp_path / "source"
    source_root.mkdir()
    (source_root / "alpha.md").write_text("# Alpha", encoding="utf-8")
    (source_root / "beta.md").write_text("# Beta", encoding="utf-8")
    triage_doc = tmp_path / "triage.md"
    triage_doc.write_text(_notes_triage_doc(), encoding="utf-8")
    raw_out = tmp_path / "raw" / "notes"
    artifact_out = tmp_path / "ops" / "artifacts" / "notes"

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "apply-notes",
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
    artifact = (artifact_out / "alpha.md").read_text(encoding="utf-8")
    assert "source_id: notes:alpha" in artifact
    assert "source_kind: notes" in artifact
    assert "Markdown Notes Applied Triage" in (artifact_out / "index.md").read_text(
        encoding="utf-8"
    )


def _notes_triage_doc() -> str:
    return """# Markdown Notes Triage

<!-- triage-item: notes:alpha -->
### 001. Alpha
- source_id: notes:alpha
- path: alpha.md

Category labels:
> idea

Decision:
- [x] include
- [ ] extract-insights
- [ ] include-later
- [ ] skip
- [ ] sensitive / exclude

Comments:
>

<!-- triage-item: notes:beta -->
### 002. Beta
- source_id: notes:beta
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
