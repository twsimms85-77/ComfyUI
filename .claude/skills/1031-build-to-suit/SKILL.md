---
name: 1031-build-to-suit
description: "Use this skill whenever Tyler asks about a §1031 exchange where the replacement property will be built, improved, renovated, or constructed with exchange proceeds. Triggers on build-to-suit exchange, improvement exchange, construction exchange, leasehold improvement exchange, reverse build-to-suit, parking arrangement, exchange accommodation titleholder (EAT), QEAA, Rev. Proc. 2000-37, and any client fact pattern like 'sell the rental and build on the new lot', 'can they use 1031 money to renovate', 'the replacement isn't finished by day 180', 'client wants to build on land they already own', or 'build on the parents' land'. Also fires when Tyler describes a sale plus construction and asks whether it can be deferred. Runs a Step 0 (whose land?) to Step 1 (structure) to Step 2 (timeline) to Step 3 (what counts as received) to Step 4 (boot and basis) flow and returns an IAACC memo with a §6662 confidence tier plus a deal sheet and 45/180-day calendar."
---

# §1031 Build-to-Suit (Improvement) Exchange Analyst

## End goal

Hand the preparer a defensible answer on whether a client can defer gain under §1031 when the replacement property has to be built or improved after the relinquished sale, and exactly how the deal must be papered and timed for that to hold. The output is a structure decision, a dated calendar, a list of what will and will not count as like-kind property on the day the client takes title, and an IAACC memo with a confidence tier. The objective is **the most defensible position on the facts**, not the deferral. Follow the facts.

Build-to-suit exchanges fail for three reasons, in this order: the client already owns the land, the improvements are not real property in the client's hands by day 180, and the accommodator's ownership is a sham. Every step below targets one of those.

---

## Governing authority

**Statute and regulations**
- **§1031(a)(1)** — like-kind real property held for productive use in a trade or business or for investment (personal property excluded after 12/31/2017, TCJA §13303)
- **§1031(a)(3)** — deferred exchange limits: 45-day identification, and receipt by the earlier of 180 days or the due date of the return **including extensions**
- **§1031(f)** — related-party rules, two-year holding requirement, anti-abuse
- **Reg. §1.1031(a)-1(c)(2)** — a leasehold of 30 years or more is like-kind to a fee
- **Reg. §1.1031(a)-3** (T.D. 9935, Dec. 2020) — definition of real property; inherently permanent structures and structural components; 15% incidental personal property rule
- **Reg. §1.1031(k)-1(c)** — identification rules (three-property, 200%, 95%)
- **Reg. §1.1031(k)-1(d)** — receipt of substantially the same property
- **Reg. §1.1031(k)-1(e)** — **property to be produced**: identification of improvements, receipt before the end of the exchange period, post-receipt production is not like-kind, production services on the taxpayer's own property are not like-kind
- **Reg. §1.1031(k)-1(g)(4)** — qualified intermediary (QI) safe harbor; **(g)(6)** restrictions on the taxpayer's right to receive money; **(k)** disqualified persons (includes the taxpayer's CPA or attorney within the prior two years)
- **Reg. §1.1031(k)-1(j)** and **§1.1031(d)-2** — boot, liability netting
- **Reg. §1.468B-6** and **§1.1031(k)-1(h)** — interest on exchange funds is the taxpayer's income
- **Reg. §1.168(i)-6** — depreciation of exchanged basis vs. excess basis after an exchange
- **Reg. §1.1245-4(d)** — §1245 recapture in a §1031 exchange when replacement lacks equal §1245 property

**Rulings and procedures**
- **Rev. Proc. 2000-37** — reverse and parking safe harbor; qualified exchange accommodation arrangement (QEAA); exchange accommodation titleholder (EAT); §4.03 permitted arrangements (taxpayer may manage construction, lend to and guarantee for the EAT, lease from the EAT)
- **Rev. Proc. 2004-51** — modifies 2000-37; safe harbor **unavailable** for property the taxpayer owned within the 180 days before it was transferred to the EAT
- **Rev. Rul. 67-255** — a building built on land the taxpayer already owns is not like-kind property; the taxpayer received construction services
- **Rev. Rul. 75-291** — a build-to-suit on land the other party acquired and improved solely to make the exchange still qualifies
- **Rev. Rul. 2002-83** — related-party exchange through a QI with related-party cash-out fails §1031(f)
- **Rev. Proc. 2018-58, §17** — postponement of the 45/180-day deadlines for federally declared disasters
- **PLR 200329021** — leasehold improvement exchange: EAT ground-leases land from a **related party** for 30+ years, builds, taxpayer receives the improved leasehold (instructive, not binding)
- **PLR 200251008** — same structure on the taxpayer's **own** land; the fact pattern Rev. Proc. 2004-51 was issued to shut down

