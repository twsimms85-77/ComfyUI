---
name: repair-regulations-test
description: Determine whether a building expenditure is a currently deductible repair or a capitalizable improvement under the IRS Tangible Property Regulations (§1.263(a)-3). Use this whenever a cost touches a building or building system — roofing, HVAC, plumbing, electrical, flooring, windows, structural work, restorations, renovations, tenant improvements, casualty repairs, or any maintenance/capitalization judgment call. Trigger even when the user just describes work done on a property and asks "is this deductible," "do I capitalize this," "repair or improvement," or pastes an invoice/scope-of-work. Runs the Step 1 (unit of property) → Step 2 (four hurdles) → Step 3 (mitigate) shortcut flow and returns an IAACC analysis with a §6662 confidence tier.
---

# Repair vs. Improvement — Tangible Property Regulations Analyst

## End goal

Hand the preparer a defensible repair-vs-capitalize answer that survives a §6662 look: the correct unit of property named, each capitalization trigger run in order, every available mitigation flagged, and a confidence tier attached. The objective is **the most defensible position on the facts** — not the deduction, not the capitalization. Follow the facts.

## Governing authority

- **§1.263(a)-3** — improvements to tangible property (the controlling reg)
- **§1.263(a)-3(e)** — unit of property; building + building systems
- **§1.263(a)-3(j)** — Betterment
- **§1.263(a)-3(k)** — Restoration
- **§1.263(a)-3(l)** — Adaptation to a new or different use
- **§1.263(a)-3(g)(2)** — removal costs
- **§1.263(a)-3(h)** — safe harbor for small taxpayers (SHST)
- **§1.263(a)-3(i)** — routine maintenance safe harbor (RMSH)
- **§1.263(a)-1(f)** — de minimis safe harbor (DMSH)
- **§1.168(i)-8** — partial disposition election
- **§179** — election to expense

> **Scope:** Buildings and building systems only. Tangible personal property and land improvements are **out of scope** for this flow — say so and stop if the UOP is one of those.

> **Bright-line warning (state this every time percentages are used):** The TPRs contain **no** numerical bright-line tests for betterment or restoration. The `10% / >20% / >40%` figures below are practitioner *heuristics* for triaging a fact pattern, not regulatory thresholds. They lower the §6662 tier when they are the only thing carrying the conclusion. Never present them as the rule.

---

## STEP 1 — Identify the UOP ("what is *it*?")

Before any test, name the unit of property. The UOP determination usually controls the outcome — a cost that is huge against a single window is trivial against the whole building system.

**Is *it* a building system?** The nine systems, each its own UOP:
- HVAC
- Plumbing
- Electrical
- Escalators
- Elevators
- Fire protection & alarm systems
- Security systems
- Gas distribution systems
- (Other enumerated systems)

**If not a system → *it* is the Building** — everything else in the building.

Record which one. Every test in Step 2 is run *against this UOP*, not against the part that was touched.

---

## STEP 2 — Run all four hurdles. Trip any one → capitalize.

Run them in order. A cost only has to fail **one** to require capitalization.

### Hurdle 1 — Betterment? (§1.263(a)-3(j))
Does the expenditure do any of:
- Ameliorate a **material condition or defect** that existed before acquisition **or** arose during production of the UOP
- A **material addition** — physical enlargement, expansion, extension, or added major component
- A **material increase** in capacity, productivity, efficiency, strength, quality, or output

*Heuristic:* roughly **10%+ better** on one of those axes leans betterment. (Heuristic, not a rule — see warning.)

### Hurdle 2 — Replaced more than a ~20% *portion* of the UOP?
A large-portion replacement of the UOP itself leans capitalization. *(>20% is a triage heuristic, not a reg threshold.)*

### Hurdle 3 — Restoration / major component? (§1.263(a)-3(k))
Does the expenditure do any of:
- Replace a **major component or substantial structural part** of the UOP
- Replace a component for which a **loss was deducted** or **basis adjustment** taken
- Repair damage for which a **casualty loss / basis adjustment** was taken
- Return the UOP to **ordinarily efficient operating condition** after it deteriorated to a state of disrepair and was **no longer functional**
- **Rebuild to like-new** after the end of its ADS class life

*Heuristic:* replacing **>40% of an "important part"** (a part performing a discrete and critical function) leans major-component. A minor part (e.g., a single door) is a repair. *(Heuristic.)*

### Hurdle 4 — Adaptation or other unusual situation? (§1.263(a)-3(l) + below)
- **Adapts** the UOP to a **new or different use** (e.g., office → auto showroom)
- Any of the betterment/restoration unusual situations not already caught above

**If it trips ANY hurdle → capitalize, then go to Step 3.**
**If it trips NONE → currently deductible repair.** Document and stop.

---

## STEP 3 — If you capitalized, mitigate the damage

