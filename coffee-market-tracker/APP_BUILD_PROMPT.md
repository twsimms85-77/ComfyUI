# Build Prompt: "Coffee Watch" — Live Coffee Price & News Tracker

Copy everything below the line into Claude Code, Cursor, Lovable, Bolt, or any AI app builder. It is written to be self-contained.

---

## The Prompt

You are a senior full-stack developer. Build a production-quality web app called **Coffee Watch** that tracks the live price of coffee futures and aggregates all coffee-market news in one place, with the news classified by what kind of market driver it is.

### Product overview

A single-user (extendable to multi-user) dashboard for someone following the coffee market. Two things matter: **(1) what is the price doing right now and historically, and (2) what news explains or predicts it.** The app should make the connection between the two visible — news events plotted on the price chart.

### Tech stack

- **Frontend:** React + TypeScript + Vite, Tailwind CSS, Recharts for charts. Typed props everywhere — no `any`.
- **Backend:** Supabase (Postgres + Auth + Row-Level Security + Edge Functions + pg_cron for scheduled jobs).
- **Jobs:** Supabase Edge Functions on cron: price poller (every 15 min during ICE trading hours, hourly otherwise) and news fetcher (every 30 min).
- All API keys live in server-side env vars / Supabase secrets. The service-role key must NEVER be shipped to or referenced in frontend code.

### Data sources

**Prices** (abstract behind a `PriceProvider` interface so the source can be swapped without touching the UI):
- Primary: ICE Coffee "C" Arabica front-month (symbol `KC=F` style) and ICE Robusta front-month, via a free/delayed source (Yahoo Finance unofficial quote endpoint or Barchart free API tier). Data is ~15-minute delayed — the UI must label it "Delayed 15 min," never "live tick."
- Store daily OHLC settlement history for charting; backfill 5 years on first run.
- Also track supporting series: USD/BRL exchange rate and ICE certified stocks (manual-entry admin field if no free feed exists).

**News** (RSS/Atom first — reliable and free; abstract behind a `NewsProvider` interface):
- Daily Coffee News (dailycoffeenews.com), Comunicaffe (comunicaffe.com), Perfect Daily Grind (perfectdailygrind.com), Global Coffee Report (gcrmag.com)
- Barchart/Nasdaq coffee commentary feed
- Google News RSS queries: "coffee futures", "arabica price", "robusta price", "Brazil coffee crop", "Vietnam coffee exports", "coffee frost Brazil"
- USDA FAS coffee reports page and ICO press page (scrape or RSS where available)
- Keep the source list in a `sources` DB table (not hardcoded) so feeds can be added/disabled from an admin settings screen.

### News classification (the differentiating feature)

Each ingested article gets tagged with a **driver category**, reflecting what historically moves this market:
`weather_frost`, `weather_drought`, `enso`, `crop_estimate`, `official_report` (USDA/Conab/ICO), `stocks_inventory` (ICE certified stocks), `currency` (BRL), `logistics_freight`, `policy_tariff_eudr`, `spec_positioning` (CFTC), `demand_consumption`, `origin_news_brazil`, `origin_news_vietnam`, `origin_news_colombia`, `other`.

Plus: `direction_hint` (bullish / bearish / neutral) and `importance` (1–5). Implement classification as a pluggable step: v1 = keyword/rules-based; v2 = LLM call (Claude API) with the article title + summary. Store the classifier version used on each row so tags can be recomputed later.

### Core screens

1. **Dashboard** — big current-price cards for Arabica (¢/lb) and Robusta ($/t) with day change and % change, freshness timestamp, "Delayed" badge; a price chart (1W / 1M / 6M / 1Y / 5Y toggles) with news-event markers overlaid on the timeline (click a marker → article popover); "Today's top stories" list ranked by importance; a small USD/BRL sparkline.
2. **News feed** — reverse-chron, paginated (infinite scroll, 25/page, cursor-based — never load the whole table), filterable by driver category, source, direction, and date range; full-text search; dedup identical stories syndicated across feeds (canonical-URL + fuzzy title match).
3. **Article detail** — summary, link out to original, tags (editable — user corrections stored as `human_override` and never overwritten by re-classification), price change of KC in the 24h and 7d after publication (computed, cached).
4. **Alerts settings** — user-defined rules: price crosses a threshold, daily move exceeds X%, any article tagged `weather_frost` or importance ≥ 4. Delivery v1 = in-app notification center + email via Resend. Store `last_triggered_at` per rule and enforce a cooldown so one frost story doesn't fire 50 emails.
5. **Admin/settings** — manage news sources (add RSS URL, enable/disable, per-source fetch status and last-success timestamp), manual entry for series with no free feed (ICE certified stocks), classifier settings.