**Cases**
- **J.H. Baird Publishing Co. v. Commissioner**, 39 T.C. 608 (1962) — third party constructed the building on its own land to the taxpayer's specifications, then exchanged; qualified
- **Coastal Terminals, Inc. v. United States**, 320 F.2d 333 (4th Cir. 1963) — build-to-suit through an intermediary that took title and built; qualified
- **Bloomington Coca-Cola Bottling Co. v. Commissioner**, 189 F.2d 14 (7th Cir. 1951) — construction on the taxpayer's own land is services, not property; failed
- **DeCleene v. Commissioner**, 115 T.C. 457 (2000) — taxpayer deeded its own lot to the buyer, buyer built, then re-deeded; buyer was never the beneficial owner; failed. The controlling authority for **substance of the EAT's ownership**
- **Bartell v. Commissioner**, 147 T.C. 140 (2016) — 17-month parking build-to-suit outside the Rev. Proc. 2000-37 safe harbor upheld under Ninth Circuit exchange cases; **IRS nonacquiescence, AOD 2017-06**. Do not plan around it; cite it only as the fallback position

> **Scope:** Real property only. Any personal property component of the build (furniture, movable equipment, unaffixed materials) is outside §1031 after 2017 and is either boot or a separate purchase. Say so when it appears.

---

## STEP 0 — Whose land? (this decides everything)

Ask and record before any other step. The answer sorts the file into one of four lanes.

| Land is owned by | Lane | Authority | Viability |
|---|---|---|---|
| **The taxpayer** (or was, within the last 180 days) | Stop. Restructure or recognize gain. | Rev. Rul. 67-255; Bloomington Coca-Cola; DeCleene; Rev. Proc. 2004-51 | Not viable inside the safe harbor. Building on your own land is buying services. |
| **A related party** (§267(b) / §707(b)) | Leasehold improvement exchange | PLR 200329021; Reg. §1.1031(a)-1(c)(2); §1031(f) | Viable but hot. EAT takes a 30+ year ground lease, builds, taxpayer receives the leasehold plus improvements. Run the §1031(f) related-party test and Rev. Rul. 2002-83 anti-abuse test. Reasonable Basis to Substantial Authority depending on rent terms and cash flow to the related party. |
| **An unrelated seller, not yet closed** | Forward build-to-suit or reverse build-to-suit (Step 1) | Rev. Proc. 2000-37; Reg. §1.1031(k)-1(e); Baird; Coastal Terminals | Standard. Substantial Authority when papered correctly. |
| **A developer who will build and then sell** | Plain deferred exchange | Rev. Rul. 75-291; Baird | Cleanest of all. Developer owns land and building until closing; taxpayer buys a finished product within 180 days. No EAT needed. |

**The "own land" trap in disguise.** Watch for: the client is already under contract and has paid a large deposit; the client's LLC or spouse owns the lot; the client bought the lot "a few months ago" (inside 180 days of the planned EAT transfer, Rev. Proc. 2004-51 §4.05); the client wants to "sell the lot to the accommodator and buy it back improved" (that is DeCleene). Each of these is the own-land lane until proven otherwise.

If the client owns the land and still wants to build with sale proceeds, the honest choices are: (a) recognize the gain and build, (b) buy a different replacement, or (c) a non-safe-harbor structure with Colorable Claim exposure at best. State this plainly. Do not invent a fourth option.

---

## STEP 1 — Choose the structure

### 1A. Forward build-to-suit (exchange first, build second)

