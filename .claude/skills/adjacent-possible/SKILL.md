---
name: adjacent-possible
description: Use this skill whenever Tyler wants to grow his skill library outward — "what skills am I missing", "propose some new skills", "expand the library", "what's adjacent to what I have", "generate skills", "run adjacent possible", or any request to find and build the next set of skills. Also trigger when he finishes building a skill and asks "what's next" in the context of the vault, or when he notices he's re-explaining something to Claude for the third time. Reads the existing library, scores the unbuilt neighborhood along the embodiment axis, and installs five complete new skills live, along with one nomination for retirement.
---

# Adjacent Possible

Grow the skill library outward. Read what exists, find the empty seats, and build five complete skills that sit one step away — chosen not for topical nearness but for **enactment delta**: how much distance each one collapses between something Tyler already knows and something he actually does.

The name is Kauffman's. The adjacent possible is the set of states reachable in one move from where a system currently stands. Not everything imaginable — everything *next*. This skill maps that set and then occupies five points in it.

**Standard:** *scire est facere.* A candidate that teaches, explains, summarizes, or "helps him think about" something is a bad candidate. A candidate that ends with a file, a filed position, an entered order, a sent message, a scheduled thing, or a changed state is a good one.

---

## The embodiment axis

Everything in this skill hangs off one distinction. Get it wrong and the output is five essays wearing skill costumes. Calibrate against these pairs before scoring anything.

| Weak (describes) | Strong (enacts) |
|---|---|
| "Explain how installment sales work" | "Draft the installment-sale election language and the §453 disclosure for this return" |
| "Summarize what's happening in the market" | "Produce today's watchlist with entry, invalidation, and size, ready to enter" |
| "Help me think about my week" | "Write the week's sprint list to the Vault, one file, ordered, with the first action named" |
| "Discuss trust distribution strategy" | "Compute the DNI carryout for these numbers and output the K-1 line placement" |
| "Give me tips on client communication" | "Draft the actual client email for this specific notice, ready to send" |
| "Review my app architecture" | "Output the schema migration and the three files that change" |

The test in one sentence: **after this skill runs, does something exist that did not exist before, and would Tyler otherwise have made it by hand?**

If the honest answer is "he'd have a better understanding," the candidate scores near zero no matter how elegant the subject. Understanding is upstream of this skill's business.

A softer secondary test, useful for close calls: could the output be pasted, filed, sent, or executed without a rewrite? Artifacts that need Tyler to translate them into a real artifact are still descriptions.

---

## Step 1: Survey the library

Before proposing anything, read what exists. Proposals generated without the survey collide with installed skills, and collisions are the one failure mode that damages what already works.

Do all three:

1. **Read the installed skill list** — name and description for every entry currently available.
2. **Read the bodies** of any skill whose territory a candidate might touch. Descriptions understate scope; bodies reveal it.
3. **Check the library** at `.claude/skills/` in the repo (linked into the vault's `08 Skills/`). The library is the source of truth and may hold skills that aren't currently installed. Also read `.claude/skills/_runs.md` for prior runs — see the run log rule in Step 5.

For each existing skill note two things and only two: **what it produces**, and **what phrases fire it**. That pair is what a new candidate has to clear.

### Region definitions

Sort the library into regions. These are the ones that recur — adapt if the library has moved:

- **Authority work** — tax research, code sections, court opinions, confidence tiering. Output is a reasoned position with citations.
- **Practice mechanics** — return prep, notices, client intake, staff workflow, filing logistics. Output is a thing that goes out the door.
- **Jurisdictional** — state-specific rules, residency, allocation, multi-state edge cases. Output is a filing decision.
- **Market structure** — scanning, sizing, market posture, backtesting, journaling. Output is a decision about capital.
- **Systems and building** — architecture, schema, UI, deployment, tooling. Output is code or a spec.
- **Contemplative and personal** — inquiry, pattern-naming, what's underneath. Output is a named structure, honestly arrived at.
- **Meta** — skills about the vault, about skills, about the working system itself.
- **Household** — family logistics, meals, trips, schedules. Output is a plan someone executes.

A region is **covered** when a request in it routes cleanly to an existing skill. It is **thin** when one skill handles a range that plainly wants two. It is **empty** when a real recurring need has nothing pointed at it. Thin and empty regions are where candidates come from — but so are the seams between covered regions, which is where the best ones come from.

---

## Step 2: Find the gaps

Do not brainstorm topics. Brainstorming produces plausible subjects; this skill needs **open loops** — places where Tyler demonstrably holds knowledge or intent that has no enacting mechanism attached.

Run all five probes. Each yields candidates. Pool them, then score.

### Probe 1 — Knowledge without artifact

Where does he know a domain deeply but produce nothing repeatable from it?

Ask: what could he explain for twenty minutes without notes, that has never once come out of a conversation as a file?

*Worked example:* he can articulate a full framework for how a specific return position gets defended, but there's no skill that outputs the memo-to-file version of that defense. The knowledge is complete; the artifact doesn't exist. Enactment delta is high because the gap is purely mechanical.

The signature of this probe: high expertise, zero output format.

### Probe 2 — Decision without record

Where does he make the same judgment repeatedly and leave no trace of the reasoning?

Ask: what call gets re-derived from scratch every time it comes up, because last time's reasoning wasn't written anywhere?

*Worked example:* the same sizing or entity-choice judgment made four times a year, each time from first principles, each time landing in roughly the same place. A skill here doesn't make the decision — it captures the decision in a fixed structure so the fifth time starts from the fourth.

The signature: repetition plus amnesia. Watch for "I've thought about this before."

### Probe 3 — Input without intake

What arrives regularly with no defined first move?

Ask: what shows up in the inbox, the mail, the feed, or the folder that produces a pause instead of a step?

*Worked example:* a category of correspondence that always requires the same three lookups before anything can happen. The intake skill does the three lookups and outputs the drafted response. Enactment delta is high because the pause was pure friction.

The signature: recurring arrival, undefined response. These are the highest-firing-likelihood candidates in the pool — inputs arrive whether or not he's in the mood.

### Probe 4 — Build without ritual

Where does something stall not for lack of ideas but for lack of a defined next physical action?

Ask: what has he described more than twice and started fewer times?

*Worked example:* a piece of work whose scope is clear and whose first concrete action has never been named. The skill's whole job is to output that first action, singular, specific enough to do in fifteen minutes.

The signature: clarity of intent, absence of a first step. Handle this probe carefully — the skill it produces must *do* something, not exhort. A skill whose output is encouragement fails the embodiment test outright. The output has to be the artifact the first step produces.

### Probe 5 — Boundary crossing

Where do two regions touch with nothing living in the seam?

Ask: what would a skill look like that could only exist because he does both of these things?

*Worked example:* the seam between authority work and systems building produces skills that turn a research framework into a schema. The seam between market structure and contemplative work produces skills about decision-state rather than decisions. The seam between household and systems produces logistics tools nobody else would build.

The signature: nobody else's library would contain it. This probe reliably produces the most interesting candidates and the ones most likely to fail the sprint-fit test — score them honestly rather than protectively.

---

## Step 3: Score

Rank the pool. Score is dominated by enactment delta, modulated by whether the skill will realistically get used, gated on namespace.

### Dimensions

**Enactment delta — 0 to 5, dominant.**
- 5: output is a finished artifact that goes out, gets filed, or gets executed as-is
- 4: output is a complete draft needing only a signature or a click
- 3: output is a structured artifact he'd still edit meaningfully
- 2: output is organized information he'd have to convert into an artifact
- 1: output is analysis
- 0: output is explanation

Anything scoring 2 or below is cut unless the reshaping is obvious, in which case reshape it and rescore.

**Firing likelihood — 0 to 3.** Will this trigger in a real week? A skill for a twice-yearly situation scores 1 no matter how elegant. Weight the calendar: something that fires in season and never otherwise scores by its in-season frequency, noted as seasonal.

**Sprint fit — 0 to 2.** Can one run complete inside a 15-minute focused sprint? Skills requiring an hour of sustained attention rarely get used, however good. If a candidate is inherently large, either narrow it to the first stage or drop it.

Total is out of 10. Below 5, cut.

### Worked scoring pass

| Candidate | Delta | Firing | Sprint | Total | Call |
|---|---|---|---|---|---|
| Drafts the actual response to a recurring correspondence type | 5 | 3 | 2 | 10 | build |
| Captures a repeated judgment in fixed structure | 4 | 2 | 2 | 8 | build |
| Turns a research framework into a working schema | 4 | 1 | 1 | 6 | build, note the seasonality |
| Explains a subject area he already knows well | 0 | 3 | 2 | 5 | cut — delta floor |
| Full multi-stage planning system | 4 | 2 | 0 | 6 | narrow to stage one, rescore |

Note the fourth row: a high total is not enough. The delta floor is a floor, not a term in a sum.

### Namespace clearance — hard gate

Every installed skill's name and description sit permanently in context and compete for triggering. A skill whose trigger surface overlaps an existing one doesn't just underperform; it degrades the skill it overlaps.

Since these install live with no approval step, this gate is the only structural protection the library has. Apply it strictly. A candidate that "probably doesn't overlap" fails — the standard is a clean routing sentence, written out, not a judgment that it's fine.

For each surviving candidate, state:
- the **nearest existing skill**, and
- **one sentence** describing a request that routes unambiguously to the new one and not the old one.

If that sentence can't be written cleanly, the candidate fails. Reshape or drop it.

**Passes:** a candidate that drafts client-facing correspondence about a notice, against an existing skill that researches the underlying authority. Routing sentence: *"draft the reply" goes to the new one; "is this position defensible" goes to the old one.* Different verbs, different outputs, no overlap.

**Fails:** a candidate for "state tax questions" against an existing state-tax skill. There is no request that cleanly separates them. Either fold the new capability into the existing skill's body, or drop it.

**Fails:** a candidate whose description opens with the same phrases as an installed skill, even if the bodies differ. Triggering happens on descriptions. Body distinction doesn't save a description collision.

When a candidate fails this gate but the underlying need is real, say so in the "Not proposed" section and name the existing skill that should absorb it. That's often the more valuable finding.

### Diversity constraint

The final five must span **at least three regions** from Step 1. No run returns five skills from one region.

This is deliberate friction. Left alone, this skill would generate five tax skills every time, because that region has the most surface area and the most legible gaps. Growth outward beats thickening in place — a library that's deep in one region and empty elsewhere fails at exactly the moments Tyler needs something unfamiliar.

If the pool genuinely can't supply three regions, return fewer than five and say why. Padding the slate to hit a count violates the standard more than a short slate does.

---

## Step 4: Build all five

Write each one as a complete, installable skill — not a pitch, not an outline. Tyler chose "build everything, prune later," which means every proposal arrives finished and gets judged on its merits rather than on a description of itself.

### Anatomy

```
skill-name/
  SKILL.md
```

One skill, one folder, one file. Folder name matches the `name:` field. Kebab-case, lowercase, hyphen-separated, short enough to type.

### Writing the description

The description is the entire triggering mechanism. Everything about *when* goes here; nothing about when goes in the body.

Construct it in four parts:

1. **Open with "Use this skill when/whenever..."** — this framing reliably improves triggering.
2. **List literal phrases Tyler would type.** Not paraphrases of intent — the actual words. "got a client in," "what do I need to know about," "run the," "is this deductible." Pull phrasing from how he actually talks in the conversation history where possible.
3. **Name the output.** "Produces a drafted reply," "outputs a scored watchlist," "writes a dated note to the Vault."
4. **Add one pushy clause.** Claude undertriggers. "Also trigger when..." or "Always use this skill for..." earns its place.

Keep it tight enough to survive a 200-character-ish practical limit where that applies. If the description needs more than two sentences to distinguish itself from a neighbor, the skill is probably the wrong shape.

### Writing the body

Write to a competent associate who has never met Tyler and won't get a second briefing.

Include:
- One or two sentences on what the skill does and the standard it upholds.
- The process in ordered, numbered steps, imperative voice.
- The exact output template where there is one, marked as exact.
- Worked examples — one per non-obvious step. Examples do more work than instructions.
- Edge cases and what to watch for.
- Rules at the end, short, each one a line.

Explain *why* a constraint matters rather than issuing bare MUSTs. A skill whose reasoning is visible degrades gracefully in situations its author didn't anticipate; a skill of bare commands doesn't.

Depth reference: match the existing skills in the library — concrete, example-driven, no filler sections.

### Anti-patterns in generated skills

Check each draft against these before installing it. Each one is a way a skill can look finished and be useless:

- **The essay in costume.** Steps that are all "consider," "reflect on," "think about." No artifact at the end. Fails the standard.
- **The everything skill.** Scope so wide it collides with three existing skills and triggers on nothing specific.
- **The empty template.** An output format with no instructions on how to fill it. Produces confident-looking blanks.
- **The unfireable.** A description written in terms Tyler would never type — describes the skill from the inside rather than from the request.
- **The exhortation.** Output is motivation or a reminder that something is undone. Never build these. If a build has stalled, the skill produces the first artifact, not a nudge about producing it.
- **The dependency.** Requires a tool, file, or connector that isn't reliably present. Either handle the absence in the body or don't build it.

---

## Step 5: Install live

The five go straight into the active library. No staging folder, no promotion step. Tyler prunes after the fact rather than approving in advance, which means the quality gates in Step 3 are doing all the work — run them honestly rather than trusting a downstream review that isn't coming.

Write to the library: `.claude/skills/<skill-name>/SKILL.md` in the ComfyUI repo, then `git add`, `git commit`, and `git push -u origin claude/1031-build-to-suit-skill-4b05s1`. The library is junction-linked into the vault's `08 Skills` and the local Claude skills directory by `install.ps1`, so one write covers every location.

In a sandbox instead: write to `./adjacent-possible-output/<skill-name>/SKILL.md` and package the set as one ZIP with the skill folders at the archive root.

Newly installed skills become invocable on the next session load. Say so when reporting.

**Never overwrite an existing folder.** On a name collision, rename the new one and flag it in the slate. This is the one irreversible failure mode left — a silent overwrite destroys a working skill with an untested one.

### Retirement nomination

Because nothing gates installation anymore, every run must also nominate **one existing skill for retirement**. The library has a working size; past it, descriptions crowd each other and triggering degrades across the board. Growth without pruning is how a library stops firing.

Nominate on these signals, in order:
- **Superseded** — a newer skill covers its territory better
- **Never fires** — its trigger phrases don't match anything Tyler actually types
- **Absorbed** — its content belongs as a section inside a neighbor
- **Below the standard** — it describes rather than enacts

Name one, give the signal and one sentence of evidence. If nothing genuinely warrants retirement, say that plainly rather than manufacturing a nominee — a forced retirement is worse than a crowded library. Tyler decides; this skill only nominates.

### Run log

Write `.claude/skills/_runs.md` and append one dated block per run:

```
## <date>
Regions surveyed: <list>
Installed: <five names>
Retirement nominated: <name> — <signal>
Deleted by Tyler since last run: <names, or none>
```

Read this file at the start of Step 1. Do not rebuild something Tyler deleted after a previous run — a deletion is a verdict. If context has genuinely changed enough to reopen it, say which change reopened it and let him decide.

---

## Step 6: Present the slate

Use this exact structure:

```
## Library map
<2–4 lines naming the regions currently covered, which are thin, which are
empty, and the overall shape>

## The five

### 1. <skill-name>
**Enacts:** <the open loop it closes, one line>
**Produces:** <the artifact that exists afterward>
**Fires on:** <2–3 literal phrases>
**Nearest existing:** <skill> — <one line on how they stay distinct>
**Region:** <region> | **Score:** <n>/10

### 2–5. <same>

## Not proposed
<2–3 candidates that scored well but failed a gate, each with the reason. Where
a failure was namespace overlap, name the existing skill that should absorb the
need instead.>

## Nominated for retirement
<one existing skill, the signal, one sentence of evidence — or "none warranted"
with a reason>

## Installed
<paths written, and the note that they fire on next session load>

## Next
<The single next physical action, one line.>
```

### Worked example of the output

```
## Library map
Authority work and jurisdictional are the deepest regions — well covered, close
to saturated. Practice mechanics is thin: research is handled, but the artifacts
that leave the office aren't. Market structure covers scanning but not the
record after a decision. Household and meta are covered. The empty seat is the
seam between authority work and practice mechanics.

## The five

### 1. notice-reply-drafter
**Enacts:** correspondence arrives, three lookups happen by hand, nothing is
drafted until the fourth step
**Produces:** a client-ready reply letter with the authority already cited
**Fires on:** "draft a response to this notice", "reply to this CP", "client got
a letter"
**Nearest existing:** the authority-research skill — that one answers whether a
position holds; this one writes what goes in the envelope
**Region:** Practice mechanics | **Score:** 10/10

[...four more, same shape]

## Not proposed
- A general state-tax lookup skill. Scored 8 but failed namespace clearance
  outright against the existing state skill — no request separates them. The
  capability it wanted belongs in that skill's body as a new section.
- A full multi-stage planning system. Delta 4, but sprint fit 0. Narrowed
  version is proposal #4; the full version isn't buildable as one skill.

## Nominated for retirement
The older summarizing skill in the meta region — signal: absorbed. Everything it
does is now a section inside two newer skills, and its description overlaps both.

## Installed
Five folders written to the Vault and to the active skills directory. They fire
on next session load.

## Next
Restart the session and type "draft a response to this notice" to test #1.
```

---

## Aesthetic clause

These are objects Tyler will live with. Build them the way Koenig built Case Study #22 — the structure *is* the decoration.

Concretely:

- **No decorative sections.** If a heading has nothing load-bearing under it, delete the heading.
- **Restraint over completeness.** A skill that does one thing exactly beats one that does four adequately. When torn between adding a capability and keeping the shape clean, keep the shape.
- **The frame shows.** Steps numbered, sequence visible, nothing important buried in prose.
- **Warmth in the accents only.** A well-chosen name and one good sentence at the top. Calm everywhere else.
- **Vocabulary carries weight or it goes.** Latin, Wyckoff terms, IAACC structure, Fibonacci intervals — use them where they do actual work, never as ornament. A term used decoratively is worse than a plain word, because it implies a precision that isn't there.
- **Length is a ceiling, not a target.** A beautiful skill reads like it couldn't have been shorter.

---

## Failure modes of this skill itself

Watch for these while running it. Each one produces output that looks like success:

- **Region drift.** Five candidates from the deepest region because that's where the gaps are legible. The diversity constraint exists for exactly this; enforce it even when the tax candidates are objectively better that run.
- **Delta inflation.** Scoring a candidate 4 because the subject is interesting rather than because the output is an artifact. Re-read the calibration table when a score feels generous.
- **Survey skipping.** Proposing without reading existing bodies, then discovering the overlap after the folders are written. The survey is cheap; the collision is not.
- **Slate padding.** Reaching five by including a candidate that scored 4. Return four and say so.
- **Compliment as output.** The slate is not a presentation of how well the library is doing. If the honest finding is that the library is already dense and the best remaining candidates are marginal, that is the finding — say it and return two.
- **Recursive drift.** This skill can propose skills that propose skills. One meta-layer is enough; do not propose another generator.

---

## Rules

- Five per run. Fewer if the pool is honestly thin — never more.
- At least three regions represented.
- Enactment delta below 3 is a cut, regardless of total score.
- Every proposal fully written before it's presented. No stubs, no outlines.
- Namespace clearance is a hard gate, and now the only one. An overlapping skill is worse than no skill.
- Install live, to the Vault and the active skills directory both.
- Never overwrite an existing skill folder. A silent overwrite is the one irreversible failure.
- Nominate one skill for retirement every run, or state that none is warranted.
- A skill Tyler deleted after a previous run does not come back.
- Report "Not proposed" honestly. The rejects define the edge of the adjacent possible more sharply than the accepts do.
- Append to the run log. Read it first.
- End with exactly one next action. Do not stack.
