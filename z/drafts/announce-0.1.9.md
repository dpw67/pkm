# Draft — GitHub Discussions announcement for v0.1.9

**Status:** draft. Post to
[Announcements](https://github.com/dpw67/pkm/discussions/categories/announcements)
by hand; Discussions has no draft state, so posting is immediately public.

**Prerequisites — both now satisfied, so this is clear to post.**

1. The `v0.1.9` release is **published**, not a draft. ✅ Verified 2026-09-14:
   `draft: false`, published 22:29 UTC, and v0.1.9 holds the **Latest** badge.
   It mattered because a draft's tag URL is not a 404 — it returns 200 with a
   bare page carrying only the title in `og:` meta tags, so the "Release notes"
   link below would have landed a reader on what looks like an *empty* release
   rather than a missing one. Tested by grepping the anonymous page for four
   distinctive strings from the notes body — `DayMeeting`, `Seventy-four`,
   `membership rule`, `241 URIs` — which returned **0 matches each while
   drafted and 1 each now**.
2. `w3id.org/pkm` serves 0.1.9. ✅ Verified 2026-09-14: the namespace returns
   `owl:versionInfo "0.1.9"`, the front page reads "Vocabulary 0.1.9", and
   `vocab/WeekCluster`, `vocab/Knowledge` and `vocab/DayCollection` all carry
   their new text.

**Title — pick one:**

- `PKM Vocabulary v0.1.9 — a cluster is a whole, and a collection says what decides membership`
- `PKM Vocabulary v0.1.9 — what the graph said all along`

---

## Body

Two releases ago I argued that a cluster is not a bag — that a Day Cluster is a
whole of unlike parts about one subject, rather than a pile of notes that
happen to mention the same day. I rewrote `Cluster` and `DayCluster` to say so,
and left seven concepts underneath them still defined as "a group of related
notes about a …". All three of `Cluster`'s direct children were among them. So
anyone who followed the hierarchy down one level met the exact phrasing the
parent had just abandoned.

v0.1.9 finishes it, and then finds the same defect one layer over.

**Two of the seven could not take the same sentence, and the graph is why.**
`TimeCluster` turns out to be a generic parent, not a whole — its children are
five period clusters, which are five of a kind rather than unlike parts. And
`EffortCluster` and `TopicCluster` carry no ISO 25964 relations at all, alone
among the clusters, so writing "unlike parts" into their definitions would have
asserted in prose exactly what this release exists to stop asserting. They say
less, on purpose, and the missing relations are now written down as work.

**The collections were the same mistake in different clothes.** Fourteen of
eighteen descriptions opened "All notes related to ‹X›". That is not a
membership rule — nothing in it tells a reader whether a given term belongs,
which is why the collections read as vague. Each now states the rule instead.

What I could not do is change any membership, because that is not editorial: if
`DayCollection` drops a member, a query that used to return it now does not.
So where a collection turns out to be a hand copy of a subtree, the description
says so **and says which side wins**. `DayCollection` now records that it holds
26 members against the 25 concepts under `DayCluster`, that `DayMeeting` is in
the tree and missing from the collection, and that the hierarchy is
authoritative where the two disagree. It cannot fix the drift; it can tell you
which source to trust.

**Seventy-four more change notes were repaired, and none of that was my work.**
The SKOS Editor fixed two long-standing artifacts — a language tag written
inside a quoted label, and a proposer named twice when they approved their own
proposal. I had recorded both as permanent upstream residue. They were not;
issue #81 explains why the fix had appeared not to reach this vocabulary, whose
notes all arrived by import. Thanks to Jessica Talisman, whose
[Intentional Arrangement SKOS Editor](https://github.com/jesstalisman-ia/intentional-arrangement-skos)
this vocabulary is authored in.

Those 74 changed nothing a reader sees, which is the part I like: the build had
been repairing them on the way out since v0.1.6, so the published pages always
read correctly and only the source was ever wrong.

**Nothing moved.** 241 URIs, 236 hierarchy links, 318 ISO 25964 relations and
all 18 collection membership sets are identical to v0.1.8. Prose only, so by
the versioning table this is a patch — cite anything you were citing before.

- [Release notes](https://github.com/dpw67/pkm/releases/tag/v0.1.9)
- [Changelog](https://github.com/dpw67/pkm/blob/main/CHANGELOG.md)
- [The vocabulary](https://w3id.org/pkm/vocab)

As always: if a definition looks wrong to you, that is the most useful thing
you can tell me. Three of the fixes in this release exist because the wording
looked fine one term at a time and only failed when read next to its siblings.
