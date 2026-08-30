# LYT Circle — draft announcement posts

Two drafts. The first is the main announcement; the second is a shorter,
single-question follow-up to post a week or so later if the first one gets traction.

**Pre-flight, before posting:**

- `notes.warrenweb.net` is still behind the Plus paywall. Either drop the paywall first
  or cut that link — a paywalled link in a "please give me feedback" post reads badly.
- The blog post doesn't exist yet. Placeholder marked `[BLOG POST URL]` below; drop the
  sentence if you post before writing it.
- Checked against the published vocabulary: "Effort" is not a term (the terms are
  *Effort Cluster*, *Efforts Folder*, *Project*, *Area*, *Interest*), and the time
  periods are siblings under Calendar rather than nested — the draft is written to match.
- Three concepts cite the ACE for Organization Knowledge Pack (CC BY-NC-ND). Your
  definitions are your own paraphrases, which is ordinary citation and fine. One thing
  to eyeball: *Idea Emergence* uses Nick's "nothingness / somethingness" phrasing
  fairly directly — worth putting in quotation marks, given you're publishing CC BY 4.0
  and he's ND.

---

## Post 1 — main announcement

**Suggested title:** I turned my vault's vocabulary into something my tools can read — would love your eyes on it

---

My Ideaverse has gotten big enough that I have a naming problem, and I suspect I'm not
the only one.

I run ACE, so I have Atlas, Calendar, and Efforts. Underneath that I've built out a
"Day Cluster" — the plan, log, journal, review, and health notes that belong to a single
day — plus similar clusters for weeks, months, quarters, and years. That structure works
well for me in Obsidian. The trouble started when the vault stopped being the only thing
that touches it.

I've got a Swift app for meal planning, Python scripts that build daily notes from
templates, a Neo4j graph, and Claude reading across all of it. Every one of those has its
own quiet idea of what a "Day Plan" is, or whether an "Effort" is the same thing as a
project. Nothing breaks loudly. Things just drift, and six months later a script writes a
note the app can't find.

So I did the boring thing: I wrote the terms down. 223 of them, each with a definition, a
scope note saying where it actually lives, and its relationships to the terms above and
below it. Then I published the whole thing at a permanent address so my tools — and
anyone else — can point at a term and get a real answer:

**https://w3id.org/pkm/vocab**

Under the hood it's SKOS, which is the standard librarians and taxonomists use for
exactly this. You genuinely don't need to care about that part. What matters for anyone
reading it is that every term has a stable address, so "Day Cluster" means one specific
documented thing and can't quietly become two.

Some of what's in there will look familiar: Ideaverse, Spark, Effort Cluster, ACE
Organization, ARC Ideation, Idea Emergence. Some of it is mine and probably idiosyncratic — the
diabetes health notes, the meal planning, the Swift app intents.

**This is version 0.1.1, which is my way of saying it's a first draft and I expect to be
wrong about things.** Nothing is deleted when I change my mind — a retired term stays
resolvable and points at whatever replaced it — so it's safe to link to even now.

What I'd genuinely like feedback on:

1. **Should the time periods nest, or sit side by side?** Right now Day, Week, Month,
   Quarter, Year and Decade are all siblings under Calendar — the only nesting is that a
   Day is also part of a Week. I keep going back and forth. A Day genuinely is part of a
   Week which is part of a Month, but when I nest them the tree gets deep and the notes
   at each level don't actually inherit anything from the level above. Curious how others
   see it.
2. **Are the names right?** I went back and forth on "Cluster" for a dozen notes that
   belong to one day. Is there better language for that?
3. **What's obviously missing?** There's a whole layer of LYT practice — MOCs, home
   notes, the maps — that I haven't modelled at all yet, mostly because I wasn't sure
   whether they're *terms* or *techniques*.

Browse it here: https://w3id.org/pkm/vocab — the hierarchy view is probably the fastest
way in, and every term links to its own page.

I'm also writing up the thinking behind it, and keeping working notes as I go:
[BLOG POST URL] · https://notes.warrenweb.net

Pick at it. Tell me what's wrong with it. That's what a 0.1 is for.

---

## Post 2 — follow-up (post later, only if #1 lands)

**Suggested title:** What do you call the notes that belong to a single day?

---

Following on from the vocabulary I posted a while back — one naming decision I'm still
unsure about, and I'd rather ask than keep guessing.

For each day I generate a handful of notes: a plan, a log, a journal entry, a review,
health data, sometimes a schedule and a canvas. They're distinct notes, but they're one
thing conceptually — the day's record.

I've been calling that a **Day Cluster**, and the same pattern repeats for Week, Month,
Quarter, and Year.

"Cluster" has never quite sat right. It sounds like something that happened by accident
rather than something I deliberately assembled. Candidates I've considered and rejected:

- **Day Note** — already means one specific note to most people
- **Daily** — too vague, and it's an adjective
- **Day Set** / **Day Group** — technically accurate, completely lifeless
- **Day Folder** — describes the storage, not the idea

So: what do you call yours? Or do you not have a name for it, because you've never needed
one until a script asked you to?

(Terms live at https://w3id.org/pkm/vocab if you want to see the rest of the structure —
Day Cluster is under Calendar, alongside the Week, Month, Quarter and Year clusters.)
