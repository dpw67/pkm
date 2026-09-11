"""A reading sheet for reviewing the vocabulary a family at a time.

`check` answers "is anything broken". This answers a different question:
"does this read the way I meant it to". Those need different layouts. A
checker reports one term at a time; drift between terms that are supposed to
be parallel is invisible that way, and it is the defect this vocabulary keeps
producing -- three of the five `*Review` definitions were wrong, and
`QuarterLog` named itself as its own source, and neither is findable by
reading 223 pages in alphabetical order.

So the sheet pivots. Terms sharing a suffix (`DayPlan`, `WeekPlan`,
`MonthPlan` ...) print as one table with a row each, definitions in a column.
A gap in the grid is a term that was never minted; a row that reads unlike its
neighbours is drift. Both are obvious across, and neither is obvious down.

Nothing here fails a build. Every flag is a hint for a human reader.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

from rdflib import URIRef

from . import SKOS, Vocabulary

#: Split a local name into words, acronym-aware, so `PKMPythonAPI` is
#: PKM + Python + API rather than one run of capitals. Non-alphanumerics are
#: turned into boundaries first, which is how `Month-Health` reaches the
#: `*Health` grid at all -- the hyphen is the defect, not a reason to hide it.
WORDS = re.compile(r"[A-Z]+(?=[A-Z][a-z])|[A-Z]?[a-z]+|[A-Z]+|\d+")

#: Printed in this order with a blank row where a term does not exist, because
#: the gap is the finding. Every other family prints only what it has.
PERIODS = ("Day", "Week", "Month", "Quarter", "Year", "Decade", "Life")

#: Period words to blank out before comparing two definitions, so that
#: "...evaluating a completed week." and "...evaluating a completed month."
#: compare equal and a genuine difference stands out.
PERIOD_WORDS = {
    "day": "daily", "week": "weekly", "month": "monthly",
    "quarter": "quarterly", "year": "yearly", "decade": "", "life": "",
}

#: A suffix needs this many terms before it is worth a table of its own.
MIN_FAMILY = 3


def words(name: str) -> list[str]:
    return WORDS.findall(re.sub(r"[^A-Za-z0-9]+", " ", name))


def split(name: str) -> tuple[str, str] | None:
    """(first word, the rest) -- or None for a single-word name."""
    parts = words(name)
    if len(parts) < 2:
        return None
    return parts[0], "".join(parts[1:])


def _normalise(text: str, stem: str) -> str:
    """Blank the family's own name out of its prose, then flatten it.

    Two definitions that differ only in naming their own period should
    compare equal; anything left over is a real difference.
    """
    out = text.lower()
    for word in filter(None, (stem.lower(), PERIOD_WORDS.get(stem.lower(), ""))):
        out = out.replace(word, "~")
    return re.sub(r"[^a-z~]+", " ", out).strip()


def _cell(text: str) -> str:
    """Make a literal safe for a Markdown table cell without losing it."""
    if not text:
        return "—"
    return text.replace("|", "\\|").replace("\n", "<br>").strip()


class Sheet:
    """Everything the renderer needs, worked out once."""

    def __init__(self, vocab: Vocabulary):
        self.vocab = vocab
        self.concepts = vocab.concepts()
        self.by_name = {vocab.local_name(u): u for u in self.concepts}

        self.parents: dict[str, list[str]] = defaultdict(list)
        self.children: dict[str, list[str]] = defaultdict(list)
        for child, parent in vocab.broader_pairs():
            if not (vocab.is_local(child) and vocab.is_local(parent)):
                continue
            kid, mum = vocab.local_name(child), vocab.local_name(parent)
            self.parents[kid].append(mum)
            self.children[mum].append(kid)
        for mapping in (self.parents, self.children):
            for key in mapping:
                mapping[key] = sorted(set(mapping[key]))

        self.families = self._families()
        self.placed = {n for fam in self.families.values() for n in fam.values()}
        self.flags: list[str] = []

    def _families(self) -> dict[str, dict[str, str]]:
        """suffix -> {first word: local name}, for suffixes worth a table."""
        grouped: dict[str, dict[str, str]] = defaultdict(dict)
        for name in self.by_name:
            parts = split(name)
            if parts is None:
                continue
            stem, suffix = parts
            # Two terms with the same prefix and suffix cannot both be shown;
            # in practice the local names are unique, so this cannot collide.
            grouped[suffix][stem] = name

        keep = {}
        for suffix, members in grouped.items():
            periodic = [p for p in PERIODS if p in members]
            if len(members) >= MIN_FAMILY or len(periodic) >= 2:
                keep[suffix] = members
        return dict(sorted(keep.items()))

    def prose(self, name: str, prop: URIRef) -> str:
        uri = self.by_name[name]
        return "\n".join(str(o) for o in self.vocab.graph.objects(uri, prop))

    def order(self, suffix: str) -> list[tuple[str, str | None]]:
        """Rows for a family: (first word, local name or None for a gap)."""
        members = self.families[suffix]
        periodic = [p for p in PERIODS if p in members]
        if len(periodic) >= 2:
            # Show the whole calendar, gaps included -- a missing MonthPlan is
            # the sort of thing only an empty row makes visible.
            rows = [(p, members.get(p)) for p in PERIODS[:max(
                PERIODS.index(p) for p in periodic) + 1]]
            rest = sorted(k for k in members if k not in PERIODS)
            return rows + [(k, members[k]) for k in rest]
        return [(k, members[k]) for k in sorted(members)]

    def groups(self, suffix: str) -> dict[str, str]:
        """stem -> group letter, for families whose definitions do not all agree.

        Deliberately does not pick a winner. The most common wording is not the
        right wording -- four of the eight `*Cluster` definitions share the
        formulaic "A group of related notes about a ..." and the four that say
        something real are the minority. So this partitions and lets the reader
        judge, rather than flagging the odd one out and being backwards half
        the time.

        Empty dict means either one wording throughout, or no two terms
        agreeing at all -- in both cases there is no partition to show.
        """
        members = self.families[suffix]
        shapes = {
            stem: _normalise(self.prose(name, SKOS.definition), stem)
            for stem, name in members.items()
        }
        counts = Counter(shape for shape in shapes.values() if shape)
        # Largest group first, so A is always the most common wording; ties
        # broken on the shape text to keep the letters stable between runs.
        ranked = sorted(counts, key=lambda shape: (-counts[shape], shape))
        if len(ranked) < 2 or counts[ranked[0]] < 2:
            return {}
        # A family needs a template before anything can be said to depart from
        # it. `*Event` splits fourteen ways across fifteen terms -- an event
        # about sleep and an event about a script have nothing to share -- so
        # requiring the largest wording to cover half the family drops the
        # families that were never parallel in the first place.
        if counts[ranked[0]] * 2 < len(members):
            return {}
        letters = {shape: chr(ord("A") + i) for i, shape in enumerate(ranked)}
        return {stem: letters.get(shape, "?") for stem, shape in shapes.items()}

    def partition(self, suffix: str) -> str | None:
        """One line describing how a family's definitions split, or None."""
        groups = self.groups(suffix)
        if not groups:
            return None
        sizes = Counter(groups.values())
        parts = ", ".join(
            f"**{letter}** {sizes[letter]}" for letter in sorted(sizes))
        return (f"`*{suffix}` definitions fall into {len(sizes)} wordings "
                f"({parts}) — the largest group is not necessarily the right one")


