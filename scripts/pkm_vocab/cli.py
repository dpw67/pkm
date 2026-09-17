"""Command line entry point.

    python -m pkm_vocab check <export.ttl>    validate, report
    python -m pkm_vocab build <export.ttl>    validate, transform, publish
    python -m pkm_vocab notes <published.ttl> --out <dir>   Obsidian stubs
    python -m pkm_vocab hub <published.ttl> --out <note.md>  Obsidian hub blocks
    python -m pkm_vocab review <export.ttl>   family-grouped reading sheet
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from . import load, wrap
from .checks import ERROR, INFO, WARN, Report, check
from .notes import HUB_BLOCKS, write_hub, write_notes
from .review import write_review

LEVELS = (ERROR, WARN, INFO)

LEGEND = {
    ERROR: "violates a SKOS integrity condition or references something that does not exist",
    WARN: "structurally wrong or unpublishable as-is, but not a spec violation",
    INFO: "editorial completeness; nothing is broken",
}


def _render_text(report: Report) -> str:
    out: list[str] = []
    vocab = report.vocab
    out.append(f"PKM vocabulary check — {vocab.path}")
    out.append(f"scheme: {vocab.scheme or '(none found)'}")
    out.append(f"base:   {vocab.base or '(none found)'}")
    out.append("")

    width = max(len(k) for k in report.stats)
    for key, value in report.stats.items():
        out.append(f"  {key:<{width}}  {value}")
    out.append("")

    counts = {level: report.count(level) for level in LEVELS}
    out.append(
        "  ".join(f"{counts[level]} {level.lower()}" for level in LEVELS)
        or "no findings"
    )

    for level in LEVELS:
        items = [f for f in report.findings if f.level == level]
        if not items:
            continue
        out.append("")
        out.append(f"{level} — {LEGEND[level]}")
        out.append("=" * 76)
        grouped: dict[str, list] = defaultdict(list)
        for finding in items:
            grouped[finding.code].append(finding)
        for code, group in grouped.items():
            out.append("")
            out.append(f"[{code}] ({len(group)})")
            for finding in group:
                prefix = f"  {finding.subject}: " if finding.subject else "  "
                out.append(f"{prefix}{finding.message}")
    out.append("")
    return "\n".join(out)


def _render_markdown(report: Report) -> str:
    out: list[str] = []
    vocab = report.vocab
    out.append(f"# Vocabulary check — `{vocab.path.name}`")
    out.append("")
    out.append(f"- **Scheme:** `{vocab.scheme or '(none found)'}`")
    out.append(f"- **Base:** `{vocab.base or '(none found)'}`")
    counts = {level: report.count(level) for level in LEVELS}
    out.append(
        "- **Findings:** "
        + ", ".join(f"{counts[level]} {level.lower()}" for level in LEVELS)
    )
    out.append("")
    out.append("## Statistics")
    out.append("")
    out.append("| Metric | Count |")
    out.append("| --- | ---: |")
    for key, value in report.stats.items():
        out.append(f"| {key} | {value} |")

    for level in LEVELS:
        items = [f for f in report.findings if f.level == level]
        if not items:
            continue
        out.append("")
        out.append(f"## {level.title()} ({len(items)})")
        out.append("")
        out.append(f"_{LEGEND[level]}._")
        grouped: dict[str, list] = defaultdict(list)
        for finding in items:
            grouped[finding.code].append(finding)
        for code, group in grouped.items():
            out.append("")
            out.append(f"### `{code}` ({len(group)})")
            out.append("")
            for finding in group:
                subject = f"**`{finding.subject}`** — " if finding.subject else ""
                out.append(f"- [ ] {subject}{finding.message}")
    out.append("")
    return "\n".join(out)



def _build(args) -> int:
    """Validate, transform, then write every published artifact."""
    from .diagram import render_map
    from .guard import report_prose_delta
    from .pages import write_pages
    from .render import (BROWSE_DIR, render_agents, render_all_terms,
                         render_collections, render_hierarchy, render_resources,
                         render_search_index, render_vocab_index, splice)
    from .split import stale_term_files, write_all
    from .transform import publish

    vocab = load(args.source)
    report = check(vocab)
    if report.count(ERROR):
        print(_render_text(report))
        print("\nrefusing to build: fix the errors above", file=sys.stderr)
        return 1

    # Before anything is written: has prose moved since the last commit, and
    # was that intended? A re-export from the wrong SKOS Editor project once
    # reverted 33 literals and every other check passed. See guard.py.
    for line in report_prose_delta(vocab.graph, args.source, args.root):
        print(line, file=sys.stderr)

    published = publish(vocab)
    print(
        f"{args.source}: {len(vocab.graph)} triples -> {len(published)} published "
        f"({len(vocab.concepts())} concepts, {len(vocab.collections())} collections)",
        file=sys.stderr,
    )

    # Publishing an artifact that fails its own checker would be worse than
    # not publishing, so the transform is verified before anything is written.
    verified = check(wrap(published, args.source))
    if verified.count(ERROR):
        print(_render_text(verified))
        print("\nrefusing to build: the transform produced errors", file=sys.stderr)
        return 1
    for level in (WARN, INFO):
        if verified.count(level):
            print(f"  {verified.count(level)} {level.lower()} remain after transform",
                  file=sys.stderr)

    root = args.root
    browse = root / "vocab" / BROWSE_DIR
    # The vocabulary is four pages, not one: a landing page shaped like the
    # namespace front page, and one page per view under browse/. See render.py.
    targets = [
        (root / "vocab" / "index.md", render_vocab_index(vocab, published)),
        (browse / "hierarchy.md", render_hierarchy(vocab, published)),
        (browse / "collections.md", render_collections(vocab, published)),
        (browse / "all.md", render_all_terms(vocab, published)),
        (browse / "map.md", render_map(vocab, published)),
        (root / "resources" / "index.md", render_resources(vocab, published)),
        (root / "agents" / "index.md", render_agents(vocab, published)),
    ]
    # Written wholesale rather than spliced: it is JSON, there is no prose to
    # preserve, and it must stay free of front matter so Jekyll copies it
    # through as a static file instead of trying to render it.
    search = root / "vocab" / "search.json"
    index = render_search_index(vocab, published)

    if args.dry_run:
        names = {vocab.local_name(u) for u in [*vocab.concepts(), *vocab.collections()]}
        print(f"would write vocab/pkm-vocab.ttl, {len(names)} Turtle files and "
              f"{len(names)} term pages under vocab/terms/, agents/index.ttl, "
              f"resources/index.ttl", file=sys.stderr)
        for path, _ in targets:
            print(f"would splice {path.relative_to(root)}", file=sys.stderr)
        print(f"would write {search.relative_to(root)} "
              f"({len(names)} entries, {len(index)} bytes)", file=sys.stderr)
        return 0

    written = write_all(vocab, published, root)
    # Unlike the Turtle, term pages are only rewritten when their content
    # changes, so this counts what moved rather than what exists.
    pages = write_pages(vocab, published, root)
    for path, body in targets:
        written.append(splice(path, body))
    search.write_text(index + "\n", encoding="utf-8")
    written.append(search)
    print(f"wrote {len(written)} files, {len(pages)} term pages changed",
          file=sys.stderr)

    keep = {vocab.local_name(u) for u in [*vocab.concepts(), *vocab.collections()]}
    for stale in stale_term_files(root, keep):
        print(f"  stale: {stale.relative_to(root)} — no longer in the vocabulary; "
              "deprecate rather than delete if the URI was published", file=sys.stderr)
    return 0


def _notes(args) -> int:
    """Mirror the published vocabulary into an Obsidian vault as term stubs."""
    vocab = load(args.source)
    written, unchanged, pruned = write_notes(
        vocab, args.out, prune=not args.no_prune, dry_run=args.dry_run)

    verb = "would write" if args.dry_run else "wrote"
    print(f"{args.source}: {len(vocab.concepts())} concepts + "
          f"{len(vocab.collections())} collections", file=sys.stderr)
    print(f"  {verb} {written}, unchanged {unchanged} -> {args.out}", file=sys.stderr)
    for name in pruned:
        print(f"  {'would prune' if args.dry_run else 'pruned'}: {name} — "
              "no longer in the vocabulary", file=sys.stderr)
    return 0


def _hub(args) -> int:
    """Fill the generated blocks in the vault's hand-written vocabulary hub."""
    vocab = load(args.source)
    changed, missing = write_hub(vocab, args.out, dry_run=args.dry_run)

    if missing:
        # Reported rather than appended. A generated block appended to the end
        # of a hand-written page is in the wrong place and silently so, and the
        # hub's prose order is the point of keeping it hand-written.
        print(f"{args.out}: no markers for {', '.join(missing)}", file=sys.stderr)
        print("  The hub is hand-written. Paste each pair once, where that block "
              "belongs, then this fills them:", file=sys.stderr)
        for name in missing:
            print(f"    <!-- pkm:begin generated: {name} -->", file=sys.stderr)
            print(f"    <!-- pkm:end generated: {name} -->", file=sys.stderr)
        return 1

    print(f"{args.source}: {len(vocab.concepts())} concepts + "
          f"{len(vocab.collections())} collections", file=sys.stderr)
    if not changed:
        print(f"  unchanged -> {args.out}", file=sys.stderr)
    else:
        print(f"  {'would update' if args.dry_run else 'updated'} "
              f"{', '.join(HUB_BLOCKS)} -> {args.out}", file=sys.stderr)
    return 0


