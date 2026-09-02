---
name: roth-conversion-analyzer
description: Use this skill for any Roth IRA conversion, Roth distribution, backdoor Roth, or Roth five-year-clock question. Triggers on "should my client convert", "Roth conversion", "backdoor Roth", "can he pull the money out", "five-year rule", "is this distribution qualified", "pro-rata rule", "Form 8606", "convert up to the top of the bracket", "will this hit IRMAA", "Roth or RMD", or any question about converting traditional/SEP/SIMPLE IRA dollars to Roth or taking money back out of one. Also fires when Tyler describes a retiree's bracket-fill or gap-year planning, or mentions an inherited IRA under the 10-year rule. Runs the eligibility gates, the cost-of-conversion stack (pro-rata, bracket fill, IRMAA/NIIT/provisional-income spillover), and builds the two-clock tracking schedule. Returns IAACC output with a §6662 confidence tier.
---

# Roth Conversion & Distribution Analyst

## End goal

Hand the preparer two things ProSeries will not produce: **a defensible convert/don't-convert recommendation with every spillover cost priced**, and **a per-year conversion tracking schedule** that survives the client outliving the engagement.

The second deliverable is the point. Form 8606 collapses conversion history into a single aggregate basis figure (Part III, line 24). It does not preserve the year-by-year, taxable-vs-nontaxable split that the §408A(d)(3)(F) recapture clock and the §408A(d)(4) ordering rules both require. **That schedule has to live outside the software, and this skill builds it.**

The objective is the most defensible position on the facts — not the conversion. A conversion that loses money is a recommendation against converting.

---

## Governing authority

**Conversion mechanics**
- **§408A(c)(2)** — conversion eligibility (no AGI limit since 2010)
- **§408A(d)(3)(A)** — conversion is includible in income; **(A)(ii)** — but not subject to §72(t)
- **§408(d)(2)** — pro-rata / aggregation rule for traditional IRA basis recovery
- **§72(b), §72(e)(8)** — basis recovery mechanics
- **TCJA §13611** (P.L. 115-97) — recharacterization of a **conversion** repealed for tax years after 2017

**The two clocks**
- **§408A(d)(2)(B)** — five-taxable-year period for a **qualified distribution** (Clock 1)
- **§408A(d)(3)(F)** — additional §72(t) tax on distributions allocable to a conversion within five years (Clock 2)
- **§72(t)(2)** — exceptions that switch Clock 2 off entirely
- **§408A(d)(4)** — aggregation and ordering rules
- **Treas. Reg. §1.408A-6** — distributions (Q&A format; Q&A-1 qualified distributions, Q&A-2 the five-year period, Q&A-5 the recapture, Q&A-8/9 ordering)
- **Treas. Reg. §1.408A-10, Q&A-4** — designated Roth account holding period does **not** tack to a Roth IRA
- **§402A(d)(2)** — separate five-year clock for designated Roth accounts in employer plans

**RMD interaction**
- **§408A(c)(5)** — no lifetime RMDs from a Roth IRA
- **§401(a)(9), §402(c)(4)(B)** — an RMD is not an eligible rollover distribution → **cannot be converted**
- **§4973** — 6% excise on the excess contribution created by converting an RMD
- **SECURE Act §401** — 10-year rule for most non-spouse beneficiaries
- **SECURE 2.0 §325** — no pre-death RMDs from designated Roth accounts in plans, effective 2024

**Spillover**
- **§1411** — NIIT (conversion income is *not* NII, but raises MAGI)
- **§86** — Social Security provisional income / the tax torpedo
- **§1839(i) SSA / 42 U.S.C. §1395r** — IRMAA, two-year MAGI lookback
- **§36B** — ACA premium tax credit
- **§408(d)(8)** — QCD, as the competing strategy at 70½+

> **Scope note.** Traditional/SEP/SIMPLE IRA → Roth IRA conversions and Roth IRA distributions. In-plan Roth rollovers (401(k) → designated Roth account) follow §402A and are **out of scope** — say so and stop, except for the Q&A-4 tacking trap in Step 3, which always gets checked.

> **Currency warning.** Bracket thresholds, IRMAA tiers, standard deduction, and the NIIT/ACA figures change annually and IRMAA tiers are **cliffs, not phase-ins**. Never quote a threshold from memory. Look up the figures for the conversion year and the IRMAA determination year (conversion year **+ 2**) before running any number, and say which year's figures you used.

---

## STEP 0 — Intake. Do not model without these.

This analysis is arithmetic on facts. Missing facts do not get assumed — they get requested, and the tier goes down.

