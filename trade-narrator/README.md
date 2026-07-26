# Trade Narrator

A disciplined-trading assistant: you predefine entry/exit criteria and risk
rules, and the app tells you in plain English when to get in and when to get
out. Its core rule: **a market can only be traded when its volatility watch
criteria are met** — the app only lets you act on the most volatile setups
you defined in advance.

## What's here

| File | What it is |
|---|---|
| `index.html` | A complete, working v1 of the app. Open it in any browser (works great on a phone). No server, no build step — data is saved in the browser's localStorage. |
| `BASE44_PROMPT.md` | The finalized prompt to paste into Base44 if you'd rather have Base44 generate a hosted version with accounts and (in v2) live market data. |

## The five screens

1. **Watch** — your markets, each with a volatility metric + threshold.
   Locked (gray) until criteria are met, then Eligible (green). Locked markets
   cannot open the trade planner.
2. **Sizer** — bet size calculator: account × risk % ÷ per-unit risk, rounded
   down, with warnings above 2% risk.
3. **Trades** — the "get out" screen. Type the current price; the banner says
   exactly one of HOLD / TAKE PROFIT / STOP. Stop wins ties, and a STOP exit
   is one tap with no confirmation.
4. **Journal** — P&L, win rate, and a red "rule breaks" counter for exits
   taken with no signal (manual overrides).
5. **Settings** — account size, risk %, max open trades, max daily loss.
   Trading locks when the daily loss limit is hit.

## v1 vs v2

v1 is manual-entry: you type the current price/ATR, the app makes the call.
That's deliberate — it works today with zero API keys. The v2 section of the
Base44 prompt covers live data feeds (Polygon.io etc.) and eligible/stop
alerts.
