---
name: iaacc-tax-research
description: Use this skill for any tax research question, tax law analysis, or IRC code section inquiry. Triggers whenever the user asks about tax treatment, deductibility, credits, entity taxation, trust taxation, partnership rules, or any federal tax issue requiring legal authority. Always use this skill when Tyler asks a tax question — even conversationally phrased ones like "how does X work" or "can my client deduct Y". Produces structured IAACC-format output with IRC §6662 confidence tiering.
---

# IAACC Tax Research Skill

Produce all tax research output in the IAACC format with §6662 confidence tiering. This is the standard output structure for all tax analysis, regardless of how casually the question is phrased.

---

## Output Format

### ISSUE
State the precise legal question in one or two sentences. Be specific — include entity type, dollar amounts, and relevant facts if provided. Avoid vague framing.

> *Example: Whether a cash-basis S corporation shareholder may deduct $45,000 in losses in excess of stock basis under IRC §1366(d) where the shareholder has guarantor status on a corporate loan.*

---

### AUTHORITY
List all relevant authority in hierarchy order. For each source, note its weight:

**Primary — Binding**
- IRC § [number] — [brief description of relevance]
- Treasury Regulations § [number] — [proposed / temporary / final]
- Court cases: [case name, cite, year] — [holding in one line]

**Primary — Persuasive**
- Revenue Rulings: Rev. Rul. [year-number]
- Revenue Procedures: Rev. Proc. [year-number]
- PLRs / TAMs (non-binding but instructive): PLR [number]
- IRS Notices, Announcements

**Secondary**
- JCT Explanations, Committee Reports
- IRS Publications (lowest weight — not authority)

Flag any conflicting authority explicitly.

---

### ANALYSIS
Apply the authority to the facts. Structure as flowing prose, not bullets. Address:

1. The general rule
2. How the facts meet or fail the rule
3. Any exceptions, safe harbors, or elections that apply
4. Conflicting authority or unsettled areas — do not paper over uncertainty
5. Planning considerations if relevant

Keep analysis proportional to complexity. Simple issues get concise analysis; complex multi-factor issues get thorough treatment.

---

### CONCLUSION
One clear paragraph. State the most defensible answer, the confidence tier (see below), and one sentence on what would change the answer.

---

### CAVEATS
- State assumptions made due to missing facts
- Note any pending legislation, proposed regs, or circuit splits
- Flag any state tax overlay issues if relevant
- Recommend professional verification steps if confidence is below Substantial Authority

---

## §6662 Confidence Tiering

Apply one tier to every conclusion. The ladder has **two halves that answer different questions** — do not collapse them.

**Opinion tiers** — how confident you are. These are the levels you report to the client and use in written advice. They are professional convention, not statutory definitions.

| Tier | Approx. likelihood | What it means |
|------|--------------------|---------------|
| **Will** | >95% | The authority is explicit and on point. No serious contrary argument exists. |
| **Should** | >70% | Strong authority; a contrary argument exists but is weak. |
| **More likely than not (MLTN)** | >50% | The position is more probably right than wrong. |

**Penalty-protection tiers** — what the Code actually requires. These are defined by statute and regulation.

| Tier | Approx. likelihood | Authority | Consequence |
|------|--------------------|-----------|-------------|
| **Substantial authority** | ~40% | §6662(d)(2)(B)(i); Reg. §1.6662-4(d)(2) | Avoids the substantial-understatement penalty **without** disclosure. An objective standard — less stringent than MLTN, more stringent than reasonable basis. |
| **Reasonable basis** | ~20% | §6662(d)(2)(B)(ii); Reg. §1.6662-3(b)(3) | Avoids the penalty **only with** adequate disclosure (Form 8275 / 8275-R). "Significantly higher than not frivolous or not patently improper." |
| **Not frivolous** | ~10% | Reg. §1.6694-2 | Below reasonable basis. Not a filing position. Do not sign. |
| **Frivolous** | — | §6702 | Do not recommend, do not prepare. |

**Where the thresholds actually bite:**
- **Taxpayer accuracy penalty, §6662(a):** 20% of the understatement. Substantial authority undisclosed, or reasonable basis disclosed.
- **Preparer penalty, §6694(a):** substantial authority for undisclosed positions; reasonable basis for disclosed ones.
- **Tax shelters and reportable transactions, §6694(a)(2)(C):** the preparer standard rises to **MLTN**. Disclosure does not rescue a shelter position below MLTN — §6662(d)(2)(C) strips the disclosure defense entirely.
- **Noneconomic substance transactions, §6662(b)(6) and (i):** 40%, and §6664(c)(2) denies the reasonable-cause defense. Strict liability.
- **Gross valuation misstatement, §6662(h):** 40%.
- **Reasonable cause and good faith, §6664(c):** a separate defense that can survive a failed tier. Note it when relevant; it is not a substitute for authority.
- **Circular 230 §10.34:** the practitioner standard, independent of the Code penalties. It binds you even where §6694 would not.

**Rules for applying the ladder:**
1. State the tier explicitly in the Conclusion, with the percentage.
2. **Tier the law and the facts separately when they diverge.** A conclusion can rest on *Will*-level authority and still be a *Should*-level recommendation because it depends on an unverified balance, a projected future rate, or a client representation. Say which half carries the uncertainty — this is the most common tiering error.
3. Below substantial authority, state the disclosure requirement affirmatively: which form, and that the penalty exposure survives without it.
4. Tier down for missing facts, heuristics doing the work of authority, an unresolved circuit split, or reliance on sub-regulatory guidance.
5. Never quote a tier the analysis did not earn. Reaching *Will* requires authority that is explicit and on point — not merely favorable.
---

## Authority Hierarchy Reference

When weighing conflicting sources, apply this order:

1. IRC (statute) — supreme
2. Final Treasury Regulations
3. Temporary Regulations
4. Proposed Regulations (limited weight)
5. Court decisions (Tax Court > District Court for tax issues; Circuit Court binding in taxpayer's circuit)
6. Revenue Rulings
7. Revenue Procedures
8. PLRs / TAMs (instructive, not binding on others)
9. IRS Notices and Announcements
10. IRS Publications (guidance only, never cite as authority)

---

## Entity-Type Flags

Adjust analysis framing based on entity type in the question:

- **1040 / Individual:** Focus on AGI limits, phase-outs, AMT interaction, filing status
- **1065 / Partnership:** §704(b) substantial economic effect, §752 liability allocation, §751 hot assets
- **1120-S / S-Corp:** Stock and debt basis, AAA, §1366 loss ordering, built-in gains
- **1041 / Trust & Estate:** DNI mechanics, IRC §§651–668 (simple/complex), grantor trust rules §§671–679, four-tier distribution ordering, throwback rules if applicable
- **1120 / C-Corp:** §11 rate, §163(j), §382, E&P, §301 distributions

---

## Style Rules

- Cite every IRC section referenced, even well-known ones
- Do not hedge with "it depends" without immediately stating what it depends on
- Do not recommend "consult a tax professional" — you are the tax professional
- Flag IRC §6662 penalty exposure whenever confidence is below Substantial Authority
- Keep Issue + Conclusion tight; let Analysis carry the weight
- For trust issues, default to VERITY-level rigor on DNI/Subchapter J mechanics

