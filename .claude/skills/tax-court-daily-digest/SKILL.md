---
name: tax-court-daily-digest
description: Use this skill to produce a plain-English daily digest of newly filed U.S. Tax Court opinions, one card per opinion, scored for relevance to Tyler's solo NH tax practice. Triggers on the scheduled afternoon run (rides the 4:05 PM ET EOD rail) and on manual requests like "run the tax court digest", "any new Tax Court opinions today", or "digest today's Tax Court filings". Pulls from CourtListener, summarizes each opinion, and writes a dated note to the Vault.
---

# Tax Court Daily Digest

Produce a plain-spoken but practice-aware digest of new U.S. Tax Court opinions and write it to the Vault as a dated note. One card per opinion. Plain English a smart client could follow, but with the code sections and holding a practitioner needs.

This skill holds the **summarize-and-score logic**. It is fired by a scheduled cron entry (the same daily rail as the 4:05 PM ET EOD auto-logger) and can also be run on demand.

---

## Data source — CourtListener (implemented)

CourtListener carries U.S. Tax Court opinions. We use it instead of scraping DAWSON. The fetch is implemented in `scripts/fetch_tax_opinions.py` and runs **without any API token**:

- **Metadata** comes from the court's Atom feed: `https://www.courtlistener.com/feed/court/tax/` (no auth). Yields case name, citation, docket, filed date, opinion URL, and the PDF link.
- **Full opinion text** comes from the public opinion **PDF** (no auth), extracted with `pypdf`. (The opinion HTML page sits behind an anti-bot WAF, so the PDF is the reliable text source.)

**Dependency:** `pypdf` (pure-Python). Install once on the runner: `python -m pip install pypdf`.

### Running the fetch
```
python scripts/fetch_tax_opinions.py --state <watermark.json> --out <new.json>
```
- `--state` — path to the watermark (JSON list of already-digested opinion ids). Read-only here.
- `--out` — where to write the JSON of new opinions (omit for stdout).
- `--no-text` — metadata only (skips PDF download); useful for a quick "anything new?" check.
- `--max N` — how many recent feed entries to consider (default 25).

It emits, per **new** opinion, exactly the fetch contract the cards need:
`case_name`, `citation` ("not yet cited" if none), `opinion_type` (Regular / Memorandum / Summary), `docket_number`, `date_filed`, `opinion_url`, `pdf_url`, and `full_text` (the extracted opinion text — parse central vs. "also touched" code sections from this).

### Timing & de-dup (important)
The court posts opinions after **3:30 PM ET**, and CourtListener harvests with some lag — so the 4:05 PM ET run may not see everything same-day. To never miss or double-post:
- A **watermark** file holds the ids of already-digested opinions. The fetch reads it and emits only opinions **not** in it, regardless of filed date.
- The fetch does **not** modify the watermark. **This skill updates the watermark only after the day's note is successfully written** — so a crash never silently drops an opinion. A late-posted opinion is simply caught on the next run.
- Default state file: `01 - Tax & CPA\Tax Court Digest\.state\watermark.json` (create if absent).

---

## Card format (locked)

Render one card per opinion, in this exact structure:

```
### <Case Name> 
**<Citation>** · filed <YYYY-MM-DD> · <Opinion type: Regular / Memorandum / Summary>

**Code sections:** <central §§ first> — *also touched:* <secondary §§>

**The gist:** <2–3 plain sentences a smart client could follow.>

**Holding:** <What the court actually decided — the outcome and the rule applied.>

**Relevance: N/10** — <one-line why, anchored to Tyler's practice.>
```

Notes:
- **Code sections:** identify the section(s) the opinion actually turns on and list them first; list incidentally-cited sections under "also touched." If none, say "No specific IRC section central — <basis>."
- **The gist:** plain-spoken. No jargon dumps. 2–3 sentences.
- **Holding:** state the decision and the operative rule, not the procedural posture. Who won on what.
- Keep each card self-contained.

---

## Relevance scoring (judgment, not a formal rubric)

Score 1–10 by judgment against Tyler's practice profile. No formal rubric yet — anchor to the profile and give a one-line why.

**Practice profile:** solo NH shop; returns are 1040 / 1065 / 1041 / 1120-S.

**High relevance (lean 7–10):**
- Trusts & estates mechanics — §643 / DNI, fiduciary income, distributions
- Multi-state exposure — VT / NY / CA issues
- Roth / RMD interplay
- §30D (clean vehicle credit) and similar individual credits
- CP-notice / IRS correspondence-driven disputes

**Low relevance (lean 1–3):**
- Criminal tax matters
- Niche fact patterns unlikely to walk into a solo NH 1040/passthrough practice
- Pure procedural/jurisdictional rulings with no transferable rule

**Mid (4–6):** general business/passthrough or individual issues that could plausibly touch the practice but aren't in the high-relevance buckets.

The one-line why should name the hook ("DNI allocation on a complex trust — directly your §1041 work") or the reason it's low ("collection due process technicality, won't surface in your practice").

---

## Output — write to the Vault

Write a dated note:

`C:\Dellcockpit home\Tyler's Vault\01 - Tax & CPA\Tax Court Digest\<YYYY-MM-DD>.md`

(Create the `Tax Court Digest` folder if absent. Adjust the parent folder if Tyler prefers a different home.)

Note structure:

```markdown
# Tax Court Digest — <YYYY-MM-DD>

<N> new opinion(s).   <!-- or: "No new opinions today." -->

<cards, highest Relevance score first>

---
*Source: CourtListener (court: tax). Generated <timestamp ET>.*
```

Ordering: sort cards by Relevance descending so the most practice-relevant opinion is on top.

If there are no new (un-watermarked) opinions, still write the note with "No new opinions today." so the daily trail is unbroken — or skip writing and log it, per Tyler's preference (default: write the note).

---

## Run summary
After writing, report to Tyler in chat: the date, count of new opinions, and the single highest-relevance card's case name + score, with a link to the note. Keep it to 1–2 lines.

## Rules
- Plain English in the gist; practitioner precision in code sections and holding.
- Never invent a citation — if CourtListener hasn't assigned one, say "not yet cited."
- Score by judgment against the profile; always give the one-line why.
- De-dup against the watermark every run; catch late-posted opinions on the next run rather than missing them.
- This skill summarizes and orients. For a binding read on how a holding applies to a specific client, hand off to `iaacc-tax-research`.
