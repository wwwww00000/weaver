from __future__ import annotations

from pathlib import Path

import yaml
from typer.testing import CliRunner

from weaver.cli import app
from weaver.inventory import build_source_inventory, render_inventory_qmd


def test_build_source_inventory_infers_projects_and_normalizes_categories(tmp_path: Path) -> None:
    artifact_dirs, project_glossary, chatgpt_glossary = _sample_inventory_inputs(tmp_path)

    inventory = build_source_inventory(
        artifact_dirs,
        project_glossary_path=project_glossary,
        chatgpt_project_glossary_path=chatgpt_glossary,
    )

    by_id = {record.source_id: record for record in inventory.records}
    assert by_id["obsidian:p12n-signals"].project_labels == ("p12n",)
    assert by_id["obsidian:p12n-signals"].normalized_category_labels == ("quant",)
    assert by_id["chatgpt:abc"].project_labels == ("genesis",)
    assert by_id["chatgpt:abc"].chatgpt_project_name == "agentic-ai"
    assert by_id["chatgpt:abc"].normalized_category_labels == ("cognitive",)
    assert by_id["chatgpt:def"].project_labels == ("genesis",)
    assert by_id["chatgpt:def"].normalized_category_labels == ()


def test_render_inventory_qmd_includes_overviews_and_attention_queue(tmp_path: Path) -> None:
    artifact_dirs, project_glossary, chatgpt_glossary = _sample_inventory_inputs(tmp_path)
    inventory = build_source_inventory(
        artifact_dirs,
        project_glossary_path=project_glossary,
        chatgpt_project_glossary_path=chatgpt_glossary,
    )

    rendered = render_inventory_qmd(inventory, output_path=tmp_path / "source-inventory.qmd")

    assert "## Project Overview" in rendered
    assert "## Category Overview" in rendered
    assert "## Candidate Synthesis Bundles" in rendered
    assert "## Unassigned Topic Hints" in rendered
    assert "genesis/cognitive" in rendered
    assert "| quantc | quant | 1 |" in rendered
    assert "## Attention Queue" in rendered
    assert "Uncategorized Genesis Note" in rendered


def test_cli_cluster_qmd_writes_inventory_and_manifest(tmp_path: Path) -> None:
    artifact_dirs, project_glossary, chatgpt_glossary = _sample_inventory_inputs(tmp_path)
    out = tmp_path / "clusters" / "source-inventory.qmd"
    manifest = tmp_path / "clusters" / "manifest.csv"

    result = CliRunner().invoke(
        app,
        [
            "cluster",
            "qmd",
            "--artifact-dir",
            str(artifact_dirs[0]),
            "--artifact-dir",
            str(artifact_dirs[1]),
            "--project-glossary",
            str(project_glossary),
            "--chatgpt-project-glossary",
            str(chatgpt_glossary),
            "--out",
            str(out),
            "--manifest",
            str(manifest),
        ],
    )

    assert result.exit_code == 0
    assert "Wrote 3 artifacts" in result.stdout
    assert out.exists()
    assert manifest.exists()
    manifest_text = manifest.read_text(encoding="utf-8")
    assert "synthesis_bundles" in manifest_text
    assert "chatgpt:abc" in manifest_text


def _sample_inventory_inputs(tmp_path: Path) -> tuple[list[Path], Path, Path]:
    obsidian_dir = tmp_path / "artifacts" / "obsidian"
    chatgpt_dir = tmp_path / "artifacts" / "chatgpt"
    obsidian_dir.mkdir(parents=True)
    chatgpt_dir.mkdir(parents=True)

    project_glossary = tmp_path / "project-glossary.yaml"
    project_glossary.write_text(
        yaml.safe_dump(
            {
                "projects": {
                    "p12n": {"status": "active", "description": "Trading ML."},
                    "genesis": {"status": "active", "description": "Building and AI."},
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    chatgpt_glossary = tmp_path / "chatgpt-project-glossary.yaml"
    chatgpt_glossary.write_text(
        yaml.safe_dump(
            {
                "chatgpt_projects": {
                    "g-p-agentic": {
                        "inferred_name": "agentic-ai",
                        "project_labels": ["genesis"],
                        "confidence": "high",
                    }
                }
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )

    _write_artifact(
        obsidian_dir / "p12n-signals.md",
        {
            "source_id": "obsidian:p12n-signals",
            "source_kind": "obsidian",
            "decision": "include",
            "title": "signals",
            "original_path": "p12n/signals.md",
            "category_labels": ["quantc"],
            "source_tags": [],
            "triage_comments": None,
        },
    )
    _write_artifact(
        chatgpt_dir / "abc.md",
        {
            "source_id": "chatgpt:abc",
            "source_kind": "chatgpt",
            "decision": "extract-insights",
            "title": "Agentic Awareness Chat",
            "project_id": "g-p-agentic",
            "transcript_path": "raw/chatgpt/transcripts/abc.md",
            "category_labels": ["cogntive"],
            "triage_comments": None,
        },
    )
    _write_artifact(
        chatgpt_dir / "def.md",
        {
            "source_id": "chatgpt:def",
            "source_kind": "chatgpt",
            "decision": "include",
            "title": "Uncategorized Genesis Note",
            "project_id": None,
            "transcript_path": "raw/chatgpt/transcripts/def.md",
            "category_labels": [],
            "triage_comments": "genesis",
        },
    )
    return [obsidian_dir, chatgpt_dir], project_glossary, chatgpt_glossary


def _write_artifact(path: Path, frontmatter: dict[str, object]) -> None:
    path.write_text(
        "---\n"
        + yaml.safe_dump(frontmatter, sort_keys=False).strip()
        + "\n---\n\n"
        + f"# {frontmatter['title']}\n",
        encoding="utf-8",
    )