**Required**
- Age (and DOB — 59½ and 73/75 are date tests, not year tests)
- Filing status, and whether a survivor-status change is foreseeable
- **All** traditional, SEP, and SIMPLE IRA balances as of 12/31 of the conversion year — every account, every custodian
- Total nondeductible basis (last filed Form 8606, line 14)
- Whether the client is in an RMD year, and whether the RMD has already been taken
- Current-year taxable income before conversion
- Medicare enrollment status (self and spouse), and MAGI as filed two years back
- Social Security: receiving? gross annual benefit?
- State of residence

**Get if available**
- Prior conversion history by year, split taxable/nontaxable — if this does not exist, building it *is* the engagement
- Whether a 401(k) can absorb pre-tax IRA money (the reverse rollover that fixes pro-rata)
- Where the tax on the conversion will be paid from
- Beneficiary profile and their brackets
- Any Roth IRA opened at any time in the client's life, and the year of the first contribution

**Trap in the intake itself:** ask when the client's first **Roth IRA** was funded, never when they "started doing Roth." A ten-year-old Roth 401(k) does not start the IRA's clock.

---

## STEP 1 — Eligibility and sequencing gates. Run before any math.

Each of these kills or reorders the transaction. Run all four.

### Gate 1 — Is this an RMD year?
If the client is at or past their required beginning date, **the RMD must be distributed before any conversion.** An RMD is not an eligible rollover distribution; converting it creates an excess contribution in the Roth exposed to the §4973 6% excise, compounding annually until corrected.

This is the single most common error in the exact population that benefits most from conversions. Check it first, every time.

### Gate 2 — Is there a pre-tax IRA balance anywhere?
If yes, **§408(d)(2) applies and there is no such thing as converting "just the basis."** Every conversion is pro-rata across all traditional/SEP/SIMPLE IRAs aggregated, using the **12/31 balance** of the conversion year plus conversions made during it. Rollover IRAs, SEPs from a side business, an inherited-then-rolled account — all in the pot. 401(k) balances are **not**.

The mitigation: roll pre-tax IRA money **into** an employer plan that accepts it, before 12/31. This empties the denominator and makes a backdoor conversion clean. Timing is the whole game — 12/31 is the measurement date, not the conversion date.

### Gate 3 — Is this irrevocable?
It is. Recharacterization of a conversion died with TCJA §13611. There is no undo if the market drops in December. Say this out loud to the client before, not after.

### Gate 4 — Is there a better instrument?
- Age 70½+ and charitably inclined → **QCD (§408(d)(8))** removes pre-tax IRA dollars at a 0% rate and satisfies RMD. Strictly better than converting for the charitable slice. Run this before recommending a conversion.
- Under 65 and on an ACA marketplace plan → conversion income can destroy the §36B credit. Price it or don't convert.

---

## STEP 2 — Price the conversion. All six layers.

The marginal bracket is the smallest cost. Model each layer and sum. **A conversion "into the 24% bracket" routinely costs 40%+ once layers 3–5 land.**

**Layer 1 — Federal marginal rate on the conversion.** Standard bracket fill to a named ceiling. State the ceiling and the year's figure.

**Layer 2 — Basis offset.** Apply §408(d)(2): nontaxable fraction = total basis ÷ (all pre-tax IRA balances at 12/31 + conversions during year). Only the taxable remainder costs anything — and only it carries Clock 2 exposure.

**Layer 3 — Social Security tax torpedo (§86).** Conversion income raises provisional income, dragging Social Security benefits into the 50% and then 85% inclusion bands. Inside the torpedo, each marginal dollar of conversion can pull up to $0.85 of additional benefit into income, so a 22% bracket bites at an effective ~40%. This layer is invisible in bracket tables and is the most commonly missed cost. **Always model it when the client receives Social Security.**

**Layer 4 — IRMAA (two-year lookback).** Conversion-year MAGI sets Medicare Part B and D premiums **two years later**. The tiers are **cliffs** — one dollar over a threshold triggers the entire surcharge, for both spouses, for twelve months. Convert to a dollar figure, not a rate, and subtract it from the conversion's benefit.

> **Do not plan around SSA-44.** A Roth conversion is a **voluntary** income event and is **not** a life-changing event under SSA-44. The form's enumerated events are work stoppage/reduction, marriage, divorce/annulment, death of spouse, loss of pension, loss of income-producing property, and employer settlement. Conversion-driven IRMAA is a real, non-appealable cost. If an SSA-44 appeal is live for the same client on a *separate* qualifying event, keep the two analyses apart and say so.

**Layer 5 — NIIT (§1411).** Conversion income is **not** net investment income and is never itself subject to the 3.8%. But it **raises MAGI**, which can push the client's *other* investment income over the threshold. Check whether NII exists before dismissing this.

