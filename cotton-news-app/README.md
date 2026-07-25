# Cotton Market Monitor

A single-file dashboard for tracking ICE Cotton No. 2 (CT) futures — prices, news,
supply & demand, positioning, weather, and the report calendar, all in one page.

## Run it

No build step, no dependencies:

```bash
# open directly
open cotton-news-app/index.html        # macOS
xdg-open cotton-news-app/index.html    # Linux

# or serve it
python3 -m http.server 8080            # then visit http://localhost:8080/cotton-news-app/
```

## What's inside

| Panel | Data | Notes |
|---|---|---|
| Futures board | Sample | Contract months with links to Barchart / ICE live quotes |
| Front-month chart | Sample | 90-session line chart with crosshair tooltip |
| Cotton news | Sample | Category-tabbed feed layout + links to real sources (USDA ERS/FAS, Cotlook, Cotton Grower, AgWeb, Reuters) |
| Supply watch | Sample | Acreage, abandonment, crop condition, development pace |
| Supply & demand | Sample | WASDE-style U.S. + world balance sheets, ending-stocks-by-country chart |
| CFTC positioning | **Live** | Managed-money net position fetched from the CFTC public reporting API (Socrata, CORS-enabled); falls back to a labeled sample series |
| Cotton belt weather | **Live** | Current temp + 7-day rain for TX High Plains, Coastal Bend, Delta, Southeast, Gujarat, Mato Grosso, Xinjiang via Open-Meteo (keyless); shows an error state if unreachable |
| Report calendar | Static | Recurring cadence of Crop Progress, Export Sales, COT, WASDE, Ginnings, Plantings/Acreage, FND |
| Contract specs | Static | CT size, tick, months, limits, delivery points, hours |
| Driver cheat sheet | Static | Supply-side and demand-side factors that move cotton |

Every sample-data panel is labeled **SAMPLE DATA** in the UI. Price/news panels are
placeholders because free CORS-accessible quote and RSS endpoints don't exist —
wire in a paid feed (Barchart OnDemand, dtn, ICE Data Services) or a small server-side
proxy to make them live.

Dark mode follows the OS setting; the ◐ Theme button overrides it. The header pill
tracks ICE session hours (9:00 p.m. – 2:20 p.m. ET) against a live ET clock.

Nothing here is trading advice.
