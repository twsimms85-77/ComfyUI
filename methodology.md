# CLX 5-Day Markov Call — Methodology

## Overview
Each cycle produces a single directional call on CLX (Clorox Co., NYSE) over the next
5 trading days, logged to `clxpredictionlog.csv`. The card reports the call, its
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
