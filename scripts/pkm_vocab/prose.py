"""Checks on the words inside a note, rather than on the shape of the graph.

Two defects hide in prose and nowhere else, and both are invisible to the
editor that produces them:

  A CamelCase token reads as a citation of a term. When no such term exists the
  note promises a concept the vocabulary does not have -- a dangling reference
  that `dangling-reference` cannot see, because it is spelled in English rather
  than in RDF.

  A misspelling survives indefinitely. Nothing downstream parses prose, so a
  typo in a scope note is as durable as the URI it sits on, and 0.1.7 put all
  of it on a public page.

Both fall out of one tokenising pass, which is why they live together here.

WHY QUOTED SPANS ARE EXEMPT. The SKOS Editor's change notes quote the very
string they record fixing -- `Corrected typo from "definiton" to "definition"`.
Fourteen of the fifteen misspellings in this vocabulary are that pattern, and
they are correct: the note would be useless without the bad spelling in it. A
spell check that cannot see quotation marks would therefore fail forever on a
working audit trail, which is the difference between this check being an ERROR
and being unusable.
"""

from __future__ import annotations

import re
from pathlib import Path

from rdflib import Literal

from . import DCTERMS, SKOS, Vocabulary

#: The system dictionary. macOS ships `web2` (a 1934 Webster's), `web2a`
#: (compound entries) and `propernames`; together ~310k words. It is a 1934
#: dictionary, so it knows "interoperability" but not "workflow" -- hence
#: `wordlist.txt` alongside it.
DICTIONARY = Path("/usr/share/dict")
DICTIONARY_FILES = ("web2", "web2a", "propernames")

#: Words this vocabulary uses that the system dictionary predates, plus the
#: external product names that legitimately appear as CamelCase.
WORDLIST = Path(__file__).with_name("wordlist.txt")

#: A CamelCase token: two or more capitalised runs, each with lowercase in it.
#: Deliberately conservative. `PKMSwift` and `EKGEvent` do not match, because an
#: all-caps run has no word boundary before the next capital -- so acronym-led
#: names are missed rather than misreported. A false positive blocks the build;
#: a miss only forgoes a finding.
CAMEL_TOKEN = re.compile(r"\b(?:[A-Z][a-z0-9]+){2,}\b")

#: Splits a local name into its words, for the allowlist.
CAMEL_PARTS = re.compile(r"[A-Z]+(?![a-z])|[A-Z][a-z]+|[a-z]+")

#: A prose word worth checking. Four characters and up: below that the
#: dictionary's coverage of abbreviations is worse than the signal.
PROSE_WORD = re.compile(r"\b[a-z][a-z']{3,}\b")

#: Everything between quotes, of any of the three kinds these notes use. The
#: SKOS Editor writes curly doubles; hand-typed notes use straight ones; code
#: spans use backticks. Single quotes are left alone on purpose -- they collide
#: with apostrophes.
QUOTED = re.compile(r'"[^"]*"|“[^”]*”|`[^`]*`')

#: The editor's own record of a duplication, which is the only evidence that a
#: concept began life as a copy of another.
DUPLICATED_FROM = re.compile(r'Duplicated from [“"]([^”"]+)[”"]')

#: Suffixes to strip before a dictionary lookup. A 1934 dictionary lists
#: headwords, so "aggregates" and "aggregated" are both absent while
#: "aggregate" is present.
SUFFIXES = ("s", "es", "ies", "ed", "d", "ing", "ings", "er", "ers", "est",
            "ly", "ion", "ions", "ment", "ments", "al", "able", "ised", "ized")

#: Prose a reader sees on the term page. A phantom citation here is a broken
#: promise to a consumer; the same token in a change note is a historical record
#: of a name that has since gone, which is not wrong.
READER_FACING = (SKOS.definition, SKOS.scopeNote, SKOS.note, SKOS.editorialNote,
                 DCTERMS.description)


def _lexicon() -> set[str] | None:
    """Every word the system dictionary knows, or None if it has none.

    Returning None rather than an empty set matters: absent and empty mean
    different things to the caller, which downgrades the spelling check rather
    than reporting 1,700 misspellings on a machine without `/usr/share/dict`.
    """
    words: set[str] = set()
    for name in DICTIONARY_FILES:
        try:
            text = (DICTIONARY / name).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        words |= {line.strip().lower() for line in text.splitlines() if line.strip()}
    return words or None


def _wordlist() -> tuple[set[str], set[str]]:
    """The committed allowlist, split into prose words and CamelCase tokens."""
    words: set[str] = set()
    tokens: set[str] = set()
    if not WORDLIST.exists():
        return words, tokens
    for line in WORDLIST.read_text(encoding="utf-8").splitlines():
        entry = line.split("#", 1)[0].strip()
        if not entry:
            continue
        (tokens if entry[:1].isupper() else words).add(entry.lower())
    return words, tokens


def _known(word: str, lexicon: set[str]) -> bool:
    """Is `word` in `lexicon`, allowing for inflection?"""
    word = word.lower()
    if word in lexicon:
        return True
    # Contractions: check the stem, not the whole token. "they're" is "they".
    if "'" in word:
        return all(part in lexicon or len(part) < 4 for part in word.split("'") if part)
    for suffix in SUFFIXES:
        # Two characters, not three: "using" strips to "us", which only finds
        # "use" once the floor is low enough to let it try.
        if not word.endswith(suffix) or len(word) - len(suffix) < 2:
            continue
        stem = word[: -len(suffix)]
        if stem in lexicon or stem + "e" in lexicon or stem + "y" in lexicon:
            return True
        # "running" -> "run": a doubled consonant before the suffix.
        if len(stem) > 2 and stem[-1] == stem[-2] and stem[:-1] in lexicon:
            return True
        # "clarified" -> "clarify": the y-to-i shift, which applies to the
        # whole -ied/-ier/-iest/-ies family. The 1934 dictionary lists some of
        # these as headwords ("applied", "carried") and not others
        # ("modified", "verified", "earlier"), so without this the check flags
        # ordinary English at ERROR depending on which words Webster liked.
        if stem.endswith("i") and stem[:-1] + "y" in lexicon:
            return True
    return False