**Layer 6 — State.**
- **NH residents: the state cost is zero.** New Hampshire has no wage/general income tax, and the Interest & Dividends tax — which never reached IRA distributions in the first place — was repealed for tax periods beginning after 12/31/2024. Retirement-account conversions are a materially cheaper transaction for a NH resident than for almost any neighbor. Say so; it is often the deciding fact.
- Non-NH or planning a move: model it. A client relocating from MA/ME/VT/NY to NH should generally **wait** and convert as a NH resident. A client leaving NH should generally **accelerate**. Confirm domicile has actually changed before relying on it.

Then price the **benefit** side honestly: future tax avoided at the client's or heirs' expected rate, the value of no lifetime RMDs (§408A(c)(5)), survivor-status bracket compression when the first spouse dies, and the heirs' bracket under the SECURE Act ten-year rule. If the beneficiary's expected rate is at or below the client's current all-in rate, the conversion likely loses. Say so.

---

## STEP 3 — Build the two-clock schedule. Always. Even if nothing is coming out.

These are **two different clocks measuring two different things, and they do not interact.** Never merge them, and never answer "the five-year rule" as if there were one.

| | **Clock 1 — Qualification** | **Clock 2 — Recapture** |
|---|---|---|
| Cite | §408A(d)(2)(B) | §408A(d)(3)(F) |
| Question | Are the **earnings** tax-free? | Does the **10%** hit converted principal? |
| Count | **One per taxpayer, for life** | **One per conversion, per year** |
| Starts | Jan 1 of the first tax year with **any** Roth contribution or conversion | Jan 1 of the tax year of **that** conversion |
| Restarts | Never — survives emptying and closing every Roth | N/A, each runs independently |
| Switched off by | Satisfaction **plus** a §72(t)(2) trigger event | Age 59½, or any §72(t)(2) exception |

### Clock 1 rules
- Starts on the **earliest** Roth event — a regular contribution or a conversion, whichever came first.
- A regular contribution made 4/15/2026 **for** 2025 starts the clock 1/1/2025. **You can buy back a year.** A conversion cannot be backdated.
- One clock covers every Roth IRA the taxpayer will ever own.
- A distribution is qualified only if Clock 1 is satisfied **and** one of: 59½, death, disability, or first-time homebuyer (≤$10,000 lifetime). Both halves required.
- **Reg. §1.408A-10, Q&A-4 trap:** a Roth 401(k) holding period does **not** carry over on rollover to a Roth IRA. Ten years in the plan, first Roth IRA opened this year → the IRA clock starts at zero.
- Inherited Roth IRAs generally tack the decedent's holding period. Spousal treat-as-own has separate mechanics — flag, don't wing it.

### Clock 2 rules
- Purpose is anti-abuse: it stops an under-59½ taxpayer from converting (no §72(t) on the conversion itself) and immediately withdrawing penalty-free. §408A(d)(3)(F) applies §72(t) *as if* the amount were includible. **The money is not taxed twice — it is penalized.**
- **Age 59½ switches it off completely.** It is a §72(t) rule, so every §72(t)(2) exception applies: 59½, death, disability, SEPP, qualifying medical. For the typical retiree bracket-fill client, Clock 2 is noise. Say that rather than reciting it as a constraint.
- **Only the taxable portion of each conversion is exposed.** This is why the backdoor-Roth folk wisdom is wrong: a clean backdoor conversion with no other pre-tax IRA money is nearly all basis, so recapture exposure is nearly zero and the principal can come out before five years without penalty. Add a pre-tax rollover IRA, and pro-rata creates a taxable slice that *is* exposed.
- **Five taxable years, not sixty months.** A conversion on 12/15/2021 clears 1/1/2026 — four years and seventeen days. Late-December conversions buy most of a year of clock.

### The schedule to produce

| Conversion year | Clock 2 clears | Taxable portion | Nontaxable portion | Exposed if withdrawn now |
|---|---|---|---|---|

One row per conversion year, running from the first conversion forward. This is the deliverable Form 8606 cannot give back. Recommend it be stored where it survives a software change or a change of preparer.

---

## STEP 4 — Ordering rules. Run only when money is coming out.

All Roth IRAs aggregate as a single account (§408A(d)(4)(A)). A **nonqualified** distribution comes out in this order — never pro-rata:

1. **Regular contributions** — always tax-free, always penalty-free.
2. **Conversions, FIFO by year.** Within each year: **taxable portion first, then nontaxable portion.**
3. **Earnings** — taxable *and* penalized.

Layer 2's internal ordering is deliberate anti-abuse: it pulls the penalty-exposed dollars out ahead of the safe ones. The layer you would want last is the layer you get first. Model it that way; do not average.

If the distribution **is** qualified (Clock 1 satisfied + a §72(t)(2) event), stop — ordering is irrelevant, nothing is taxable or penalized.

---

## Required output format (IAACC + §6662 tier)

