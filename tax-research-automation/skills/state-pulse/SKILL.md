---
name: state-pulse
description: Use this skill to produce a weekly digest of state tax developments across the states Tyler actually files in — NH, VT, ME, MA, plus NY and CA on the watchlist — scored for relevance to his solo NH practice. Triggers on the scheduled Friday run and on manual requests like "run the state pulse", "anything new from VT", "what changed in Massachusetts", or "state tax news this week". Reads each state's guidance page directly, filters hard, and writes a dated note to the Vault.
---

# State Pulse — Weekly Multi-State Digest

Blue J's content is federal-heavy — government sources plus Tax Notes. State coverage is the thinnest part of the platform, which makes it exactly the gap worth automating.

This skill covers the states Tyler files in. It is the **noisiest** of the three pulses and the one that most needs a hard filter: state revenue departments publish a great deal that matters only to large filers, specific industries, or in-state businesses he doesn't serve.

Fired by a scheduled Friday run; also available on demand.

---

## Sources

No Python script. State revenue sites have no common API and their HTML changes often, so a scraper here would rot faster than it earns. Fetch each page directly with WebFetch and read it.

| State | What to read | Why |
|---|---|---|
| **NH** | Dept. of Revenue Administration — news / what's new; Technical Information Releases | Home state. BPT / BET / I&D rates and thresholds, filing changes. |
| **VT** | Dept. of Taxes — news room; technical bulletins; fact sheets | Active VT work — see `vt-tax-research`. HS-122 / HI-144 / PTC changes are high value. |
| **ME** | Maine Revenue Services — **Maine Tax Alerts** (monthly, the single best state source of the four) | Nonresident and part-year allocation, conformity. |
| **MA** | Dept. of Revenue — **Technical Information Releases** and **Directives**; DOR news | Highest volume, and the most likely to matter for cross-border clients. |
| **NY, CA** | Watchlist only — check when a client-driven question is open | Occasional exposure; not worth a weekly sweep on their own. |

**One-time setup:** confirm each URL resolves before the first scheduled run, and record the working URLs in this table. Vermont and Maine in particular have reorganized their sites. If a page 404s, find the current equivalent and update this file rather than silently skipping the state — a state that quietly drops out of the digest is worse than one that visibly fails.

---

## Filter hard

State DORs publish constantly. Two buckets only.

**Bucket A — Matters (0–3, hard cap 3).**
Changes a rate, threshold, form, due date, election, or filing obligation for a **1040 / 1065 / 1041 / 1120-S** filer that Tyler plausibly serves. Full card.

**Bucket B — Everything else.**
Collapse to a count by state: *"NH 2, VT 5, ME 1, MA 11 — nothing actionable."*

### Straight to Bucket B

- Rates and rules for taxes he doesn't file: meals & rooms, tobacco, fuel, gross receipts on specific industries, unclaimed property
- Large-filer and combined-reporting mechanics
- Municipal / local property assessment procedure
- Administrative notices with no substantive change

### Lean Bucket A

- **Conformity** — a state decoupling from or conforming to a federal provision. Highest-value category by a wide margin; it silently changes returns.
- Residency, domicile, and part-year / nonresident **allocation** rules
- Personal income tax rates, brackets, standard deduction, credits
- Passthrough entity tax (PTET) elections, deadlines, and mechanics
- VT property tax credit / household income (HS-122, HI-144)
- New or retired forms, and any due-date change
- Anything with an effective date inside the coming filing season

---

## Card format (locked) — Bucket A only

```
### <ST> — <short plain title>
**<Document type + number, if any>** · <date> · effective <date or "on issuance">

**What changed:** <2–3 plain sentences.>

**Who it hits:** <which of Tyler's client types, concretely — e.g. "NH residents with VT rental income".>

**Federal interaction:** <conformity / decoupling / none — say which.>

**Relevance: N/10** — <one-line why.>

[source](<url>)
```

Include **Federal interaction** on every card. A state change that decouples from a federal provision is the one that quietly breaks a return, and it is the reason this digest exists.

Where a card raises a real open question, draft a Blue J prompt the same way `fed-tax-pulse` does — but note in the prompt that the state analysis needs verification against primary state authority, because Blue J's state coverage is thin. For VT specifically, hand off to `vt-tax-research` instead of Blue J; that skill knows the authority hierarchy.

---

## Output — write to the Vault

`C:\Dellcockpit home\Tyler's Vault\01 - Tax & CPA\State Pulse\<YYYY-MM-DD>.md`

```markdown
# State Pulse — week of <YYYY-MM-DD>

<M> item(s) worth attention.   <!-- or: "Nothing actionable this week." -->

## Matters
<Bucket A cards, highest Relevance first>

## Scanned, nothing actionable
NH <n> · VT <n> · ME <n> · MA <n>

## Not reached
<any state whose page failed to load — name it and say why>

---
*Sources: NH DRA, VT Dept. of Taxes, ME Revenue Services, MA DOR. Generated <timestamp ET>.*
```

**Always include a "Not reached" section when a source fails.** A silent gap in a weekly digest reads as "nothing happened," which is the one thing it must never imply.

---

## Run summary

One or two lines in chat: count of items that matter, the top one, any state that failed to load, and a link to the note.

## Rules

- Hard cap of 3 cards. State volume will tempt you past it; don't.
- Name the federal interaction on every card.
- Never invent a TIR, bulletin, or alert number.
- Report unreachable sources loudly; never let a failed fetch look like a quiet week.
- VT questions route to `vt-tax-research`, not Blue J.
- Multi-state framing questions route to `state-tax-landscape-out-of-state-preparer`.