### Schema (Postgres)

```sql
-- every table gets: id uuid pk default gen_random_uuid(),
-- created_at timestamptz default now(), updated_at timestamptz
instruments(id, symbol text unique not null, name, unit, exchange)
price_ticks(id, instrument_id fk not null, price numeric not null,
            quoted_at timestamptz not null, is_delayed bool default true,
            source text not null, unique(instrument_id, quoted_at, source))
price_daily(id, instrument_id fk not null, date date not null,
            open numeric, high numeric, low numeric, close numeric not null,
            unique(instrument_id, date))
sources(id, name not null, url not null, feed_url, kind check (kind in ('rss','scrape','api')),
        enabled bool default true, last_fetched_at, last_success_at, failure_count int default 0)
articles(id, source_id fk not null, title not null, url not null unique,
         canonical_url, summary, published_at timestamptz not null,
         raw jsonb, dedup_hash text)
article_tags(id, article_id fk not null, category text not null,
             direction text check (direction in ('bullish','bearish','neutral')),
             importance smallint check (importance between 1 and 5),
             classifier_version text not null, human_override bool default false,
             unique(article_id, category))
alert_rules(id, user_id fk not null, kind, params jsonb not null,
            enabled bool default true, cooldown_minutes int default 240, last_triggered_at)
alert_events(id, rule_id fk not null, fired_at not null, payload jsonb, seen_at)
```

All money/price fields are `numeric` (never float), with the unit defined on the instrument (`usc_per_lb`, `usd_per_tonne`). All timestamps are `timestamptz` in UTC; render in the user's local zone and show ICE trading hours (NY) on the chart.

### Non-negotiable engineering requirements

- **RLS enabled on every table** (Supabase default is OFF — turn it on explicitly). User-owned tables (`alert_rules`, `alert_events`) get `auth.uid() = user_id` policies; shared read-only data (prices, articles) gets authenticated-read, service-role-write policies. Writes from ingestion jobs use the service role via Edge Functions only.
- **Error states:** every fetch has loading, error-with-retry, and empty states. If the price poller fails, the dashboard shows the last known price with a visible "stale since <time>" warning — never a blank card and never a silently stale number.
- **Empty states:** first-run dashboard (no data yet) shows a friendly "backfilling history…" progress state, not a broken chart.
- **Ingestion resilience:** per-source try/catch — one dead RSS feed must not kill the whole fetch run. Increment `failure_count`, auto-disable after 10 consecutive failures, and surface disabled feeds in admin. Respect ETag/Last-Modified to avoid refetching.
- **Rate limits:** the price poller respects the upstream API's limits and backs off exponentially on 429s.
- **Dedup:** enforce at the DB level (unique URL + dedup_hash), not just in app code.
- **Soft delete** (`deleted_at`) for articles and sources rather than hard deletes.
- **Server-side validation** on any user input (alert params, source URLs — validate that a submitted feed URL actually parses as RSS before saving).
- **Mobile:** dashboard and news feed must be fully usable on a phone (this is a check-it-over-morning-coffee app). Chart collapses gracefully; filters move into a drawer.
- **Testing:** unit tests for classifier rules and dedup; one integration test that runs a fake RSS payload end-to-end into `articles` + `article_tags`.

### Build order (do these as separate, working milestones)

1. Schema + migrations + RLS policies + seed instruments and the default source list.
2. Price poller Edge Function + daily backfill + dashboard price cards and chart.
3. News fetcher + rules-based classifier + news feed screen with filters/pagination.
4. Event markers on chart + per-article price-impact computation.
5. Alerts (rules, evaluation job, notification center, email).
6. Admin screen + LLM classifier upgrade behind the pluggable interface.

Start with milestone 1 and show me the schema and RLS policies before writing UI code.

---

## Notes for the user (not part of the prompt)

- **Cost:** everything above runs on free tiers (Supabase free, delayed price data, RSS). The only optional paid piece is the Claude API for v2 classification and Resend beyond free-tier email volume.
- **Legal:** delayed/unofficial price endpoints are fine for personal use; if this ever becomes a public or commercial app, license real-time data (ICE via a vendor like Barchart OnDemand or databento).
- **Scope trap to avoid:** don't ask the builder for "predictions" in v1 — price + classified news + event markers is already the useful product. Forecasting is a v3 experiment, not a foundation.