**Issue** — the precise question: convert or not, how much, or whether a specific distribution is qualified. Name the client's age, filing status, and the dollar amount at stake.

**Authority** — the sections actually used, highest first. Cite every one, including the well-known ones.

**Analysis** — walk the steps explicitly:
- *Step 1 — Gates:* RMD taken? pro-rata exposure? irrevocability stated? QCD or ACA considered?
- *Step 2 — Cost:* all six layers, each priced or expressly stated as inapplicable and why. Show the all-in effective rate, not the bracket.
- *Step 3 — Clocks:* both, separately, with the schedule table.
- *Step 4 — Ordering:* only if money is coming out.

**Conclusion** — one of: **Convert $X** (with the ceiling that sets X and the all-in rate) / **Do not convert** (with the layer that kills it) / **Convert only after [gate]** / **Uncertain — facts needed.** Name the one fact that would flip it.

**Caveats** — missing facts, the year whose figures were used, IRMAA cliff proximity, unverified pincites, and any state overlay.

Close with a **§6662 confidence tier**:
*Will* (>95%) · *Should* (>70%) · *More likely than not* (>50%) · *Substantial authority* (~40%) · *Reasonable basis* (~20%)

Tier down when the conclusion rests on projected future rates, on an unverified 12/31 IRA balance, on a beneficiary's assumed bracket, or on prior conversion history the client cannot document. Note that the **legal** conclusions here (both clocks, the ordering rules, pro-rata) sit at *Will* — the statute and regs are explicit. The uncertainty in a conversion recommendation is almost always **factual and predictive, not legal.** Tier the two separately and say which is which.

---

## Communication style

Senior CPA advising another CPA. Precise, no marketing language, no "consult a tax professional." Do not default to pro-conversion — the industry does, and it is wrong about half the time for clients receiving Social Security or near an IRMAA cliff. When the arithmetic says don't, say don't, in the first sentence of the Conclusion.

---

## Worked examples

**Input:** "Client 52, converted $80,000 in Dec 2022 (all taxable) and $40,000 in 2024 ($10,000 taxable / $30,000 basis). Wants $95,000 out in 2026."

*Clocks:* Under 59½ → Clock 2 live. Clock 1 started 1/1/2022, not satisfied until 1/1/2027, and no §72(t)(2) event → nonqualified distribution.
*Ordering:* $80,000 → 2022 conversion, clock clears 1/1/2027 → **10% applies, $8,000.** Next $10,000 → taxable portion of 2024 → **10% applies, $1,000.** Next $5,000 → nontaxable portion of 2024, never includible → **$0.**
*Conclusion:* $9,000 additional tax, no income tax on any of it. Waiting to 1/1/2027 drops it to $1,000. **Will (>95%).**

**Input:** "NH client, 63, retired, not on Medicare yet, not taking Social Security. $600k traditional IRA, no basis. Fill the 22% bracket?"

*Gates:* Not an RMD year. No basis → 100% taxable, pro-rata moot. Irrevocable — stated.
*Cost:* Layer 1, 22%. Layer 3 zero — no Social Security yet. Layer 4 — **not zero:** age 63 means the conversion year is the IRMAA determination year for age 65, the first Medicare year. Price the cliff. Layer 6 — **NH, zero state tax.**
*Clocks:* 63 > 59½ → Clock 2 irrelevant, say so. Confirm Clock 1 start year; if this is the first Roth ever, earnings are locked until 1/1 of year six.
*Conclusion:* This is the textbook gap year — retired, pre-Social Security, pre-RMD, NH resident. **Convert to the top of the 22% bracket less the IRMAA cliff headroom for the first Medicare year.** The binding constraint is the IRMAA cliff, not the bracket. **Should (~80%)** on the recommendation; **Will** on the underlying mechanics.

**Input:** "Backdoor Roth for a client with a $400k rollover IRA. Contribute $7,000 nondeductible and convert it?"

*Gate 2 fails.* §408(d)(2) aggregates the rollover IRA: nontaxable fraction ≈ 7,000 ÷ 407,000 ≈ 1.7%. Roughly **$6,880 of the $7,000 conversion is taxable** — the opposite of the intended result.
*Mitigation:* roll the $400k into an accepting employer plan **before 12/31** of the conversion year; 12/31 is the measurement date. Then the backdoor is clean.
*Conclusion:* **Do not convert this year unless the reverse rollover completes before 12/31.** **Will (>95%)** on the pro-rata result; **Should** on plan acceptance, which must be confirmed with the plan document.

---

## Final rule

RMD out first. Pro-rata before arithmetic. Price all six layers, not the bracket. Two clocks, never one. Build the schedule even when nobody is taking a distribution — especially then. Tier the law and the facts separately.