def _family_table(sheet: Sheet, suffix: str) -> list[str]:
    out = [f"### `*{suffix}`", ""]
    groups = sheet.groups(suffix)
    note = sheet.partition(suffix)
    if note:
        out += [f"> {note}", ""]

    out += ["| | term | definition | scope note |", "| --- | --- | --- | --- |"]
    for stem, name in sheet.order(suffix):
        if name is None:
            out.append(f"| **gap** | _no `{stem}{suffix}`_ | | |")
            continue
        mark = groups.get(stem, "")
        label = sheet.vocab.label(sheet.by_name[name])
        term = f"`{name}`" if label == name else f"`{name}`<br>{label}"
        out.append(
            f"| {mark} | {term} | {_cell(sheet.prose(name, SKOS.definition))} "
            f"| {_cell(sheet.prose(name, SKOS.scopeNote))} |"
        )
    out.append("")
    return out


def _leftovers(sheet: Sheet) -> list[str]:
    """Terms in no family, grouped by parent so siblings still sit together."""
    rest = [n for n in sorted(sheet.by_name) if n not in sheet.placed]
    grouped: dict[str, list[str]] = defaultdict(list)
    for name in rest:
        parents = sheet.parents.get(name) or ["(no parent)"]
        grouped[parents[0]].append(name)

    out: list[str] = []
    for parent in sorted(grouped):
        out += [f"### Under `{parent}`", ""]
        out += ["| term | definition | scope note |", "| --- | --- | --- |"]
        for name in grouped[parent]:
            label = sheet.vocab.label(sheet.by_name[name])
            term = f"`{name}`" if label == name else f"`{name}`<br>{label}"
            extra = [p for p in sheet.parents.get(name, []) if p != parent]
            if extra:
                term += "<br>_also under " + ", ".join(f"`{p}`" for p in extra) + "_"
            out.append(
                f"| {term} | {_cell(sheet.prose(name, SKOS.definition))} "
                f"| {_cell(sheet.prose(name, SKOS.scopeNote))} |"
            )
        out.append("")
    return out


