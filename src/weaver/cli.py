from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Annotated

import typer

from weaver import __version__
from weaver.inventory import (
    build_source_inventory,
    write_inventory_manifest_csv,
    write_inventory_qmd,
)
from weaver.triage.apply import apply_triage_document, parse_decisions
from weaver.triage.chatgpt_apply import apply_chatgpt_triage
from weaver.triage.chatgpt import scan_chatgpt_export, sort_chatgpt_items
from weaver.triage.obsidian import (
    scan_markdown_sources,
    scan_obsidian_vaults,
    sort_triage_items,
)
from weaver.triage.render import (
    render_chatgpt_split_index,
    render_chatgpt_triage,
    render_notes_triage,
    render_obsidian_triage,
    write_manifest_csv,
)
from weaver.triage.schema import ChatGPTSortMode, SortMode

DEFAULT_OBSIDIAN_VAULT = Path("/mnt/c/Users/limwe/Documents/obsidian")
DEFAULT_CHATGPT_EXPORT = Path("raw/exports/chatgpt/2026-06-23")
DEFAULT_NOTES_INBOX = Path("notes/inbox")

app = typer.Typer(
    no_args_is_help=True,
    help="Deterministic tooling for triaging personal knowledge sources.",
)
triage_app = typer.Typer(no_args_is_help=True, help="Create human triage documents.")
cluster_app = typer.Typer(
    no_args_is_help=True,
    help="Build deterministic source inventory workbenches.",
)
app.add_typer(triage_app, name="triage")
app.add_typer(cluster_app, name="cluster")


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option("--version", help="Show the Weaver version and exit."),
    ] = False,
) -> None:
    if version:
        typer.echo(__version__)
        raise typer.Exit()


@triage_app.command("obsidian")
def triage_obsidian(
    vault_paths: Annotated[
        list[Path] | None,
        typer.Argument(
            exists=False,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help=(
                "One or more Obsidian vault directories to scan. "
                f"Defaults to {DEFAULT_OBSIDIAN_VAULT}."
            ),
        ),
    ] = None,
    out: Annotated[
        Path,
        typer.Option(
            "--out",
            "-o",
            dir_okay=False,
            writable=True,
            help="Markdown triage document to write.",
        ),
    ] = Path("ops/triage/obsidian.md"),
    manifest: Annotated[
        Path,
        typer.Option(
            "--manifest",
            "-m",
            dir_okay=False,
            writable=True,
            help="CSV manifest to write alongside the triage document.",
        ),
    ] = Path("ops/manifests/obsidian.csv"),
    sort: Annotated[
        SortMode,
        typer.Option("--sort", help="Ordering for notes in the triage document."),
    ] = SortMode.PATH,
    limit: Annotated[
        int | None,
        typer.Option("--limit", min=1, help="Only render the first N notes after sorting."),
    ] = None,
    include_assets: Annotated[
        bool,
        typer.Option(
            "--include-assets",
            help="Include common asset directories such as assets/ and attachments/.",
        ),
    ] = False,
    include_periodic: Annotated[
        bool,
        typer.Option(
            "--include-periodic",
            help="Include periodic note directories such as daily/ and weekly/.",
        ),
    ] = False,
) -> None:
    """Create an editable triage document for Markdown notes in Obsidian vaults."""

    resolved_vault_paths = vault_paths or [DEFAULT_OBSIDIAN_VAULT]
    for vault_path in resolved_vault_paths:
        if not vault_path.is_dir():
            raise typer.BadParameter(f"Obsidian vault does not exist: {vault_path}")

    items, summary = scan_obsidian_vaults(
        resolved_vault_paths,
        include_assets=include_assets,
        include_periodic=include_periodic,
    )
    items = sort_triage_items(items, sort)
    if limit is not None:
        items = items[:limit]

    out.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)

    out.write_text(render_obsidian_triage(items, summary), encoding="utf-8")
    write_manifest_csv(manifest, items)

    typer.echo(f"Wrote {len(items)} notes to {out}")
    typer.echo(f"Wrote manifest to {manifest}")


