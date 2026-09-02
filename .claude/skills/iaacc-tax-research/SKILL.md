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

Apply one of these tiers to every conclusion:

| Tier | Standard | Weight of Authority Required |
|------|----------|------------------------------|
| **Substantial Authority** | ~40% or greater likelihood | Statute + reg or case law support; no dominant contrary authority |
| **Reasonable Basis** | ~25–35% | Some authority supports position; more likely wrong than right |
| **Colorable Claim** | <25% | Arguable but weak; disclose on return; penalty exposure without disclosure |
| **No Authority** | Frivolous | Do not recommend |

Always state the tier explicitly in the Conclusion section. If Substantial Authority cannot be reached, note disclosure requirements under §6662(d) and Reg. §1.6662-4.

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

