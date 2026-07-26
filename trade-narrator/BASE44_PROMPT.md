# Trade Narrator — Base44 Prompt (final)

Paste everything inside the code fence into Base44. Decisions already made:
v1 uses **manual price/volatility entry** (works immediately, no API keys);
the v2 section at the bottom tells Base44 how to add live data and alerts later.

```
Build an app called "Trade Narrator" — a disciplined trading assistant that tells me
in plain English when to get into a trade and when to get out. The core rule of the
entire app: I can only trade a market when that market's volatility watch criteria
have been met. The app's job is to enforce my own rules so emotion never makes the
decision. Version 1 uses manual entry for prices and volatility readings — I type
the current number, the app makes the call.

== DATA MODEL ==

Settings (single record):
- account_size (dollars), default_risk_percent (default 1%), max_open_trades
  (default 2), max_daily_loss (dollars), created_at, updated_at

Market:
- name, symbol, market_type (stock / futures / crypto / forex),
  status (WATCHING / ELIGIBLE / IN_TRADE), notes, created_at, updated_at

WatchCriteria (one per market — a market cannot be created without it):
- market_id, volatility_metric (ATR / % daily range / VIX level / IV rank / custom),
  threshold_value, threshold_direction (above / below), current_value
  (manually entered), criteria_met (boolean, computed: current_value vs threshold),
  last_checked_at

TradePlan (created only when a market is ELIGIBLE):
- market_id, direction (long / short), entry_criteria (checklist, one item per
  line), exit_criteria_profit (text), exit_criteria_stop (text), entry_price,
  stop_price, target_price, risk_percent, calculated_position_size, dollar_risk,
  dollars_committed, status (ACTIVE / CLOSED), created_at

Trade (execution record):
- trade_plan_id, actual_entry_price, actual_exit_price, exit_reason
  (target hit / stop hit / manual override), profit_loss_dollars,
  narration_log (timestamped text entries), opened_at, closed_at

== SCREENS ==

1. MARKET WATCH (home screen)
A card grid of all my markets, ELIGIBLE sorted to the top. Each card shows:
symbol, current volatility value vs threshold, and a status badge — LOCKED
(gray), ELIGIBLE (green), or IN TRADE (blue). Each card has an inline field to
type the current volatility reading plus an Update button; updating recomputes
criteria_met. LOCKED cards have their "Plan Trade" button disabled with the
message "Volatility criteria not met — this market is locked." The Add Market
flow defines the market and its watch criteria together.

2. TRADE PLAN WIZARD (only reachable from an ELIGIBLE market)
Step 1 — Entry criteria: I type my entry checklist, one condition per line.
Step 2 — Exit criteria: direction (long/short), profit exit in words, stop-loss
exit in words, plus entry price, stop price, target price. Validate the geometry:
long requires stop < entry < target; short requires target < entry < stop.
A plan without a stop-loss cannot be saved.
Step 3 — Bet size: the calculator below runs inline; then every entry-criteria
line must be checked off as true right now before "Open Trade" activates.
Saving sets the market to IN_TRADE. Block new plans when open trades ≥
max_open_trades or today's realized losses ≥ max_daily_loss (show why).

3. BET SIZE CALCULATOR (inline in the wizard AND standalone in the nav)
Inputs: account size (from Settings), risk % per trade, entry price, stop price.
Outputs: dollar risk (account × risk %), risk per unit (|entry − stop|),
position size = floor(dollar risk ÷ risk per unit) — always round DOWN to whole
units — dollars committed (size × entry), and actual risk at that size.
Warnings: risk % above 2%; committed dollars above account size (leverage);
error when size rounds to zero (stop too far for the risk budget).

4. ACTIVE TRADE / "GET OUT" SCREEN
One card per active trade, designed for a two-second glance. Shows the exit
criteria I wrote, entry/stop/target, a field to type the current price, and a
giant narration banner with exactly three possible states:
"HOLD — no exit criteria met",
"TAKE PROFIT — target reached, get out", or
"STOP — exit now, stop-loss hit".
Stop-loss check takes priority over target. When the banner says STOP, the Exit
button fires with ONE tap and no confirmation dialog. Exiting with no signal
active is allowed but recorded as exit_reason "manual override". Exiting records
actual exit price, computes P&L (direction-aware), appends to the narration log,
closes the trade, and returns the market to WATCHING with its current volatility
value cleared — it must re-qualify before the next trade.

5. JOURNAL
Summary tiles: total P&L, win rate, average win, average loss, and a count of
"manual override" exits highlighted in red (it measures rule-breaking). Below,
a table of closed trades: date, market, direction, entry, exit, P&L, exit
reason. Tapping a row shows that trade's full narration log.

6. SETTINGS
Account size, default risk %, max open trades, max daily loss. Framed as
"the rules you answer to."

== RULES TO ENFORCE IN LOGIC, NOT JUST UI ==
- A TradePlan can never be created for a market whose criteria_met is false.
- Only one active trade per market.
- Every state change (eligible, plan created, price checked, exit signal shown,
  trade closed) is appended to the narration log with a timestamp.
- A market that just closed a trade must have its volatility re-entered and
  re-qualify before it can be traded again.

== STYLE ==
Dark theme only (deep blue-black ground, not pure black), high contrast, large
touch targets — this gets used on a phone while watching markets. Monospace
tabular numerals for all prices and dollar figures. Status colors: gray =
locked, green = eligible/profit, blue = in trade, red = stop/loss, amber =
warnings. No confirmation dialog on the STOP state — when it says get out,
one tap gets out.

== V2 (build after v1 works) ==
- Live data: integrate Polygon.io (stocks) and/or an exchange API (crypto) to
  auto-refresh current price and ATR/% daily range every minute during market
  hours, replacing manual entry. Keep manual entry as a fallback.
- Alerts: push/email notification when a LOCKED market's criteria flip to
  ELIGIBLE, and when an active trade's price crosses stop or target.
- Auth: require login before anything loads; all data is private per user.
```

## Notes

- **Volatility is concrete, not vibes**: each market carries one metric
  (ATR, % daily range, VIX, IV rank) with a numeric threshold. "Most volatile
  situations" = the threshold you set.
- **The manual-override counter is the point of the app** — it narrates *you*,
  not just the trade.
- A working reference implementation of this exact spec lives in
  `index.html` next to this file (open it in any browser; data stays in
  localStorage).