def _collections(sheet: Sheet) -> list[str]:
    vocab = sheet.vocab
    out = ["| collection | members | description |", "| --- | ---: | --- |"]
    for uri in vocab.collections():
        name = vocab.local_name(uri)
        count = len(list(vocab.graph.objects(uri, SKOS.member)))
        note = "\n".join(str(o) for o in vocab.graph.objects(uri, SKOS.note))
        out.append(f"| `{name}` | {count} | {_cell(note)} |")
    out.append("")
    return out


def _childless(sheet: Sheet) -> list[str]:
    """Terms with no children whose siblings all have some."""
    found = []
    for name in sorted(sheet.by_name):
        if sheet.children.get(name):
            continue
        for parent in sheet.parents.get(name, []):
            siblings = [s for s in sheet.children[parent] if s != name]
            if siblings and all(sheet.children.get(s) for s in siblings):
                found.append(f"- `{name}` — no children, but every other term "
                             f"under `{parent}` has some")
                break
    return found


def render(vocab: Vocabulary) -> str:
    sheet = Sheet(vocab)

    out = [
        f"# Vocabulary review — `{vocab.path.name}`",
        "",
        f"{len(sheet.concepts)} concepts, {len(vocab.collections())} collections. "
        "Regenerate with `make review`.",
        "",
        "Read a family table **across**, not down. Terms sharing a suffix are "
        "supposed to say the same thing about different subjects, so a row "
        "that reads unlike its neighbours is drift and an empty row is a term "
        "that was never minted. Where a family's definitions do not all agree, "
        "each row carries a letter for its wording — **A** is the most common, "
        "which is not the same as the most correct.",
        "",
    ]

    gaps = [f"- `{stem}{suffix}` is missing from the `*{suffix}` family"
            for suffix in sheet.families
            for stem, name in sheet.order(suffix) if name is None]
    odd = [f"- {note}" for note in
           filter(None, (sheet.partition(s) for s in sheet.families))]
    childless = _childless(sheet)

    out += ["## Worth a look", ""]
    if gaps or odd or childless:
        out += gaps + odd + childless + [""]
    else:
        out += ["Nothing flagged.", ""]

    out += ["## Families", ""]
    for suffix in sheet.families:
        out += _family_table(sheet, suffix)

    out += ["## Everything else, by parent", ""]
    out += _leftovers(sheet)

    out += ["## Collections", ""]
    out += _collections(sheet)

    return "\n".join(out)


def write_review(vocab: Vocabulary, out: Path) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(vocab), encoding="utf-8")
    return out
