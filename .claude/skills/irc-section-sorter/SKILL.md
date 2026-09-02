---
name: irc-section-sorter
description: Use this skill whenever Tyler wants to look up Internal Revenue Code (IRC) sections and have them organized by tax function. Triggers on requests like "fetch IRC §X", "pull these code sections", "sort these IRC sections", "is §X income, a deduction, or a credit", or any request to gather a set of code sections and group them by whether they govern INCOME (inclusion/recognition), DEDUCTION (above- or below-the-line subtractions), or CREDIT (dollar-for-dollar tax offsets). Fetches authoritative current text and returns a classified, grouped summary with citations.
---

# IRC Section Sorter

Fetch Internal Revenue Code sections and sort each into one of three functional buckets — **Income**, **Deduction**, or **Credit** — with a one-line summary and citation for each. The goal is a fast, organized map of how a set of code sections operate, not a full IAACC analysis (use `iaacc-tax-research` for that).

---

## Inputs this skill handles
- A list of specific sections: *"fetch §§ 61, 162, 25A, 199A, 24"*
- A topic to expand into sections: *"pull the major individual credits"* → identify the relevant §§ first, then fetch.
- A pasted block of sections to classify.

If the request is a topic rather than explicit section numbers, first list the sections you'll fetch and proceed.

---

## Fetch procedure
1. **Source — primary:** Cornell Legal Information Institute, `https://www.law.cornell.edu/uscode/text/26/<section-number>`. This is the standard, current statutory text.
2. If Cornell is unavailable for a section, fall back to `https://uscode.house.gov` (Office of Law Revision Counsel) or `https://www.govinfo.gov`.
3. Pull the section heading and enough of the operative text to determine its function. Do **not** paste the full statute — summarize.
4. **Amendments — note only when it matters.** Don't append an amendment line to every section. Add a brief "*Note:*" about the most recent amendment ONLY when leaving it out would be misleading or confusing — e.g., a dollar amount/threshold changed, a sunset or expiration applies, the provision was extended/restructured, or a recent act materially altered how the section operates. If the section is stable and the current summary stands on its own, say nothing about amendments.

---

## Classification rules
Assign each section to exactly one bucket based on its **primary operative function**:

- **INCOME** — defines gross income, inclusions, recognition events, or timing of income. (e.g., §61 gross income, §451 timing, §1001 gain/loss, §1245 recapture.)
- **DEDUCTION** — authorizes a subtraction from income, above- or below-the-line. (e.g., §162 trade/business, §163 interest, §170 charitable, §199A QBI, §179 expensing.)
- **CREDIT** — provides a dollar-for-dollar offset against tax liability. (e.g., §24 child tax credit, §25A education, §41 R&D, §38 general business credit.)

Edge cases:
- A section that does more than one thing → classify by its dominant function and add a one-line note flagging the secondary role.
- Definitional or procedural sections that don't fit any bucket → place under a fourth **Other / Definitional** heading rather than forcing a fit.

---

## Output format

```
## IRC Sections — Sorted

### Income
- **§<n> — <heading>.** <One-line plain-English summary.> [<note: amendment/sunset if any>]

### Deduction
- **§<n> — <heading>.** <One-line summary.>

### Credit
- **§<n> — <heading>.** <One-line summary.>

### Other / Definitional   (only if needed)
- **§<n> — <heading>.** <One-line summary.>

**Source:** Cornell LII (26 U.S.C.), retrieved <date>.
```

Within each bucket, list sections in ascending numerical order.

---

## Rules
- Always cite the source and retrieval date — statutory text changes.
- Summarize, never paste full section text.
- Classify by primary function; flag dual-purpose sections rather than hiding the nuance.
- If a section number doesn't exist or was repealed, say so explicitly instead of guessing.
- This skill organizes and orients. For a binding deductibility/treatment conclusion, hand off to `iaacc-tax-research`.