@triage_app.command("notes")
def triage_notes(
    note_paths: Annotated[
        list[Path] | None,
        typer.Argument(
            exists=False,
            file_okay=True,
            dir_okay=True,
            readable=True,
            resolve_path=False,
            help=(
                "Markdown files or directories to scan, relative to --source-root "
                f"unless absolute. Defaults to scanning {DEFAULT_NOTES_INBOX}."
            ),
        ),
    ] = None,
    source_root: Annotated[
        Path,
        typer.Option(
            "--source-root",
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="Root directory containing Markdown notes to triage.",
        ),
    ] = DEFAULT_NOTES_INBOX,
    out: Annotated[
        Path,
        typer.Option(
            "--out",
            "-o",
            dir_okay=False,
            writable=True,
            help="Markdown triage document to write.",
        ),
    ] = Path("ops/triage/notes.md"),
    manifest: Annotated[
        Path,
        typer.Option(
            "--manifest",
            "-m",
            dir_okay=False,
            writable=True,
            help="CSV manifest to write alongside the triage document.",
        ),
    ] = Path("ops/manifests/notes.csv"),
    sort: Annotated[
        SortMode,
        typer.Option("--sort", help="Ordering for notes in the triage document."),
    ] = SortMode.MODIFIED_DESC,
    limit: Annotated[
        int | None,
        typer.Option("--limit", min=1, help="Only render the first N notes after sorting."),
    ] = None,
    include_assets: Annotated[
        bool,
        typer.Option(
            "--include-assets",
            help="Include common asset directories such as assets/ and attachments/.",
        ),
    ] = False,
    include_periodic: Annotated[
        bool,
        typer.Option(
            "--include-periodic",
            help="Include periodic note directories such as daily/ and weekly/.",
        ),
    ] = False,
) -> None:
    """Create an editable triage document for repo-local or arbitrary Markdown notes."""

    if not source_root.is_dir():
        raise typer.BadParameter(f"Markdown source root does not exist: {source_root}")

    try:
        items, summary = scan_markdown_sources(
            source_root,
            note_paths,
            source_kind="notes",
            include_assets=include_assets,
            include_periodic=include_periodic,
        )
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        raise typer.BadParameter(str(exc)) from exc

    items = sort_triage_items(items, sort)
    if limit is not None:
        items = items[:limit]

    out.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)

    out.write_text(render_notes_triage(items, summary), encoding="utf-8")
    write_manifest_csv(manifest, items)

    typer.echo(f"Wrote {len(items)} notes to {out}")
    typer.echo(f"Wrote manifest to {manifest}")


@triage_app.command("chatgpt")
def triage_chatgpt(
    export_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
            help="ChatGPT export ZIP, extracted directory, or conversation JSON file.",
        ),
    ],
    out: Annotated[
        Path,
        typer.Option(
            "--out",
            "-o",
            dir_okay=False,
            writable=True,
            help="Markdown triage document to write.",
        ),
    ] = Path("ops/triage/chatgpt.md"),
    manifest: Annotated[
        Path,
        typer.Option(
            "--manifest",
            "-m",
            dir_okay=False,
            writable=True,
            help="CSV manifest to write alongside the triage document.",
        ),
    ] = Path("ops/manifests/chatgpt.csv"),
    sort: Annotated[
        ChatGPTSortMode,
        typer.Option("--sort", help="Ordering for conversations in the triage document."),
    ] = ChatGPTSortMode.UPDATED_DESC,
    limit: Annotated[
        int | None,
        typer.Option("--limit", min=1, help="Only render the first N conversations after sorting."),
    ] = None,
    max_excerpt_chars: Annotated[
        int,
        typer.Option(
            "--max-excerpt-chars",
            min=80,
            help="Maximum characters to show for first and last user message excerpts.",
        ),
    ] = 500,
    split_size: Annotated[
        int | None,
        typer.Option(
            "--split-size",
            min=1,
            help="Write an index plus part files with at most N conversations each.",
        ),
    ] = None,
    split_dir: Annotated[
        Path | None,
        typer.Option(
            "--split-dir",
            file_okay=False,
            dir_okay=True,
            writable=True,
            help="Directory for split part files. Defaults to OUT without the .md suffix.",
        ),
    ] = None,
) -> None:
    """Create an editable triage document for ChatGPT conversations."""

    items, summary = scan_chatgpt_export(export_path, max_excerpt_chars=max_excerpt_chars)
    items = sort_chatgpt_items(items, sort)
    if limit is not None:
        items = items[:limit]

    out.parent.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)

    if split_size is None:
        out.write_text(render_chatgpt_triage(items, summary), encoding="utf-8")
        typer.echo(f"Wrote {len(items)} conversations to {out}")
    else:
        resolved_split_dir = split_dir or out.with_suffix("")
        resolved_split_dir.mkdir(parents=True, exist_ok=True)
        parts: list[tuple[Path, int, int]] = []
        for index, start in enumerate(range(0, len(items), split_size), start=1):
            end = min(start + split_size, len(items))
            part_items = items[start:end]
            part_path = resolved_split_dir / f"part-{index:03d}.md"
            part_path.write_text(
                render_chatgpt_triage(
                    part_items,
                    summary,
                    title=f"ChatGPT Conversation Triage Part {index:03d}",
                ),
                encoding="utf-8",
            )
            parts.append((part_path.relative_to(out.parent), start + 1, end))
        out.write_text(render_chatgpt_split_index(summary=summary, parts=parts), encoding="utf-8")
        typer.echo(f"Wrote {len(items)} conversations across {len(parts)} parts under {resolved_split_dir}")
        typer.echo(f"Wrote split index to {out}")
    write_manifest_csv(manifest, items)

    typer.echo(f"Wrote manifest to {manifest}")


