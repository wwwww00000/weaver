from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from weaver import __version__
from weaver.triage.apply import apply_triage_document, parse_decisions
from weaver.triage.obsidian import scan_obsidian_vaults, sort_triage_items
from weaver.triage.render import render_obsidian_triage, write_manifest_csv
from weaver.triage.schema import SortMode

DEFAULT_OBSIDIAN_VAULT = Path("/mnt/c/Users/limwe/Documents/obsidian")

app = typer.Typer(
    no_args_is_help=True,
    help="Deterministic tooling for triaging personal knowledge sources.",
)
triage_app = typer.Typer(no_args_is_help=True, help="Create human triage documents.")
app.add_typer(triage_app, name="triage")


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
