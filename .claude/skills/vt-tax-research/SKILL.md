---
name: vt-tax-research
description: Use this skill for any Vermont tax question — return mechanics, residency, MFS/MFJ elections, property tax credit (HS-122), household income (HI-144), nonresident/part-year allocation, or any VT-specific issue. Triggers whenever the user mentions Vermont, VT, IN-111, IN-112, IN-113, IN-114, HS-122, HI-144, PR-141, or asks about a VT return. Always use this skill when Tyler asks a VT question — even conversationally phrased ones like "does my client need to file VT" or "how does VT handle X". Produces structured IAACC-format output with §6662 confidence tiering, adapted for Vermont authority hierarchy.
---

# VT Tax Research Skill

Produce all Vermont tax research output in the IAACC format with confidence tiering. This is the standard output structure for all VT tax analysis, regardless of how casually the question is phrased. Mirrors the federal IAACC rail with VT-specific authority and issue flags.

---

## Output Format

### ISSUE
State the precise legal question in one or two sentences. Include filing status, residency status, dollar amounts, and tax year. VT issues are often residency-sensitive, so always pin down domicile and statutory residence facts.

> *Example: Whether a VT-domiciled taxpayer who worked remotely from NH for 8 months in 2024 must include W-2 wages in VT income under 32 V.S.A. §5823(a)(1), and whether the convenience-of-employer rule applies.*

---

### AUTHORITY
List all relevant authority in VT hierarchy order. For each source, note its weight:

**Primary — Binding**
- **32 V.S.A. §[number]** — Vermont Statutes Annotated, Title 32 (Taxation and Finance) — supreme state authority
- **Vermont Regulations** — codified at CVR (Code of Vermont Rules), particularly CVR 10-060-005 through 10-060-007
- **Vermont Supreme Court decisions** — binding statewide
- **Vermont Superior Court — Civil Division (formerly Tax Appeals)** — binding on parties, persuasive elsewhere