def _vocabulary_words(vocab: Vocabulary) -> tuple[set[str], set[str]]:
    """Words and tokens the vocabulary defines about itself.

    Derived rather than committed: every local name, every word inside one, and
    every word of every label. A term's own name is never a misspelling, and a
    note citing a term that exists is never a phantom citation.
    """
    words: set[str] = set()
    tokens: set[str] = set()
    for uri in list(vocab.concepts()) + list(vocab.collections()):
        name = vocab.local_name(uri)
        tokens.add(name.lower())
        words |= {part.lower() for part in CAMEL_PARTS.findall(name)}
        for prop in (SKOS.prefLabel, SKOS.altLabel):
            for label in vocab.graph.objects(uri, prop):
                words |= {w.lower() for w in re.findall(r"[A-Za-z]+", str(label))}
    return words, tokens


def check(vocab: Vocabulary, report, error: str, warn: str, info: str) -> None:
    """Add prose findings to `report`.

    Levels are passed in rather than imported, so that `checks.py` stays the one
    place that decides what each tier means.
    """
    graph = vocab.graph
    allowed_words, allowed_tokens = _wordlist()
    own_words, own_tokens = _vocabulary_words(vocab)
    known_tokens = own_tokens | allowed_tokens

    dictionary = _lexicon()
    # No system dictionary: skip spelling entirely and say so once, rather than
    # failing a build on a machine that cannot run the check. Reporting the
    # words at a lower level was the other option and is worse -- with nothing
    # to compare against, every word is unrecognised, so it would mean listing
    # seventeen hundred ordinary words as suspect. Unchecked is not the same as
    # suspect, and only one of the two is worth printing.
    lexicon = (dictionary or set()) | own_words | allowed_words

    phantom: dict[str, tuple[set[str], bool]] = {}
    suspect: dict[str, set[str]] = {}

    from .checks import PROSE

    for subject, prop, value in graph:
        if prop not in PROSE or not isinstance(value, Literal):
            continue
        name = vocab.local_name(subject) if vocab.is_local(subject) else str(subject)
        # Blank the quoted spans in place, so offsets and word boundaries are
        # unchanged and a quoted phrase cannot glue two words together.
        bare = QUOTED.sub(lambda m: " " * len(m.group(0)), str(value))

        for match in CAMEL_TOKEN.finditer(bare):
            token = match.group(0)
            if token.lower() in known_tokens:
                continue
            subjects, visible = phantom.setdefault(token, (set(), False))
            subjects.add(name)
            phantom[token] = (subjects, visible or prop in READER_FACING)

        if dictionary is None:
            continue
        for match in PROSE_WORD.finditer(bare):
            word = match.group(0)
            if _known(word, lexicon):
                continue
            suspect.setdefault(word.lower(), set()).add(name)

    for token, (subjects, visible) in sorted(phantom.items()):
        cited = ", ".join(sorted(subjects))
        report.add(
            error if visible else warn,
            "phantom-citation",
            f'prose cites "{token}", which is not a term in this vocabulary'
            + ("" if visible else " (historical name in a change note?)"),
            cited,
        )

    # Reached only with a dictionary, since the loop above skips the word pass
    # without one -- so this is unconditionally an ERROR.
    for word, subjects in sorted(suspect.items()):
        report.add(
            error,
            "misspelled-word",
            f'"{word}" is in neither the dictionary nor wordlist.txt',
            ", ".join(sorted(subjects)),
        )

    if dictionary is None:
        report.add(
            info, "no-dictionary",
            f"no dictionary under {DICTIONARY}; spelling went unchecked",
        )


def stale_duplicates(vocab: Vocabulary) -> list[tuple[str, str]]:
    """Concepts still carrying the definition of the concept they were copied from.

    The SKOS Editor writes `Duplicated from "X"` when a term is created as a
    copy, and duplication is the normal way terms are authored here -- 96 of the
    223 concepts began that way. What distinguishes a finished duplicate from an
    abandoned one is whether its definition ever changed: an identical
    definition means the copy describes its source, not itself.

    Returns (local name, source label) pairs.
    """
    graph = vocab.graph
    by_label: dict[str, list] = {}
    for uri in list(vocab.concepts()) + list(vocab.collections()):
        label = graph.value(uri, SKOS.prefLabel)
        if label is not None:
            by_label.setdefault(str(label), []).append(uri)

    found: list[tuple[str, str]] = []
    for uri in list(vocab.concepts()) + list(vocab.collections()):
        definition = graph.value(uri, SKOS.definition)
        if definition is None:
            continue
        for note in graph.objects(uri, SKOS.changeNote):
            match = DUPLICATED_FROM.search(str(note))
            if match is None:
                continue
            source_label = match.group(1)
            for source in by_label.get(source_label, ()):
                # A concept that took over its source's name reports itself as
                # its own source. That is a deletion, not an unfinished copy.
                if source == uri:
                    continue
                if str(graph.value(source, SKOS.definition) or "") == str(definition):
                    found.append((vocab.local_name(uri), source_label))
                    break
            else:
                continue
            break
    return found
