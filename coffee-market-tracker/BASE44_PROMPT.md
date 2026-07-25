# Base44 Prompt: "Coffee Watch"

Base44 handles its own stack (database, auth, hosting), so this version drops the
Supabase/React infrastructure details from `APP_BUILD_PROMPT.md` and is written as a
product-level prompt. Paste everything below the line into Base44.

---

Build an app called "Coffee Watch" — a personal dashboard that tracks the price of coffee futures and aggregates all coffee-market news in one place, with each news story classified by what kind of market driver it is. The key idea: connect price and news, so I can see what's moving the market.

PAGES

1. Dashboard
- Two big price cards: Arabica coffee (US cents per pound) and Robusta coffee (US dollars per tonne), each showing current price, daily change, and percent change, with a timestamp and a "Delayed data" badge.
- A price history line chart with time range toggles (1 week, 1 month, 6 months, 1 year, 5 years).
- News event markers overlaid on the chart timeline — clicking a marker shows the related article.
- A "Today's Top Stories" list showing the 5 most important recent articles.
- If price data can't be refreshed, show the last known price with a visible "stale since [time]" warning — never a blank card.

2. News Feed
- Reverse-chronological list of all articles: headline, source, published date, summary, driver category tag, bullish/bearish/neutral badge, and importance (1–5 stars).
- Filters: driver category, source, direction (bullish/bearish/neutral), date range. Plus keyword search.
- Paginate or infinite-scroll — never load everything at once.
- Clicking an article opens a detail view: full summary, link to the original, editable tags (my manual edits are marked as overrides and never overwritten by auto-classification), and the Arabica price change in the 24 hours and 7 days after the article was published.

3. Alerts
- Let me create alert rules: price crosses a threshold, daily move exceeds X%, or any article tagged with a chosen category (e.g. "Frost") or importance 4+.
- In-app notification center plus email notifications. Each rule has a cooldown (default 4 hours) so one event doesn't fire repeated alerts.

4. Settings / Sources
- A manageable list of news sources (name, URL, RSS feed URL, enabled on/off, last fetched time, failure count). I can add or disable sources.
- A manual-entry form for ICE certified coffee stocks (a weekly number I'll type in myself), shown as a secondary line on the dashboard.

DATA & AUTOMATION

- Fetch Arabica (ICE Coffee "C", symbol KC=F) and Robusta front-month futures prices from a free/delayed source (e.g. Yahoo Finance quotes) every 15 minutes, and store daily open/high/low/close history for the chart. Backfill as much daily history as possible on first run. Always label prices as delayed, not live.
- Fetch news every 30 minutes from these RSS feeds (seed these as the default sources):
  - Daily Coffee News: https://dailycoffeenews.com/feed/
  - Comunicaffe: https://www.comunicaffe.com/feed/
  - Perfect Daily Grind: https://perfectdailygrind.com/feed/
  - Global Coffee Report: https://gcrmag.com/feed/
  - Google News RSS searches for: "coffee futures", "arabica price", "robusta price", "Brazil coffee crop", "Vietnam coffee exports", "coffee frost Brazil"
- Deduplicate articles by URL and near-identical titles (the same story appears on multiple feeds).
- If one feed fails, skip it and continue with the others — one broken source must never stop the whole fetch. Auto-disable a source after 10 consecutive failures and show that in Settings.

NEWS CLASSIFICATION (the most important feature)

Auto-tag every article using AI with:
- Driver category (pick the best fit): Frost, Drought, El Niño/La Niña, Crop Estimate, Official Report (USDA/Conab/ICO), Inventory/Certified Stocks, Currency (Brazilian real), Logistics/Freight, Policy/Tariffs/EUDR, Speculative Positioning, Demand/Consumption, Brazil Origin News, Vietnam Origin News, Colombia Origin News, Other.
- Direction: Bullish, Bearish, or Neutral for coffee prices.
- Importance: 1–5, where 5 = likely to move the futures market (e.g. a Brazil frost warning or a surprise USDA number) and 1 = general industry news.

DESIGN

- Clean financial-dashboard look, dark mode support, coffee-brown accent color.
- Fully mobile-friendly — this is a "check the market over morning coffee" app. Filters collapse into a drawer on mobile.
- Every screen has proper loading, error, and empty states (first run should say "Backfilling price history…" instead of showing a broken chart).

Start by building the data model and the Dashboard page, then the News Feed, then Alerts, then Settings.