**Primary — Persuasive**
- **VT Department of Taxes Technical Bulletins (TB-#)** — agency interpretation, high practical weight
- **VT Department of Taxes Fact Sheets (FS-#)** — agency guidance
- **VT Department of Taxes Rulings** — taxpayer-specific but instructive

**Secondary**
- VT Tax Department instructions (IN-111, HS-122, etc.) — guidance only
- VT Tax Department FAQ pages — lowest weight
- Federal authority where VT conforms (always check conformity date)

**Conformity flag:** VT generally conforms to the IRC as of a fixed date set by the legislature each year. Always verify the current conformity date (32 V.S.A. §5824) before relying on federal treatment. Federal changes after the conformity date are NOT automatically VT law.

---

### ANALYSIS
Apply VT authority to the facts. Structure as flowing prose, not bullets. Address:

1. The VT general rule (cite statute first, then reg, then TB)
2. How VT conformity (or decoupling) from federal law affects the answer
3. How the facts meet or fail the rule
4. Residency overlay if relevant — domicile vs statutory residence under 32 V.S.A. §5811(11)
5. Allocation/apportionment mechanics for part-year and nonresident filers (IN-113)
6. Any VT-specific elections (MFS-on-VT, property tax credit, etc.)
7. Conflicting authority or unsettled areas — do not paper over uncertainty

---

### CONCLUSION
One clear paragraph. State the most defensible answer, the confidence tier, and one sentence on what would change the answer. Note any required disclosures or attached schedules (IN-112, IN-113, IN-114).

---

### CAVEATS
- State assumptions made due to missing facts (domicile, days present, source of income)
- Note current VT-federal conformity date and any decoupling that affects the answer
- Flag interaction with federal return if VT MFS election or recomputation is in play
- Flag interaction with property tax credit (HS-122/HI-144) if household income is implicated
- Recommend professional verification steps if confidence is below Substantial Authority

---

## §6662 Confidence Tiering (adapted for VT)

VT does not have its own codified penalty standard mirroring federal §6662, but 32 V.S.A. §3202 imposes negligence and substantial understatement penalties. Use the federal tiering as a practical proxy:

| Tier | Standard | Weight of Authority Required |
|------|----------|------------------------------|
| **Substantial Authority** | ~40% or greater likelihood | Statute + reg or TB support; no dominant contrary authority |
| **Reasonable Basis** | ~25–35% | Some authority supports position; more likely wrong than right |
| **Colorable Claim** | <25% | Arguable but weak; consider disclosure |
| **No Authority** | Frivolous | Do not recommend |

State the tier explicitly in the Conclusion section.

---

## VT Authority Hierarchy Reference

When weighing conflicting sources, apply this order:

1. 32 V.S.A. (Vermont Statutes) — supreme
2. Vermont Regulations (CVR)
3. Vermont Supreme Court decisions
4. Vermont Superior Court decisions (Civil Division, tax docket)
5. VT Tax Department Technical Bulletins
6. VT Tax Department Fact Sheets and Rulings
7. VT Tax Department Form Instructions
8. VT Tax Department FAQ (guidance only)

---

## VT Issue Flags — Common Triggers

### Residency (32 V.S.A. §5811(11))
Two-track test:
- **Domicile** — common-law domicile in VT (intent + physical presence)
- **Statutory residence** — maintains permanent place of abode in VT AND spends >183 days in VT during the tax year

A taxpayer can be a VT resident under either prong. Domicile is sticky — requires affirmative abandonment + new domicile elsewhere. Statutory residence is mechanical day-counting.

### Part-Year and Nonresident (IN-113)
- Part-year: file IN-111 with Schedule IN-113 allocating income to VT period
- Nonresident: file IN-111 with Schedule IN-113 allocating VT-source income only
- VT-source income includes: VT real property, VT-located business, services performed in VT, VT pass-through income
- **No convenience-of-employer rule in VT** — wages allocated based on where services actually performed (unlike NY)

### Filing Status — MFS on VT when MFJ Federal (32 V.S.A. §5822)
Available election when one spouse is a nonresident or part-year resident. Mechanics:
1. Recompute hypothetical federal MFS returns for each spouse
2. Use those recomputed federal figures as starting point for VT MFS returns
3. File two separate VT IN-111s
4. Often beneficial when one spouse has no VT-source income — prevents pulling nonresident spouse's income into VT calculation

Flag: this is a recomputation, not an actual federal MFS filing. Federal return stays MFJ.

### VT Income Starting Point (32 V.S.A. §5811(21))
VT taxable income = **federal taxable income** (NOT AGI), with VT-specific additions and subtractions on Schedule IN-112:

**Common additions:**
- Interest on non-VT state/municipal bonds
- Bonus depreciation decoupling (VT does not conform to federal bonus depreciation under §168(k))
- §199A QBI deduction addback (VT does not allow the federal QBI deduction)
- State income tax deduction (if itemized federally)

**Common subtractions:**
- Interest on US obligations
- VT municipal bond interest
- Social Security (partial, income-tested under 32 V.S.A. §5830e)
- Military retirement pay (income-tested exclusion)
- Capital gains exclusion (40% of net adjusted long-term gain on certain assets, capped — 32 V.S.A. §5811(21)(B)(ii))

### Credits
- **Income tax paid to other states** (32 V.S.A. §5825) — Schedule IN-117; limited to VT tax on same income; critical for cross-border NH/NY/MA workers
- **Earned Income Tax Credit** — 38% of federal EITC
- **Child Tax Credit** — VT CTC, $1,000/child under 5, income-phased
- **Renter Credit** — formerly Renter Rebate, claimed on Schedule HI-144 + PR-141

---

## HS-122 and HI-144 — Property Tax Credit Decision Tree

**Quick answer — does filing HS-122 require HI-144?**
- **Section A only (Homestead Declaration):** NO. Not income-tested.
- **Section B (Property Tax Credit Claim):** YES. HI-144 required to compute household income.
- **PR-141 (Renter Credit):** YES. HI-144 required.

This is the single most-missed VT filing for owner-occupants. Two separate forms with two separate purposes that share Form HI-144.

### HS-122 — Homestead Declaration + Property Tax Credit Claim
**Two parts on one form:**

**Section A — Homestead Declaration (REQUIRED for all VT homeowners)**
- File EVERY year by **April 15** (extended deadlines available but with penalty)
- Declares the property as the homestead (owner-occupied principal residence on April 1)
- Triggers the homestead education property tax rate instead of the nonresidential rate — failure to file means the higher nonresidential rate applies
- Required even if not claiming the property tax credit
- Late filing penalty: $15 or 3% of education tax (whichever greater); after Oct 15, becomes ineligible and taxed at nonresidential rate

**Section B — Property Tax Credit Claim (OPTIONAL, income-tested)**
- File if household income ≤ $128,000 (TY2024 threshold — verify current year)
- Reduces VT property tax owed based on income and property value
- Requires Schedule HI-144 attached

### HI-144 — Household Income Schedule
**Always filed with HS-122 Section B and/or PR-141 (Renter Credit).**

"Household income" is broader than VT AGI — includes:
- All income of all household members (not just filer/spouse)
- Social Security (full amount, not just taxable portion)
- Child support received
- Gifts > $6,500 from non-household members
- Workers' comp, VA benefits, unemployment
- Inheritance income
- Cash public assistance

Common miss: adult children living at home — their income gets pulled into household income calculation, often pushing the client over the credit threshold.

### Filing Decision Tree

```
Is the client a VT homeowner who occupied the property on April 1?
├─ YES → File HS-122 Section A (mandatory, annual)
│        Is household income ≤ $128,000 (verify current year)?
│        ├─ YES → Also file HS-122 Section B + HI-144 (claim credit)
│        └─ NO  → Section A only
│
└─ NO → Is the client a VT renter?
        ├─ YES → Eligible for Renter Credit?
        │        File PR-141 + HI-144
        └─ NO → No HS-122, no HI-144 required
```

### Deadline Cheat Sheet
| Form | Deadline | Late Filing |
|------|----------|-------------|
| HS-122 Section A (Homestead) | April 15 | Penalty + accepted through Oct 15; after Oct 15, parcel taxed nonresidential |
| HS-122 Section B (Credit) | April 15 | Can file through Oct 15 with penalty |
| HI-144 | Same as HS-122/PR-141 it attaches to | Same |
| PR-141 (Renter Credit) | April 15 | Through Oct 15 with penalty |

### Common Errors to Flag
- Filing HS-122 when client moved out before April 1 → not entitled, may need to amend prior years
- Missing HI-144 income for non-tax-dependent adult household members
- Forgetting Section A when property was newly purchased mid-year (file for next year's declaration)
- Treating the property tax credit as income on federal return — it's a property tax reduction, not income

---

## Common VT Forms Reference

| Form | Purpose |
|------|---------|
| IN-111 | VT income tax return (resident, part-year, nonresident) |
| IN-112 | VT tax adjustments and credits (additions/subtractions to federal TI) |
| IN-113 | Income allocation for part-year and nonresident filers |
| IN-114 | Estimated tax payment voucher |
| IN-116 | Income tax payment voucher |
| IN-117 | VT credit for tax paid to other states |
| IN-119 | VT tax credits (CTC, EITC, business credits) |
| IN-151 | Application for extension of time to file |
| HS-122 | Homestead declaration + property tax credit claim |
| HI-144 | Household income schedule |
| PR-141 | Renter credit claim |
| BI-471 | Business income tax return (1065/1120-S equivalent) |
| FIT-161 | Fiduciary income tax return (1041 equivalent) |
| WH-435 | Quarterly withholding for nonresident pass-through owners |

---

## Style Rules

- Cite 32 V.S.A. section for every VT statutory point
- Cite TB number for every agency interpretation relied on
- Always verify current VT-federal conformity date before relying on federal treatment
- Do not assume federal post-conformity-date changes flow to VT
- Do not hedge with "it depends" without immediately stating what it depends on
- Do not recommend "consult a tax professional" — you are the tax professional
- For property tax credit questions, always run the HS-122 / HI-144 decision tree explicitly
- For residency questions, always pin down both domicile AND statutory residence facts before answering
- For cross-border workers (NH/NY/MA), always flag IN-117 reciprocity mechanics
- For pass-through entities with VT-source income, flag WH-435 withholding obligation