def _review(args) -> int:
    """Render the review sheet -- a reading aid, so it never fails a build."""
    vocab = load(args.source)
    out = write_review(vocab, args.out)
    print(f"{args.source}: {len(vocab.concepts())} concepts + "
          f"{len(vocab.collections())} collections", file=sys.stderr)
    print(f"  wrote {out}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pkm_vocab", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    checker = sub.add_parser("check", help="validate a SKOS export and print a report")
    checker.add_argument("source", type=Path, help="Turtle file to check")
    checker.add_argument(
        "--format", choices=("text", "markdown"), default="text",
        help="output format (default: text)",
    )
    checker.add_argument(
        "-o", "--output", type=Path,
        help="write the report to a file instead of stdout",
    )
    checker.add_argument(
        "--strict", action="store_true",
        help="exit non-zero on warnings as well as errors",
    )

    builder = sub.add_parser("build", help="generate the published artifacts")
    builder.add_argument("source", type=Path, help="SKOS Editor export to publish")
    builder.add_argument(
        "--root", type=Path, default=Path("."),
        help="repository root to write into (default: .)",
    )
    builder.add_argument(
        "--dry-run", action="store_true",
        help="list what would be written without writing it",
    )

    noter = sub.add_parser(
        "notes", help="generate Obsidian term stubs into a vault directory")
    noter.add_argument(
        "source", type=Path,
        help="published Turtle to mirror (vocab/pkm-vocab.ttl, not the export)")
    noter.add_argument(
        "--out", type=Path, required=True,
        help="vault directory to write stubs into; entirely generated")
    noter.add_argument(
        "--no-prune", action="store_true",
        help="keep stubs for terms no longer in the vocabulary")
    noter.add_argument(
        "--dry-run", action="store_true",
        help="report what would change without writing it",
    )

    hubber = sub.add_parser(
        "hub", help="fill the generated blocks in the Obsidian vocabulary hub")
    hubber.add_argument(
        "source", type=Path,
        help="published Turtle to read (vocab/pkm-vocab.ttl, not the export)")
    hubber.add_argument(
        "--out", type=Path, required=True,
        help="the vault's hub note; hand-written, with markers this fills")
    hubber.add_argument(
        "--dry-run", action="store_true",
        help="report whether it would change without writing it",
    )

    reviewer = sub.add_parser(
        "review", help="write a family-grouped reading sheet for human review")
    reviewer.add_argument("source", type=Path, help="Turtle file to review")
    reviewer.add_argument(
        "-o", "--out", type=Path, default=Path("reports/vocab-review.md"),
        help="where to write the sheet (default: reports/vocab-review.md)",
    )

    args = parser.parse_args(argv)

    if args.command == "build":
        return _build(args)

    if args.command == "notes":
        return _notes(args)

    if args.command == "hub":
        return _hub(args)

    if args.command == "review":
        return _review(args)

    if args.command == "check":
        vocab = load(args.source)
        report = check(vocab)
        text = _render_markdown(report) if args.format == "markdown" else _render_text(report)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
            print(f"wrote {args.output}", file=sys.stderr)
        else:
            print(text)
        failed = report.count(ERROR) or (args.strict and report.count(WARN))
        return 1 if failed else 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
