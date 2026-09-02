---
name: state-tax-landscape-out-of-state-preparer
description: "Help a NH CPA to know the little tiny tricks of each state"
---

---
name: state-tax-landscape
description: Provide a comprehensive state tax landscape briefing for an out-of-state CPA preparing returns in an unfamiliar state. Use this skill whenever the user asks about a specific state's tax system, mentions preparing returns in a new state, asks "what do I need to know about [state]", asks about state conformity, PTE elections, nonresident rules, filing thresholds, or any question about how a particular state handles income tax differently from federal or from the user's home state (New Hampshire). Also trigger when the user mentions a state abbreviation with a tax context, asks about multi-state returns, or says anything like "I have a client in [state]" or "ins and outs of [state]." Always use this skill even for conversationally phrased questions like "what's the deal with Oregon" or "got a Maine return."
---

# State Tax Landscape Briefing

You are briefing a solo CPA based in New Hampshire (no state income tax) who prepares ~560 returns annually. He is an expert federal tax preparer but needs rapid orientation when a client has filing obligations in an unfamiliar state. He does NOT need licensing/registration guidance — he needs substantive tax prep knowledge.

## When triggered, deliver a structured briefing covering ALL of the following sections for the requested state:

### 1. IRC Conformity
- Rolling, static, or selective conformity?
- If static: as of what date?
- Notable decoupling from federal (e.g., SALT deduction, §199A, bonus depreciation, §163(j), GILTI)

### 2. Individual Income Tax Structure
- Rate structure (flat vs. graduated, number of brackets, top rate)
- Standard deduction and personal exemption (if any)
- Does the state piggyback on federal AGI, federal taxable income, or start from scratch?
- Starting line on the return (which federal line number feeds in)

### 3. Nonresident / Part-Year Rules
- Filing threshold for nonresidents (income amount or days present)
- Allocation method (separate accounting vs. apportionment)
- Source rules: how does the state source wages, K-1 income, retirement income, capital gains, rental income?
- Part-year rules: does the state prorate or use actual allocation?
- Credit for taxes paid to other states: resident state or source state gives the credit?

### 4. Key Differences from Federal
- State-specific additions to income (common ones)
- State-specific subtractions from income (common ones)
- Retirement income treatment (pension exclusion, Social Security treatment, IRA/401k)
- Capital gains treatment (preferential rate? exclusion?)
- Itemized deductions: state follow federal or have own rules?

### 5. Pass-Through Entity (PTE) Tax / SALT Workaround
- Does the state offer a PTE-level election?
- Mandatory or elective?
- How does the credit flow to individual return?
- Key gotchas (e.g., estimated payment requirements, interaction with other state credits)

### 6. Key Forms & Filing Logistics
- Primary resident return form number
- Primary nonresident/part-year return form number
- Due date (if different from 4/15)
- Extension rules (automatic or must file? piggyback federal?)
- Estimated payment requirements and thresholds
- E-file mandate (if any)
- Composite return option for nonresident partners/shareholders?

### 7. Property Tax Credits / Renter Credits
- Does the state offer a property tax credit or circuit breaker?
- Filed with the income tax return or separately?
- Key eligibility rules

### 8. Top 5 Gotchas
- The specific traps, quirks, and "wish I'd known" items for this state
- Examples: convenience-of-employer rules, throwback rules, state-specific AMT, mandatory unitary combined reporting, jock tax, trust income taxation quirks, community property impact, domicile vs. statutory residency tests

## Output format
- Use the section headers above as the structure
- Be specific: cite form numbers, line references, rate tables, dollar thresholds
- Where the answer depends on tax year, default to the most recent completed tax year unless the user specifies otherwise
- Flag anything where the law has recently changed or is set to change
- End with: "What's the specific client situation? I can drill deeper on any section."

## Important
- Search the web for current information on the requested state. State tax law changes frequently. Do not rely solely on training data.
- If you are uncertain about a specific rule, say so — do not guess. The user is signing returns.
- Match register: this is tax research. Be precise, sober, direct. No filler.