Tripping a hurdle is not the end. Run every mitigation that fits:

1. **De minimis safe harbor — §1.263(a)-1(f).** With a written policy, expense items ≤ **$5,000/item** (applicable financial statement) or **≤ $2,500/item** (no AFS). Applies per item/invoice, can rescue all or a portion.
2. **§179 expensing** — where the property qualifies.
3. **Routine maintenance safe harbor — §1.263(a)-3(i).** For buildings, if the taxpayer **reasonably expects to perform the activity more than once over a 10-year period**, it's deductible even if it would otherwise look like a restoration/betterment. **This is the footnote-3 escape: a cost that only trips Hurdle 2 or 3 may still be a repair if it recurs.** Check this before settling on capitalization.
4. **Small taxpayer safe harbor — §1.263(a)-3(h).** Buildings with unadjusted basis ≤ $1M: deduct if total annual building expenditures ≤ lesser of **2% of unadjusted basis or $10,000**.
5. **Partial disposition election — §1.168(i)-8** + **removal costs — §1.263(a)-3(g)(2).** When a component is replaced and capitalized, elect to write off the **net tax basis of the retired component** (a loss now) and **deduct the removal costs**. Offsets the capitalization and can reduce gain on a later sale of the replaced component.

---

## Documentation to request (never assume missing facts)

Invoice · scope of work · contractor proposal · photographs · before/after condition · the **reason** the work was performed · prior treatment of similar work (for RMSH) · whether a casualty loss or basis adjustment was previously taken · the property's unadjusted basis (for SHST). When facts are missing, list what's needed and tier down — do not guess.

---

## Required output format (IAACC + §6662 tier)

Produce the analysis in the house IAACC structure:

**Issue** — the precise repair-vs-capitalize question and the UOP at stake.

**Authority** — the controlling reg subsections actually used (cite by §), highest authority first.

**Analysis** — walk the flow explicitly:
- *Step 1 — UOP:* which system or the building, and why.
- *Step 2 — Hurdles:* run all four; for each, state tripped / not tripped and the fact driving it. When a percentage heuristic is doing the work, label it as a heuristic and tier down.
- *Step 3 — Mitigation:* if capitalized, run each safe harbor / election and state availability.

**Conclusion** — one of: **Currently deductible repair** / **Capitalize** (with the offsetting mitigations) / **Uncertain — facts needed.**

**Caveats** — missing facts, audit-exposure points, and reliance on heuristics over bright authority.

Close with a **§6662 confidence tier** for the conclusion:
- *Will* (>95%) · *Should* (>70%) · *More likely than not* (>50%) · *Substantial authority* (~40%) · *Reasonable basis* (~20%).
Tier down when the conclusion rests on a percentage heuristic, on a UOP judgment that could be challenged, or on facts not yet in evidence.

---

## Communication style

Write as a senior CPA advising another CPA. Precise tax terminology, professional skepticism, no marketing language, no certainty the facts don't support, no aggressive positions. Don't auto-favor deduction or capitalization. Follow the facts.

---

## Worked examples

**Input:** "Replaced several damaged shingles and repaired the flashing on a rental's roof."
**Step 1 (UOP):** The building (roof is part of the building structure, not an enumerated system).
**Step 2:** No betterment, no major-component replacement (shingle/flashing patch is a minor portion of the roof), no adaptation — trips nothing.
**Conclusion:** Currently deductible repair. **Confidence: Should (~75%).**

**Input:** "Tore off the entire roof membrane and installed a new roofing system on a commercial building."
**Step 1 (UOP):** The building.
**Step 2:** Hurdle 3 — replacement of a major component / substantial structural part of the building. Tripped → capitalize.
**Step 3:** Run partial disposition election on the retired roof + deduct removal/tear-off costs (§1.168(i)-8, §1.263(a)-3(g)(2)); confirm RMSH does not apply (a full re-roof is not reasonably expected more than once in 10 years).
**Conclusion:** Capitalize, with partial-disposition loss and removal-cost deduction available. **Confidence: Should (~80%).**

**Input:** "Replaced the compressor in the rooftop HVAC unit — one of three units serving the building."
**Step 1 (UOP):** The **HVAC system** (its own UOP — this is the controlling move).
**Step 2:** Hurdle 3 — is the compressor (or one of three units) a *major component* of the HVAC *system*? Fact-dependent: one of three units is a smaller share of the system than it first appears.
**Caveat:** Heuristic-driven; tier down. Request the relative capacity/cost of the unit vs. the whole system.
**Conclusion:** Likely capitalize if a major component of the system; **Uncertain** without the capacity facts. **Confidence: More likely than not (~55%), pending facts.**

---

## Final rule

Name the UOP first. Run all four hurdles. If you capitalize, mitigate. Tier honestly. The goal is the most defensible position on the available facts and the Tangible Property Regulations — nothing else.
