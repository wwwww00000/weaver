from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from weaver.cli import app
from weaver.triage.obsidian import scan_obsidian_vaults, sort_triage_items
from weaver.triage.render import render_obsidian_triage, write_manifest_csv
from weaver.triage.schema import SortMode


def test_scan_obsidian_vault_detects_notes_tags_and_ignored_dirs(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "Projects").mkdir(parents=True)
    (vault / ".obsidian").mkdir()
    (vault / "attachments").mkdir()
    (vault / "daily").mkdir()
    (vault / "weekly").mkdir()
    (vault / "Projects" / "Foo.md").write_text(
        "\n".join(
            [
                "---",
                "tags: [project, idea]",
                "---",
                "# Foo Project",
                "",
                "This note has durable content and an inline #research/tag.",
            ]
        ),
        encoding="utf-8",
    )
    (vault / ".obsidian" / "Ignored.md").write_text("# ignored", encoding="utf-8")
    (vault / "attachments" / "Asset Note.md").write_text("# ignored asset", encoding="utf-8")
    (vault / "daily" / "2026-06-21.md").write_text("# ignored daily", encoding="utf-8")
    (vault / "weekly" / "2026-W25.md").write_text("# ignored weekly", encoding="utf-8")

    items, summary = scan_obsidian_vaults([vault])

    assert summary.total_markdown_files == 1
    assert len(items) == 1
    assert items[0].source_id == "obsidian:projects-foo"
    assert items[0].title == "Foo Project"
    assert items[0].path == "Projects/Foo.md"
    assert items[0].tags == ["project", "idea", "research/tag"]
    assert "daily" in summary.ignored_dirs
    assert "weekly" in summary.ignored_dirs


def test_scan_obsidian_vault_can_include_periodic_notes(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    (vault / "daily").mkdir(parents=True)
    (vault / "daily" / "2026-06-21.md").write_text("# Daily Note", encoding="utf-8")

    items, _summary = scan_obsidian_vaults([vault], include_periodic=True)

    assert [item.path for item in items] == ["daily/2026-06-21.md"]


def test_render_and_manifest_include_stable_item_markers(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Tiny.md").write_text("# Tiny\n", encoding="utf-8")
    items, summary = scan_obsidian_vaults([vault])
    items = sort_triage_items(items, SortMode.PATH)

    markdown = render_obsidian_triage(items, summary)
    manifest = tmp_path / "manifest.csv"
    write_manifest_csv(manifest, items)

    assert "<!-- triage-item: obsidian:tiny -->" in markdown
    assert "Category labels:" in markdown
    assert "- [ ] include-later" in markdown
    manifest_text = manifest.read_text(encoding="utf-8")
    assert "source_id,source_kind,title,path" in manifest_text
    assert "category_labels" in manifest_text


def test_scan_obsidian_vault_reads_yaml_frontmatter_tag_list(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Yaml.md").write_text(
        "\n".join(
            [
                "---",
                "tags:",
                "  - research",
                "  - '#machine-learning'",
                "---",
                "# YAML",
            ]
        ),
        encoding="utf-8",
    )

    items, _summary = scan_obsidian_vaults([vault])

    assert items[0].tags == ["research", "machine-learning"]


def test_cli_writes_obsidian_triage_and_manifest(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()
    (vault / "Note.md").write_text("# Note\nSome useful words for triage.", encoding="utf-8")
    out = tmp_path / "ops" / "triage" / "obsidian.md"
    manifest = tmp_path / "ops" / "manifests" / "obsidian.csv"

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "obsidian",
            str(vault),
            "--out",
            str(out),
            "--manifest",
            str(manifest),
        ],
    )

    assert result.exit_code == 0
    assert "Obsidian Vault Triage" in out.read_text(encoding="utf-8")
    assert "obsidian:note" in manifest.read_text(encoding="utf-8")


def test_cli_uses_default_obsidian_vault_when_unspecified(
    tmp_path: Path, monkeypatch
) -> None:
    vault = tmp_path / "default-vault"
    vault.mkdir()
    (vault / "Default.md").write_text("# Default", encoding="utf-8")
    out = tmp_path / "obsidian.md"
    manifest = tmp_path / "obsidian.csv"
    monkeypatch.setattr("weaver.cli.DEFAULT_OBSIDIAN_VAULT", vault)

    result = CliRunner().invoke(
        app,
        [
            "triage",
            "obsidian",
            "--out",
            str(out),
            "--manifest",
            str(manifest),
        ],
    )

    assert result.exit_code == 0
    assert "obsidian:default" in out.read_text(encoding="utf-8")
