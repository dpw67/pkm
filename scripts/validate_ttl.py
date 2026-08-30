"""Parse-check Turtle files and report every failure, not just the first.

Stands in for `riot --validate` so `make validate` runs without Apache Jena.
Paths are taken from argv; `vocab/terms/*.ttl` and `shapes/*.ttl` are added
automatically because listing 241 generated files in the Makefile would be noise.
"""

from __future__ import annotations

import glob
import sys

import rdflib


def main(argv: list[str]) -> int:
    files = list(dict.fromkeys(
        argv + sorted(glob.glob("vocab/terms/*.ttl")) + sorted(glob.glob("shapes/*.ttl"))
    ))
    failures: list[tuple[str, str]] = []
    empty: list[str] = []

    for path in files:
        try:
            graph = rdflib.Graph()
            graph.parse(path)
        except Exception as exc:  # noqa: BLE001 — report, don't stop at the first
            failures.append((path, f"{type(exc).__name__}: {exc}"))
            continue
        # A file that parses to nothing is legal Turtle but never intentional here.
        if len(graph) == 0:
            empty.append(path)

    for path, reason in failures:
        print(f"FAIL  {path}\n      {reason}")
    for path in empty:
        print(f"EMPTY {path} — parses, but contains no triples")

    ok = len(files) - len(failures) - len(empty)
    print(f"{ok}/{len(files)} Turtle files parse with content")
    return 1 if failures or empty else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
