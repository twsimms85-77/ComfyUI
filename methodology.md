# CLX 5-Day Markov Call — Methodology

## Overview
Each cycle produces a single directional call on CLX (Clorox Co., NYSE) over the next
5 trading days, logged to `clx-prediction-log.csv`. The card reports the call, its
probability, and the running hit rate and Brier score over all resolved prior calls.

## Model
1. **States.** Each trading day is classified UP (`U`) or DOWN (`D`) from its close-to-close
   return.
2. **Transition matrix.** `P(U|U)` and `P(U|D)` are estimated from the observed state
   sequence with **Beta(2,2) shrinkage** toward 0.5 (add 2 pseudo-counts per outcome),
   because the usable sample in this environment is small.
3. **Magnitudes.** Mean up-day and down-day returns are estimated from the same window,
   **excluding earnings-driven sessions** (no earnings fall inside a normal 5-day horizon).
   Per-day noise is modeled as Gaussian with σ = 0.8%.
4. **Simulation.** 200,000 Monte Carlo paths (fixed seed = cycle date), 5 steps from the
   current state. The call is UP if `P(cumulative return > 0) ≥ 0.5`. The card reports the
   median path target and the 10–90% band.

## Scoring
A call resolves at the close of the 5th trading day after the reference close.
- **Hit** = 1 if sign(actual 5-day return) matches the call.
- **Brier** = `(p_up − outcome)²` where outcome = 1 if the period closed up, else 0.
- Running hit rate and Brier are simple averages over all resolved rows in the log.

## Data sourcing (environment constraint)
This session runs in a sandbox whose egress proxy **blocks every market-data host**
(stooq, Yahoo, Nasdaq, stockanalysis, macrotrends, stockscan were all tested and denied).
`WebSearch` is the only working channel, so daily closes are **reconstructed from search
snippets** and cross-checked arithmetically (e.g. a quoted % change is back-solved against
the neighboring close). Conflicting snippets are resolved in favor of explicitly quoted
changes over cross-source subtraction, and the provenance note is kept in the log row.
This limits the estimation window to roughly the trailing two weeks; a proper data
connector (e.g. Alpha Vantage MCP) would restore a full 60-day window and should replace
snippet reconstruction when available.

## 2026-08-07 bootstrap notes
- First logged cycle; log had never been committed (prior scheduled run failed with no
  network access), so hit rate and Brier start at 0/0 and n/a.
- Reconstructed closes: Jul 30 ≈ 96.69 (implied), Jul 31 95.53, Aug 3 98.26 (+2.86%,
  Q4 FY26 earnings beat), Aug 4 104.67 (+6.5%), Aug 5 105.84, Aug 6 105.80.
- Aug 6 was treated as an up-state per the explicitly quoted +0.19% session change,
  though subtraction against the Aug 5 snippet gives −0.04%; either way the magnitude
  is ~flat and does not move the transition estimates materially.
- Earnings sessions Aug 3–4 were excluded from magnitude estimation but retained in the
  transition counts.
- Resolved 2026-08-14: Aug 13 close $106.54, +0.70% over the horizon → hit (call was UP,
  p=0.567), Brier (0.567 − 1)² = 0.1875. Running: 1/1, Brier 0.1875.

## Copper futures variant (`copper-prediction-log.csv`)
Same model applied to **COMEX copper futures, front month (HG)**, quoted in $/lb, using
daily settlement prices. Differences from the CLX setup:
- No earnings exclusion; instead, days whose settle had to be *implied* rather than found
  (direction inferred from context, magnitude estimated) are retained in transition counts
  but **excluded from magnitude estimation**.
- Per-day noise σ = 1.0% (copper runs hotter than CLX's 0.8%).
- Resolution uses the front-month settle 5 trading days after the reference settle. Note
  the front month can roll inside a horizon; score against the same contract's settle
  where snippets allow, otherwise the continuous front-month quote, and record which.

### 2026-08-14 bootstrap notes
- Reconstructed settles: Aug 4 ≈ 6.617 (implied), Aug 5 6.703 (record, +1.3%),
  Aug 6 ≈ 6.58 (ATH near 6.90 intraday then profit-taking), Aug 7 ≈ 6.55 (direction
  inferred: TE described Aug 10–12 as a three-session rising streak, so Friday was not
  an up day), Aug 10 ≈ 6.60, Aug 11 6.61, Aug 12 6.6335, Aug 13 ≈ 6.607 (CPER −0.42%).
- Regime: record rally (tariff-driven hoarding, LME squeeze, Indonesia smelter outage,
  tame US CPI Aug 12). Transition counts came out perfectly balanced after shrinkage
  (P(U|U) = P(U|D) = 0.50), so the DOWN call is driven by return asymmetry: observed
  down days (−1.8%, −0.4%) outweigh non-record up days.