@triage_app.command("apply")
def triage_apply(
    triage_doc: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            help="Completed triage Markdown document to apply.",
        ),
    ],
    source_root: Annotated[
        Path,
        typer.Option(
            "--source-root",
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="Root directory containing original Obsidian notes.",
        ),
    ] = DEFAULT_OBSIDIAN_VAULT,
    raw_out: Annotated[
        Path,
        typer.Option(
            "--raw-out",
            file_okay=False,
            dir_okay=True,
            writable=True,
            help="Directory where selected source notes are copied.",
        ),
    ] = Path("raw/obsidian"),
    artifact_out: Annotated[
        Path,
        typer.Option(
            "--artifact-out",
            file_okay=False,
            dir_okay=True,
            writable=True,
            help="Directory where per-note intermediate artifacts are written.",
        ),
    ] = Path("ops/artifacts/obsidian"),
    decisions: Annotated[
        str,
        typer.Option(
            "--decisions",
            help="Comma-separated decisions to copy and generate artifacts for.",
        ),
    ] = "include,extract-insights",
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Validate and summarize without writing files."),
    ] = False,
) -> None:
    """Apply completed triage decisions to selected source notes."""

    selected_decisions = parse_decisions(decisions)
    summary = apply_triage_document(
        triage_doc,
        source_root=source_root,
        raw_out=raw_out,
        artifact_out=artifact_out,
        selected_decisions=selected_decisions,
        dry_run=dry_run,
    )

    action = "Would apply" if dry_run else "Applied"
    typer.echo(
        f"{action} {summary.selected_items} of {summary.total_items} triage items "
        f"for decisions: {', '.join(summary.selected_decisions)}"
    )
    typer.echo(f"Copied notes: {summary.copied_notes}")
    typer.echo(f"Wrote artifacts: {summary.written_artifacts}")
    typer.echo(f"Skipped by decision: {summary.skipped_items}")
    if summary.index_path is not None:
        typer.echo(f"Artifact index: {summary.index_path}")


@triage_app.command("apply-notes")
def triage_apply_notes(
    triage_doc: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            help="Completed Markdown notes triage document to apply.",
        ),
    ],
    source_root: Annotated[
        Path,
        typer.Option(
            "--source-root",
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="Root directory containing original Markdown notes.",
        ),
    ] = DEFAULT_NOTES_INBOX,
    raw_out: Annotated[
        Path,
        typer.Option(
            "--raw-out",
            file_okay=False,
            dir_okay=True,
            writable=True,
            help="Directory where selected source notes are copied.",
        ),
    ] = Path("raw/notes"),
    artifact_out: Annotated[
        Path,
        typer.Option(
            "--artifact-out",
            file_okay=False,
            dir_okay=True,
            writable=True,
            help="Directory where per-note intermediate artifacts are written.",
        ),
    ] = Path("ops/artifacts/notes"),
    decisions: Annotated[
        str,
        typer.Option(
            "--decisions",
            help="Comma-separated decisions to copy and generate artifacts for.",
        ),
    ] = "include,extract-insights",
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Validate and summarize without writing files."),
    ] = False,
) -> None:
    """Apply completed Markdown notes triage decisions to selected notes."""

    selected_decisions = parse_decisions(decisions)
    summary = apply_triage_document(
        triage_doc,
        source_root=source_root,
        raw_out=raw_out,
        artifact_out=artifact_out,
        selected_decisions=selected_decisions,
        index_title="Markdown Notes Applied Triage",
        dry_run=dry_run,
    )

    action = "Would apply" if dry_run else "Applied"
    typer.echo(
        f"{action} {summary.selected_items} of {summary.total_items} triage items "
        f"for decisions: {', '.join(summary.selected_decisions)}"
    )
    typer.echo(f"Copied notes: {summary.copied_notes}")
    typer.echo(f"Wrote artifacts: {summary.written_artifacts}")
    typer.echo(f"Skipped by decision: {summary.skipped_items}")
    if summary.index_path is not None:
        typer.echo(f"Artifact index: {summary.index_path}")


