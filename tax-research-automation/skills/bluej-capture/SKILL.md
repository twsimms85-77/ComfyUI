---
name: bluej-capture
description: Use this skill whenever Tyler pastes in an answer, memo, or conversation from Blue J (or any AI tax research tool) and wants it verified, restructured, and filed. Triggers on "capture this from Blue J", "here's what Blue J said", "file this research", "log this Blue J answer", or any paste of AI-generated tax analysis that needs to become a permanent, defensible work-product note. Verifies the citations, converts the answer to IAACC format with §6662 tiering, records where Tyler disagreed, tags affected clients, and writes a dated note to the Vault.
---

# Blue J Capture

Turn a Blue J answer into a permanent, defensible piece of work product.

A Blue J conversation is ephemeral and lives inside Blue J. This skill converts it into a vault note that survives the subscription, carries Tyler's own judgment on top of the machine's, and can be pulled up three years later when a return is under exam.

**The core discipline: the note must separate what Blue J said from what Tyler concluded.** Those are different things, and the delta between them is the professional judgment that makes the file defensible.

---

## Input

Tyler pastes any of: a single Blue J answer, a full conversation, a generated memo, or a client email draft. He may or may not say what the underlying question was.

If the question isn't obvious from the paste, **ask for it in one line** before proceeding — the ISSUE statement is the spine of the whole note and guessing it wrong wastes the capture.

If the paste came from a `fed-tax-pulse` or `tax-court-daily-digest` card, link back to that note.

---

## Step 1 — Verify before you restructure

Do not reformat an answer you haven't checked. Work through every authority Blue J cited:

| Check | What you're looking for |
|---|---|
| **Exists** | Is this a real code section, reg, ruling, or case? |
| **Says what it's claimed to say** | Does the cited authority actually support the proposition it's attached to? This is the failure mode that matters. |
| **Still good law** | Superseded ruling? Withdrawn reg? Reversed on appeal? Amended by later legislation? |
| **Right weight** | Is a Publication or PLR being leaned on as if it were binding? |
| **Right circuit** | Is a case binding on Tyler's taxpayers (1st Cir. / Tax Court) or merely persuasive? |
| **Currency** | Is the analysis running on a pre-amendment version of the section? |

Record the result of each check. Produce a **Citation audit** table in the note — every cite, verified or flagged.

Flag, never quietly fix. If a cite is wrong, the note says it was wrong. That record is worth more than a clean-looking memo.

**Where verification isn't possible** (no access to the source, paywalled, ambiguous), mark it `unverified` explicitly. Never mark something verified because it looks plausible.

---

## Step 2 — Restructure through IAACC

Hand the verified content to the `iaacc-tax-research` skill's format: ISSUE / AUTHORITY / ANALYSIS / CONCLUSION / CAVEATS, with a §6662 confidence tier on the conclusion.

Do not simply relabel Blue J's headings. Re-derive the structure:

- **ISSUE** — one or two sentences, entity type and dollar amounts included. Tighten whatever Blue J was answering into a precise legal question.
- **AUTHORITY** — in hierarchy order, with weight noted. Drop anything that failed Step 1, and say in CAVEATS that you dropped it.
- **ANALYSIS** — flowing prose. Surface any uncertainty Blue J papered over. AI answers systematically understate how unsettled a question is; if the area is genuinely contested, the note must say so.
- **CONCLUSION** — the most defensible answer, the tier, and one sentence on what would change it.
- **CAVEATS** — assumptions, missing facts, pending legislation, circuit splits, state overlay.

### Tier independently

Assign the §6662 tier yourself from the authority that **survived verification**. If Blue J stated or implied a confidence level, record it separately and note the difference:

> *Blue J framed this as well-settled. Tiering it at Reasonable Basis — the only on-point authority is a 1998 non-precedential decision and Rev. Rul. 2009-13 cuts the other way.*

That sentence is the most valuable line in the note.

---

## Step 3 — The judgment delta

A short, explicit section. This is what a reviewer or an examiner will actually read.

```
## Where I landed differently
- <what Blue J said> → <what I concluded> — <why>
```

If Tyler agrees with Blue J on every point, say so in one line: *"Concur in full; no departures."* Do not manufacture disagreement.

---

## Step 4 — Client crosswalk

Name the clients or client types this touches, and what to actually do:

```
## Client impact
- **<Client / type>** — <what changes for them> — <action: raise at planning meeting / amend / no action / watch>
```

If Tyler hasn't said which clients, list the **client types** from the practice profile rather than guessing at names. Never invent a client name.

Add `#followup` to any line with an action so it surfaces in the monthly rollup.

---

## Output — write to the Vault

`C:\Dellcockpit home\Tyler's Vault\01 - Tax & CPA\Research\<YYYY-MM-DD> — <short issue slug>.md`

```markdown
---
type: research
source: Blue J
date: <YYYY-MM-DD>
tier: <Substantial Authority | Reasonable Basis | Colorable Claim | No Authority>
sections: [<IRC §§>]
entities: [<1040 | 1065 | 1041 | 1120-S>]
status: <open | closed>
tags: [tax-research, blue-j]
---

# <Issue in a phrase>

## Citation audit
| Authority | Cited for | Verdict |
|---|---|---|
| IRC §<n> | <proposition> | ✅ verified |
| Rev. Rul. <n> | <proposition> | ⚠️ superseded by Rev. Rul. <n> |
| <case> | <proposition> | ❌ does not support — holding is <x> |
| <source> | <proposition> | ◻️ unverified — <why> |

## ISSUE
## AUTHORITY
## ANALYSIS
## CONCLUSION
## CAVEATS

## Where I landed differently
## Client impact

---
*Captured from Blue J <YYYY-MM-DD>. Verified <YYYY-MM-DD>. Prompt used: <one line, or link to the pulse card that generated it>.*
```

Frontmatter follows the vault's existing conventions — check `obsidian-vault-expert` if the taxonomy has moved.

---

## Step 5 — Close the loop

After writing, report in chat, 2–3 lines:
- The tier landed on, and whether it differs from Blue J's framing
- Any citation that failed verification
- The single highest-value follow-up action

If any cite failed Step 1, **say that first**. It is the most important thing in the run.

---

## Rules

- Never file an answer you haven't citation-checked. The verification *is* the value.
- Flag bad cites in the record; do not silently correct them.
- Mark `unverified` honestly — a plausible-looking cite is not a verified one.
- Tier from surviving authority, independently of what Blue J implied.
- Never invent a client name, a citation, or a holding.
- Do not recommend "consult a tax professional" — Tyler is the tax professional.
- The Blue J answer is an input, not the work product. The note is the work product.
