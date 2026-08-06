# NH BET Credit Backfill — Missing Carryforward Years (2015–2021)

Workpaper supporting the 2025 NH Business Enterprise Tax Credit Worksheet
(Form BET Credit Worksheet, Version 2 08/2025).

## 1. What the filed 2025 worksheet shows

| Worksheet line | Taxable period | Col. A available credit | Col. C excess credit |
|---|---|---|---|
| 3 — current period | 2025 | 1,762 | 1,762 |
| 4 — tenth prior | 2015 | *(blank)* | — |
| 5 — ninth prior | 2016 | *(blank)* | — |
| 6 — eighth prior | 2017 | *(blank)* | — |
| 7 — seventh prior | 2018 | *(blank)* | — |
| 8 — sixth prior | 2019 | *(blank)* | — |
| 9 — fifth prior | 2020 | *(blank)* | — |
| 10 — fourth prior | 2021 | *(blank)* | — |
| 11 — third prior | 2022 | 1,506 | 1,506 |
| 12 — second prior | 2023 | 1,956 | 1,956 |
| 13 — first prior | 2024 | 1,445 | 1,445 |

Line 1 (BPT) = 0 and Line 2 = 0, so nothing was absorbed; every year's BET is
sitting as an unused carryforward. Lines 4–10 — tax years **2015 through
2021** — are the missing years.

## 2. Assumptions

- 2023 wage base (BET enterprise value tax base proxy) = **$263,000**, per client.
- Wages deflated backward at **3.0% per year** compounded: `base(y) = 263,000 / 1.03^(2023 − y)`.
- BET rate = the statutory rate in effect for each taxable period (RSA 77-E:2).

BET rate history used:

| Period | Rate |
|---|---|
| 2001–2015 | 0.75% |
| 2016–2017 | 0.72% |
| 2018 | 0.675% |
| 2019–2021 | 0.60% |
| 2022 and later | 0.55% |

## 3. Backfilled missing credits (primary schedule)

| Tax year | Worksheet line | Wage base @ 3% | BET rate | Backfilled credit |
|---|---|---:|---:|---:|
| 2015 | 4 (tenth prior) | 207,615 | 0.750% | **1,557** |
| 2016 | 5 (ninth prior) | 213,843 | 0.720% | **1,540** |
| 2017 | 6 (eighth prior) | 220,258 | 0.720% | **1,586** |
| 2018 | 7 (seventh prior) | 226,866 | 0.675% | **1,531** |
| 2019 | 8 (sixth prior) | 233,672 | 0.600% | **1,402** |
| 2020 | 9 (fifth prior) | 240,682 | 0.600% | **1,444** |
| 2021 | 10 (fourth prior) | 247,903 | 0.600% | **1,487** |
| | | | **Total missing** | **10,547** |

Pro forma total carryforward once backfilled:
10,547 + 1,506 + 1,956 + 1,445 + 1,762 = **17,216**.

## 4. Reasonableness check against filed years

Applying the same method to years already on the worksheet:

| Tax year | Model @ 3% | On worksheet | Variance |
|---|---:|---:|---:|
| 2022 | 1,404 | 1,506 | +102 (+7%) |
| 2023 | 1,446 | 1,956 | +510 (+35%) |
| 2024 | 1,490 | 1,445 | −45 (−3%) |
| 2025 | 1,535 | 1,762 | +227 (+15%) |

The model tracks 2022 and 2024 within a few percent. 2023 and 2025 run high
against the model because the actual BET base is compensation **plus**
interest and dividends paid, not wages alone. Treat the backfilled amounts as
a conservative floor.

## 5. Anchor-year sensitivity

$263,000 × 0.55% = $1,446, which matches the **2024** figure on line 13
(1,445), not the 2023 figure (1,956). If $263,000 is actually the 2024 wage
base, every year shifts one notch:

| Tax year | Rate | Credit (2024 anchor) |
|---|---:|---:|
| 2015 | 0.750% | 1,512 |
| 2016 | 0.720% | 1,495 |
| 2017 | 0.720% | 1,540 |
| 2018 | 0.675% | 1,487 |
| 2019 | 0.600% | 1,361 |
| 2020 | 0.600% | 1,402 |
| 2021 | 0.600% | 1,444 |
| | **Total** | **10,241** |

Range across the two anchors: **$10,241 – $10,547**.

## 6. Notes / follow-ups

- A BET credit exists only to the extent BET was **actually assessed and
  paid** for the year. Confirm BET returns were filed for 2015–2021; if not,
  those returns have to be filed (and the tax paid) before the credit is
  claimable on the worksheet.
- The 2015 credit is in its tenth carryforward year on the 2025 worksheet and
  expires after the 2025 period — it is use-it-or-lose-it this filing.
- With BPT of 0, none of the carryforward is absorbed; the schedule's value is
  preserving the credits against future BPT.
- RSA 21-J:29 generally limits refund claims to 3 years, which does not block
  carrying an unclaimed credit forward but does affect any refund posture on
  the older years.

Sources for rate history: NH DRA business tax materials and NHFPI BET rate
history summaries.
