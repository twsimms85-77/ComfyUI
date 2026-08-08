---
name: fed-tax-pulse
description: Use this skill to produce a weekly digest of new federal tax guidance — proposed and final regulations, Treasury Decisions, Revenue Rulings, Revenue Procedures, Notices, and Announcements — scored for relevance to Tyler's solo NH tax practice, with a ready-to-paste Blue J research prompt drafted for each item worth a deep dive. Triggers on the scheduled Monday morning run and on manual requests like "run the fed tax pulse", "what's new from Treasury this week", "any new IRS guidance", or "what regs dropped".
---

# Fed Tax Pulse — Weekly Federal Guidance Digest

Produce a weekly digest of new federal tax guidance and write it to the Vault as a dated note. Same voice as the Tax Court digest: plain English a smart client could follow, with the code sections and operative rule a practitioner needs.

The point of this skill is **not** to summarize everything. It is to convert a week of federal guidance into **at most three questions worth taking into Blue J**, each with the prompt already written. Everything else gets one line and a link.

This skill is fired by a scheduled Monday-morning entry and can also be run on demand.

---

## Data sources

Two independent sources, fetched by `scripts/fetch_fed_tax.py`. Neither needs an API key.

- **Federal Register** — `api.federalregister.gov`, filtered to IRS and Treasury, types `RULE` (final regs / Treasury Decisions), `PRORULE` (proposed regs), and `NOTICE`. This source is stable and well-documented; treat it as the backbone of the digest.
- **Internal Revenue Bulletin** — parsed from `irs.gov/irb`. Catches Rev. Ruls., Rev. Procs., Notices, Announcements, and T.D.s. The IRB has **no JSON API**, so this path is a tolerant HTML parse and is inherently more fragile.

**Dependency:** `requests`. Install once on the runner: `python -m pip install requests`.

### Before the first scheduled run

Run the connectivity probe once and confirm both sources answer:

```
python scripts/fetch_fed_tax.py --check
```

Expect `federal_register: OK` and `irb: OK`. If the IRB line says `reachable but nothing parsed`, the page layout changed — the Federal Register half still works, so the digest degrades rather than dies. Fix the parser in `IRB_LINK_RE` / `IRB_ITEM_RE` when that happens.

### Running the fetch

```
python scripts/fetch_fed_tax.py --state <watermark.json> --out <new.json>
```

- `--state` — watermark path (JSON list of already-digested item ids). **Read-only here.**
- `--out` — where to write the JSON (omit for stdout).
- `--since-days N` — Federal Register lookback (default 8, one day of overlap on a weekly cadence).
- `--bulletins N` — how many recent IRB issues to scan (default 2).
- `--source federal_register|irb|all` — restrict to one source when debugging.
- `--check` — probe both sources and exit.

Per new item the fetch emits: `id`, `source`, `designator`, `kind`, `title`, `abstract`, `action`, `date`, `effective_on`, `comments_close_on`, `url`, `pdf_url`, `docket_ids`, `rins`, `cfr_references`, `agencies`.

It also emits an `errors` array. **If `errors` is non-empty, say so in the note and in the chat summary** — a silent partial run is worse than a loud one.

### Watermark discipline

Identical to the Tax Court digest. The fetch reads the watermark and never writes it. **Update the watermark only after the week's note is successfully written**, so a crash never silently drops an item. Late-posted guidance is caught on the next run rather than missed.

Default state file: `01 - Tax & CPA\Fed Tax Pulse\.state\watermark.json` (create if absent).

---

## Triage — the part that matters

Most weeks produce 10–40 raw items and almost none of them matter to a solo NH 1040/passthrough shop. Sort every item into one of three buckets.

**Bucket A — Deep dive (0–3 per week, hard cap 3).**
Something that changes a position, a due date, an election, or a number Tyler will actually use this season. Gets a full card *and* a drafted Blue J prompt.

**Bucket B — Worth knowing (any number).**
Real guidance in an area he touches, but no action needed. One line: designator, plain-English what-it-does, link.

**Bucket C — Noise.**
Excise, international-only, employee plans he doesn't serve, procedural minutiae, corrections to items already digested. **Do not list these individually.** Collapse to a single count: *"18 other items (excise, international, EP/EO) — not listed."*

Be ruthless about the cap. Three well-framed questions he actually researches beats twenty he skims.

### Practice profile (scoring anchor)

Solo NH shop; returns are 1040 / 1065 / 1041 / 1120-S.