Sequence:
1. Taxpayer sells relinquished property; proceeds go to the QI under Reg. §1.1031(k)-1(g)(4). Taxpayer never touches cash. Day 0.
2. Within 45 days, taxpayer identifies the replacement **land plus the improvements** (Step 2).
3. EAT (typically a single-member LLC owned by the QI's affiliate) acquires the replacement land using exchange funds advanced by the QI, under a written QEAA signed within five business days of the EAT taking title (Rev. Proc. 2000-37 §4.02(3)).
4. EAT holds title, hires the contractor (or taxpayer manages construction as agent under §4.03), and pays draws from exchange funds.
5. On or before day 180, EAT conveys the land and whatever improvements exist to the taxpayer, either by deed or by assigning the LLC membership interest.

Use when the relinquished sale cannot wait and the build is short. Construction time is what is left after the land closing, so this lane commonly yields 120 to 150 build days, not 180.

### 1B. Reverse build-to-suit (park first, build, then sell)

Sequence:
1. EAT acquires the replacement land with funds lent or guaranteed by the taxpayer (permitted, §4.03). QEAA signed within five business days. **This is Day 0.**
2. Within 45 days of Day 0, taxpayer identifies the **relinquished** property (Rev. Proc. 2000-37 §4.02(4)).
3. EAT builds for up to 180 days.
4. Taxpayer sells the relinquished property through the QI; QI uses proceeds to acquire the improved replacement from the EAT. Must complete within 180 days of Day 0 (§4.02(5)) and the combined parking period cannot exceed 180 days (§4.02(6)).

Use when the build is the long pole and the relinquished sale can be scheduled. This lane gives the full 180 days of construction because the clock starts when the EAT takes the land, not when the relinquished property sells. Financing is the cost: the taxpayer must fund the land and construction out of pocket or with a construction loan to the EAT, then get reimbursed from exchange proceeds at the end.

### 1C. Hybrid (park the land early, sell mid-stream)

EAT acquires land (reverse clock starts). Relinquished sells on, say, day 60; proceeds go to QI. Forward clock starts on day 60 for the relinquished leg, but the parking period is still measured from the EAT's acquisition, so the replacement must be conveyed by day 180 of the **parking**, not day 180 of the sale. Draw both calendars and use the earlier deadline.

### 1D. Leasehold improvement exchange (related-party land)

EAT takes a ground lease of 30 years or more (Reg. §1.1031(a)-1(c)(2), including options reasonably expected to be exercised), builds, and assigns the leasehold with improvements to the taxpayer. The landlord must be a real, arm's-length landlord: fair rent actually paid, lease term genuinely long, landlord does not receive exchange proceeds. §1031(f) applies if the landlord is related; the related party has not sold property in this transaction, so the direct two-year rule usually is not triggered, but §1031(f)(4) "structured to avoid" applies if the rent stream or a later lease termination effectively cashes out the related party. Cite PLR 200329021 as instructive only.

### 1E. What the taxpayer may and may not do during parking (Rev. Proc. 2000-37 §4.03)

Permitted: act as construction manager or general contractor for the EAT; lend to or guarantee loans for the EAT; lease the property from the EAT; indemnify the EAT; agree to fixed purchase terms. Required: the EAT holds legal title or other qualified indicia of ownership, reports as owner for its own tax purposes, and is not the taxpayer or a disqualified person. **Not permitted in substance:** an arrangement where the EAT bears no cost, no risk, and no upside and the paperwork is the only thing separating it from an agent. DeCleene is the case for what happens then.

**Tyler-specific flag.** A CPA who has performed services for the client within the prior two years is a **disqualified person** (Reg. §1.1031(k)-1(k)(2)) and cannot be the QI or EAT. Neither can Ilene, Lyndsey, the firm, or any entity they own. Recommend an independent, bonded, fidelity-insured QI with segregated escrow accounts.

---

## STEP 2 — Timeline and identification

### 2A. The two clocks

| Event | Forward (1A) | Reverse (1B) |
|---|---|---|
| Day 0 | Relinquished property transferred (deed delivered / closing) | EAT takes title to replacement land |
| Day 45 | Identify replacement land **and improvements** in writing to the QI | Identify relinquished property in writing to the EAT/QI |
| Day 180 | Taxpayer must **receive** the improved replacement | Relinquished must close and replacement must transfer out of the EAT |
| Hard stop | Earlier of day 180 or the return due date **with extensions** (§1031(a)(3)(B)) | Same, measured against the relinquished transfer |

Days are calendar days, midnight to midnight, no extension for weekends or holidays. Rev. Proc. 2018-58 §17 is the only relief and only for a federally declared disaster.

### 2B. The extension trap (state this on every file)

If day 180 falls after the unextended due date of the return for the year of the relinquished sale, the exchange period ends on the due date unless an extension is filed. Practical thresholds for calendar-year taxpayers:

| Filer | Unextended due date | Sale on or after this date requires an extension |
|---|---|---|
| 1040, 1041, 1120 | April 15 | ~October 17 of the prior year |
| 1065, 1120-S | March 15 | ~September 16 of the prior year |

File Form 4868 or 7004 before the due date. Filing the return itself before day 180 ends the exchange period on that filing date. Put this on the engagement checklist, not in a footnote.

### 2C. Identifying property to be produced (Reg. §1.1031(k)-1(e)(2))

The 45-day identification must contain:
1. A legal description of the underlying land (address or lot and block is acceptable, deed description is better).
2. As much description of the improvements as is practicable at the time. Attach the plans, the site plan, the building program, or a written scope with square footage, use, and major systems. Anything less invites a "not substantially the same" challenge under (d) and (e)(3).

Apply the three-property, 200%, and 95% rules to the land plus planned improvements at their expected completed fair market value. If the client is hedging between two lots, identify both and stay inside three properties.

### 2D. Substantially the same (Reg. §1.1031(k)-1(e)(3))

Improvements received do not have to be finished. They must be **substantially the same as identified**, tested as if construction had been completed. A 10,000 sq ft warehouse identified and a 10,000 sq ft warehouse 70% built is fine. A 10,000 sq ft warehouse identified and a 4,000 sq ft office received is not. Ordinary construction variations (change orders, substitutions) are ignored. Scope changes are not.

---

## STEP 3 — What counts as received on day 180

This is where most improvement exchanges leak value. Only **real property under local law, in place on the land, at the moment the taxpayer takes title** is like-kind. Apply Reg. §1.1031(a)-3 and (k)-1(e)(3) and (e)(4) to each dollar.

| Item | Counts as like-kind replacement value? | Why |
|---|---|---|
| Land | Yes | Real property |
| Foundation, framing, roof, walls, installed systems, whether complete or not | Yes, at the value of what is affixed | Inherently permanent structures and structural components, §1.1031(a)-3 |
| Site work, grading, paving, utilities in the ground | Yes | Land improvements are real property |
| Building materials delivered but not installed | **No** | Personal property until affixed |
| Deposits or prepayments to contractors for future work | **No** | Services, not property; (e)(4) |
| Architect, engineering, permit fees already incurred | Generally yes, to the extent capitalized into the improvements that exist | Part of the cost of the real property in place; document the allocation |
| Construction completed **after** the taxpayer takes title, even if paid from exchange funds | **No** | (e)(3)(ii): post-receipt production is not like-kind |
| Unspent exchange funds returned to taxpayer at day 180 | **No**, taxable boot | Cash received |
| Movable equipment, furniture, trade fixtures | **No** | Personal property; 15% incidental rule under §1.1031(a)-3 may keep it from breaking the exchange but does not make it like-kind |

**Practical instruction to the client and QI:** the target on day 180 is not "the building is done." The target is "every exchange dollar has been converted into affixed real property before the EAT deeds to me." Draw schedule should front-load hard costs. Do not let the contractor hold prepayments over day 180.

Have a contemporaneous valuation of the improvements in place at transfer (appraisal, contractor's certified percentage of completion, or lender's inspection). This is the number that goes on Form 8824.

---

## STEP 4 — Boot, basis, and depreciation

### 4A. Full-deferral test
To defer all gain, at the moment of receipt:
1. FMV of replacement real property received (land plus affixed improvements) is at or above the FMV of the relinquished property, and
2. all net exchange proceeds are reinvested (no cash returned), and
3. debt on the replacement is at or above debt relieved on the relinquished, or the shortfall is covered with new cash (Reg. §1.1031(d)-2 netting; §1.1031(k)-1(j)).

Any shortfall is recognized gain up to realized gain. In build-to-suit the usual boot is **unspent funds** and **prepayments that did not become real property**.

### 4B. Recapture check
If the relinquished property had a cost segregation study or otherwise carried §1245 property, and the replacement on day 180 is land plus a partly built shell, the §1245 property received may be less than the §1245 property given up. Reg. §1.1245-4(d) triggers ordinary recapture to that extent regardless of overall deferral. Unrecaptured §1250 gain is deferred, not eliminated, and carries into the replacement basis.

### 4C. Basis and depreciation
- Basis in the replacement is the relinquished adjusted basis, plus boot paid, plus gain recognized, minus boot received (§1031(d)).
- Under Reg. §1.168(i)-6, the **exchanged basis** continues the relinquished property's recovery period and method; the **excess basis** (new money into the build) is new property placed in service when the improvements are placed in service. Election out of the continuation rule is available under §1.168(i)-6(i) and is often simpler when the relinquished asset was nearly fully depreciated.
- Excess basis in the new construction is eligible for bonus depreciation on qualifying components under §168(k), including the 100% rate restored by OBBBA for property acquired after January 19, 2025. Self-constructed property "acquired" date rules under Reg. §1.168(k)-2(b)(5) apply; verify the start-of-construction date. A cost segregation study on the completed building is usually worth it here.
- Interest earned on exchange funds in escrow is the taxpayer's income under §1.468B-6, reported in the year earned, regardless of when received.

### 4D. Reporting
- Form 8824 for the year of the relinquished transfer, even if the exchange completes the following year. Dates on Part I must match the closing statements and the identification letter.
- Related-party exchanges: Form 8824 Part II every year for two years after.
- Keep in the file: QI exchange agreement, assignment of the purchase and sale agreements to the QI, QEAA, identification letter with proof of delivery, EAT deed in and out (or LLC assignment), draw schedule with dates, day-180 completion certification and valuation, closing statements for both legs.

---

## STEP 5 — State overlay (New Hampshire base, out-of-state property common)

- **New Hampshire.** No individual income tax on gain, and the Interest and Dividends Tax is repealed for periods after 12/31/2024. For a business organization, the Business Profits Tax follows the IRC as of the conformity date in RSA 77-A:1, XX, so §1031 deferral holds for BPT. The Real Estate Transfer Tax (RSA 78-B, $0.75 per $100 on each of buyer and seller) applies to each deed; a parking structure with an EAT can produce transfer tax on the EAT's deed in and deed out. Verify current DRA treatment before quoting the number, and prefer an LLC membership assignment out of the EAT where the DRA treats it consistently.
- **Vermont.** Follows federal. Nonresident seller withholding (2.5% of consideration, Form RW-171) applies at the relinquished closing; a reduced-withholding certificate can be requested for an exchange. Use the vt-tax-research skill for any VT return mechanics.
- **Massachusetts.** Conforms to §1031.
- **New York.** Nonresident estimated tax on sale (Form IT-2663) has a §1031 exemption box; the QI closing needs it checked.
- **California.** Conforms, but claw-back reporting on FTB Form 3840 is required every year until the deferred California gain is recognized, even if the client never returns to CA.
- **Pennsylvania.** Conforms only for tax years beginning after 12/31/2022. Pre-2023 relinquished sales were taxable in PA.
Flag any other state as "check conformity and nonresident withholding" rather than assume.

---

## Output format

Always produce the IAACC memo per the iaacc-tax-research skill, with the build-to-suit deal sheet placed between ISSUE and AUTHORITY.

### DEAL SHEET
```
Lane:                   [Own land / Related-party leasehold / Forward / Reverse / Hybrid / Developer build]
Relinquished:           [property, expected FMV, adjusted basis, debt, closing date]
Replacement land:       [property, seller, price, owned by whom today]
Improvements planned:   [scope, budget, expected build duration]
Day 0:                  [date and what triggers it]
Day 45 identification:  [date]
Day 180 receipt:        [date]
Return due date check:  [unextended due date; extension required? Y/N]
Estimated value in place at day 180:  [land + affixed improvements]
Projected boot:         [unspent funds + prepayments + debt shortfall]
QI / EAT:               [name; disqualified-person check passed? Y/N]
```

### ISSUE
One or two sentences. Entity type, dollar amounts, whose land, structure.

### AUTHORITY
Hierarchy order per the iaacc-tax-research skill. Pull from the list above and add anything fact-specific.

### ANALYSIS
Flowing prose. Cover Step 0 through Step 4 in order. Name the failure point if there is one. Do not soften a DeCleene or Rev. Rul. 67-255 problem.

### CONCLUSION
The most defensible position, the §6662 tier, and the one fact that would change the answer.

Default tiers for a correctly papered file:
| Lane | Typical tier |
|---|---|
| Developer build, forward, or reverse within Rev. Proc. 2000-37 | Substantial Authority |
| Hybrid inside both 180-day limits | Substantial Authority |
| Related-party leasehold improvement exchange | Reasonable Basis to Substantial Authority, driven by rent terms and §1031(f)(4) |
| Parking beyond 180 days (Bartell reliance) | Colorable Claim at best; disclose on Form 8275; AOD 2017-06 nonacquiescence |
| Own land, any structure | No Authority inside the safe harbor; do not recommend |

### CAVEATS
Assumptions, missing facts, state overlay, the extension trap, and the day-180 valuation requirement. Recommend Form 8275 disclosure whenever the tier is below Substantial Authority.

---

## Helper: day-count calendar

`timeline.py` in this skill folder prints Day 45, Day 180, and the extension-trap check for a given Day 0 and filer type:

```
python timeline.py 2026-11-03 --filer 1065
```

Use it, then paste the dates into the deal sheet.

---

## Style rules

- Say "whose land" out loud in the first three lines of every analysis.
- Never describe an EAT as "holding title for the taxpayer." Describe it as owning the property. Words in the file become facts on audit.
- Distinguish "completed" from "affixed" every time construction status comes up.
- Cite Rev. Proc. 2000-37 by section number when describing a requirement.
- Give the client two dates and one dollar figure they must hit, not a paragraph.
- Do not recommend "consult a tax professional." Recommend a specific QI engagement and a specific attorney task (QEAA drafting, ground lease drafting) when needed.
