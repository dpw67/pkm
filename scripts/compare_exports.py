#!/usr/bin/env python3
"""Compare two SKOS Editor exports at the triple level.

Serialization order differs between exports, so `diff` overstates the change.
This compares triple sets and reports what actually moved, in the terms that
matter for a release: URIs, hierarchy, membership, and prose.

Two uses:

  Round-trip fidelity -- did the editor give back what it was given?
      compare_exports.py before.ttl after.ttl --expect-identical

  Release cross-check -- did the editor session land the intended literals?
      compare_exports.py v0.1.8.ttl new-export.ttl

Exits non-zero when --expect-identical is passed and anything differs.
"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rdflib.namespace import SKOS  # noqa: E402

import pkm_vocab  # noqa: E402


def _short(uri) -> str:
    return str(uri).rsplit("#", 1)[-1].rsplit("/", 1)[-1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--expect-identical", action="store_true",
                    help="exit non-zero on any difference (round-trip test)")
    args = ap.parse_args()

    a = pkm_vocab.load(args.before)
    b = pkm_vocab.load(args.after)

    added = set(b.graph) - set(a.graph)
    removed = set(a.graph) - set(b.graph)

    # The invariants a patch release must not break.
    ua = {a.local_name(u) for u in a.concepts() + a.collections()}
    ub = {b.local_name(u) for u in b.concepts() + b.collections()}
    iso = lambda v: sum(1 for _ in v.graph.triples((None, None, None))
                        if "iso25964" in str(_[1]))

    def members(v):
        return {v.local_name(c): frozenset(v.local_name(m)
                for m in v.graph.objects(c, SKOS.member)) for c in v.collections()}

    print(f"triples   {len(a.graph)} -> {len(b.graph)}  (+{len(added)} / -{len(removed)})")
    print(f"URIs      {len(ua)} -> {len(ub)}")
    print(f"  minted  {sorted(ub - ua) or 'none'}")
    print(f"  lost    {sorted(ua - ub) or 'none'}")
    print(f"hierarchy broader pairs {len(a.broader_pairs())} -> {len(b.broader_pairs())}"
          f"  identical={a.broader_pairs() == b.broader_pairs()}")
    print(f"ISO 25964 triples {iso(a)} -> {iso(b)}")
    ma, mb = members(a), members(b)
    changed = sorted(k for k in set(ma) | set(mb) if ma.get(k) != mb.get(k))
    print(f"collection membership changed: {changed or 'none'}")

    if added or removed:
        print("\nby property:")
        pa = Counter(_short(p) for _, p, _ in removed)
        pb = Counter(_short(p) for _, p, _ in added)
        for prop in sorted(set(pa) | set(pb)):
            print(f"  {prop:24} -{pa.get(prop,0):<4} +{pb.get(prop,0)}")
        subs = sorted({_short(s) for s, _, _ in added | removed})
        print(f"\nsubjects touched ({len(subs)}): {', '.join(subs)}")

    if args.expect_identical:
        ok = not added and not removed
        print("\nROUND-TRIP LOSSLESS" if ok else "\nROUND-TRIP LOSSY — see above")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