@cluster_app.command("qmd")
def cluster_qmd(
    artifact_dirs: Annotated[
        list[Path] | None,
        typer.Option(
            "--artifact-dir",
            file_okay=False,
            dir_okay=True,
            readable=True,
            help="Applied artifact directory to include. May be passed multiple times.",
        ),
    ] = None,
    out: Annotated[
        Path | None,
        typer.Option(
            "--out",
            "-o",
            dir_okay=False,
            writable=True,
            help="QMD source inventory workbench to write.",
        ),
    ] = None,
    manifest: Annotated[
        Path | None,
        typer.Option(
            "--manifest",
            "-m",
            dir_okay=False,
            writable=True,
            help="CSV manifest to write for the same inventory.",
        ),
    ] = None,
    project_glossary: Annotated[
        Path,
        typer.Option(
            "--project-glossary",
            exists=True,
            readable=True,
            help="Project glossary used for deterministic project inference.",
        ),
    ] = Path("ops/context/project-glossary.yaml"),
    chatgpt_project_glossary: Annotated[
        Path,
        typer.Option(
            "--chatgpt-project-glossary",
            exists=True,
            readable=True,
            help="ChatGPT project ID glossary used for deterministic project inference.",
        ),
    ] = Path("ops/context/chatgpt-project-glossary.yaml"),
) -> None:
    """Generate a QMD source inventory from applied artifacts."""

    resolved_artifact_dirs = artifact_dirs or [
        Path("ops/artifacts/obsidian"),
        Path("ops/artifacts/notes"),
        Path("ops/artifacts/chatgpt"),
    ]
    today = Path(date.today().isoformat())
    resolved_out = out or Path("ops/clusters") / today / "source-inventory.qmd"
    resolved_manifest = manifest or resolved_out.with_name("manifest.csv")

    inventory = build_source_inventory(
        resolved_artifact_dirs,
        project_glossary_path=project_glossary,
        chatgpt_project_glossary_path=chatgpt_project_glossary,
    )
    write_inventory_qmd(inventory, resolved_out)
    write_inventory_manifest_csv(inventory, resolved_manifest)

    typer.echo(f"Wrote {len(inventory.records)} artifacts to {resolved_out}")
    typer.echo(f"Wrote manifest to {resolved_manifest}")


@triage_app.command("apply-chatgpt")
def triage_apply_chatgpt(
    triage_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            resolve_path=True,
            help="Completed ChatGPT triage Markdown file or split part directory.",
        ),
    ] = Path("ops/triage/chatgpt.md"),
    export_path: Annotated[
        Path,
        typer.Option(
            "--export-path",
            exists=True,
            readable=True,
            resolve_path=True,
            help="ChatGPT export ZIP, extracted directory, or conversation JSON file.",
        ),
    ] = DEFAULT_CHATGPT_EXPORT,
    raw_out: Annotated[
        Path,
        typer.Option(
            "--raw-out",
            file_okay=False,
            dir_okay=True,
            writable=True,
            help="Directory where selected ChatGPT conversations are copied.",
        ),
    ] = Path("raw/chatgpt"),
    artifact_out: Annotated[
        Path,
        typer.Option(
            "--artifact-out",
            file_okay=False,
            dir_okay=True,
            writable=True,
            help="Directory where per-conversation intermediate artifacts are written.",
        ),
    ] = Path("ops/artifacts/chatgpt"),
    decisions: Annotated[
        str,
        typer.Option(
            "--decisions",
            help="Comma-separated decisions to copy and generate artifacts for.",
        ),
    ] = "include,extract-insights",
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Validate and summarize without writing files."),
    ] = False,
) -> None:
    """Apply completed ChatGPT triage decisions to selected conversations."""

    selected_decisions = parse_decisions(decisions)
    summary = apply_chatgpt_triage(
        triage_path,
        export_path=export_path,
        raw_out=raw_out,
        artifact_out=artifact_out,
        selected_decisions=selected_decisions,
        dry_run=dry_run,
    )

    action = "Would apply" if dry_run else "Applied"
    typer.echo(
        f"{action} {summary.selected_items} of {summary.total_items} triage items "
        f"for decisions: {', '.join(summary.selected_decisions)}"
    )
    typer.echo(f"Copied conversations: {summary.copied_conversations}")
    typer.echo(f"Wrote transcripts: {summary.written_transcripts}")
    typer.echo(f"Wrote artifacts: {summary.written_artifacts}")
    typer.echo(f"Skipped by decision: {summary.skipped_items}")
    if summary.index_path is not None:
        typer.echo(f"Artifact index: {summary.index_path}")