**Lean Bucket A:**
- Trusts & estates mechanics — §643 / DNI, fiduciary income, distributions
- Passthrough basis, §199A, §704(b), §752, S-corp basis and AAA
- Multi-state exposure — VT / ME / MA / NY / CA
- Roth / RMD interplay, retirement distributions
- Individual credits and the tangible property regs (§263(a), §168)
- Anything with a **comment deadline** or **effective date** inside 90 days
- Inflation-adjusted figures and AFRs he keys into returns

**Lean Bucket C:**
- Excise, employment tax for large employers, international reporting he doesn't file
- Employee plans / exempt organizations
- Pure agency housekeeping, corrections, technical amendments

---

## Card format (locked) — Bucket A only

```
### <Designator> — <short plain title>
**<Kind>** · published <YYYY-MM-DD> · <effective / comments close, if any>

**Code sections:** <central §§ first> — *also touched:* <secondary §§>

**What changed:** <2–3 plain sentences a smart client could follow.>

**Who it hits:** <which of Tyler's client types, named concretely.>

**Relevance: N/10** — <one-line why, anchored to the practice.>

**Ask Blue J:**
> <the drafted prompt — see below>

[source](<url>)
```

### Drafting the Blue J prompt — the whole point of this skill

For every Bucket A item, write a prompt Tyler can paste into Blue J without editing. It must carry, in this order:

1. **A concrete fact pattern**, not a hypothetical. Invent plausible specifics drawn from his practice profile — entity type, state, method of accounting, year, dollar magnitude. Better a specific fact pattern he adjusts than a vague one he has to build from scratch.
2. **The precise question**, naming the guidance by designator.
3. **The adversarial follow-up**, always: *"What authority cuts against this, and what is the strongest argument the Service would make?"*
4. **The deliverable ask** — memo, client email, or bullets.

Format it as a single block quote he can copy in one motion.

> **Example.** For a proposed reg amending the §1.263(a)-3 improvement standards:
>
> "A NH single-member LLC (disregarded, cash basis) owns a 12,000 sq ft commercial building placed in service in 2019. In 2026 it spent $180,000 replacing the entire HVAC system — 4 rooftop units, all of them. No partial disposition election was made on the prior units. Under REG-XXXXXX-XX as proposed, does this remain a capitalizable improvement to the HVAC building system, or does the proposed change to the major-component test alter the result? What authority cuts against my position, and what is the strongest argument the Service would make? Then draft this as a research memo."

Anchor the invented facts to the guidance's actual subject matter. Never invent a designator, an effective date, or a code section — those come from the fetch or from the source document, or they don't appear.

---

## Output — write to the Vault

`C:\Dellcockpit home\Tyler's Vault\01 - Tax & CPA\Fed Tax Pulse\<YYYY-MM-DD>.md`

(Create the `Fed Tax Pulse` folder if absent.)

```markdown
# Fed Tax Pulse — week of <YYYY-MM-DD>

<N> new item(s). <M> worth a deep dive.   <!-- or: "Quiet week — nothing worth a deep dive." -->

## Deep dive
<Bucket A cards, highest Relevance first>

## Worth knowing
- **<Designator>** — <one plain-English line>. [source](<url>)

## Not listed
<count> other items (<categories>).

---
*Sources: Federal Register API (IRS + Treasury), Internal Revenue Bulletin. Window: <window_start> to <today>. Generated <timestamp ET>.*
<!-- if errors non-empty: -->
*⚠️ Partial run — <error text>. Items from the failed source are NOT in this digest and were NOT watermarked.*
```

If nothing clears Bucket A, still write the note with "Quiet week" so the trail is unbroken.

**On a partial run, watermark only the items from sources that actually succeeded.** Never watermark a source that errored — that would silently swallow the week.

---

## Run summary

Report to Tyler in chat, 1–2 lines: the week, count of new items, how many deep dives, the top item's designator, and a link to the note. If there were errors, lead with that.

## Rules

- Plain English in "What changed"; practitioner precision in code sections and designators.
- Never invent a designator, effective date, comment deadline, or code section.
- Hard cap of 3 deep dives. If week five things qualify, pick the three with the nearest deadlines or widest client impact and demote the rest to Bucket B.
- Every Bucket A card ships a paste-ready Blue J prompt. A card without one is incomplete.
- Always include the adversarial follow-up in the drafted prompt.
- Watermark only after a successful write, and only for sources that succeeded.
- This skill orients and queues. For a binding read on a specific client, hand off to `iaacc-tax-research`. To file a Blue J answer once Tyler has run it, hand off to `bluej-capture`.
