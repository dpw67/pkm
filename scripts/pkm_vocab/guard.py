"""Warn when an export moves prose that the release did not intend to move.

0.1.10 was a presentation release: no triple was supposed to change. A
re-export taken from the wrong project in the SKOS Editor reverted 33 prose
literals -- the seven Cluster definitions, eleven scope notes and fifteen
collection descriptions that 0.1.9 had just written -- and **nothing in the
build noticed**. The export parsed, `make check` reported 0 error,
`make validate` passed 247/247, and the pages rendered. It was found only by
running `scripts/compare_exports.py` by hand.

So this runs on every build instead. It compares the export being built against
the copy committed at `HEAD` and reports what moved, loudly when prose did and
not at all when it did not.

Deliberately narrower than `scripts/compare_exports.py`, which is the full
release cross-check between two arbitrary files -- URIs minted and lost,
hierarchy pairs, ISO 25964 counts, collection membership. This answers one
question on the way past: has prose changed since the last commit, and did you
mean it to? Reach for the other tool when the answer is interesting.

Advisory, never fatal. Prose moving is exactly what a prose release does; the
defect is prose moving *silently*.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from rdflib import Graph
from rdflib.namespace import SKOS

from . import wrap

__all__ = ["prose_delta", "report_prose_delta"]

#: The three properties a reader actually reads. `skos:changeNote` and
#: `dcterms:modified` are excluded on purpose: they move on every editor
#: session by design, so including them would make the check cry wolf and
#: get it switched off.
WATCHED = ((SKOS.definition, "definition"),
           (SKOS.scopeNote, "scopeNote"),
           (SKOS.note, "note"))


def _committed(path: Path, root: Path) -> Graph | None:
    """The export as committed at HEAD, or None if that cannot be read.

    Returns None rather than raising for every ordinary reason a checkout has
    no blob to compare against: not a git repository, a shallow or fresh clone
    with no commits, a path outside the work tree, or a build from a tarball.
    The build must not depend on git being present.
    """
    try:
        rel = path.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    try:
        blob = subprocess.run(
            ["git", "-C", str(root), "show", f"HEAD:{rel.as_posix()}"],
            capture_output=True, timeout=30, check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    if not blob.strip():
        return None
    graph = Graph()
    try:
        graph.parse(data=blob, format="turtle")
    except Exception:
        # A malformed committed copy is not this build's problem to report.
        return None
    return graph


def prose_delta(current: Graph, committed: Graph) -> dict[str, list[str]]:
    """Local names whose definition, scope note or note differs, by property."""
    before, after = wrap(committed), wrap(current)
    out: dict[str, list[str]] = {}
    for prop, name in WATCHED:
        moved = []
        for subject in set(committed.subjects(prop)) | set(current.subjects(prop)):
            if str(committed.value(subject, prop)) != str(current.value(subject, prop)):
                moved.append(after.local_name(subject) or before.local_name(subject))
        if moved:
            out[name] = sorted(moved)
    return out


def report_prose_delta(current: Graph, source: Path, root: Path) -> list[str]:
    """Lines describing what moved since HEAD. Empty when nothing did."""
    committed = _committed(source, root)
    if committed is None:
        return []

    delta = prose_delta(current, committed)
    drift = len(current) - len(committed)
    if not delta and not drift:
        return []

    lines = [f"  export vs HEAD: {len(committed)} -> {len(current)} triples "
             f"({drift:+d})"]
    if not delta:
        lines.append("    no definition, scope note or note changed")
        return lines

    total = sum(len(v) for v in delta.values())
    for name, subjects in delta.items():
        shown = ", ".join(subjects[:6])
        more = f", +{len(subjects) - 6} more" if len(subjects) > 6 else ""
        lines.append(f"    {name:<10} {len(subjects):>3}  {shown}{more}")
    lines.append(f"  ^ {total} prose literal{'' if total == 1 else 's'} moved. "
                 "Intended? If this release is not about prose, stop and run")
    lines.append("    scripts/compare_exports.py before checking in.")
    return lines
