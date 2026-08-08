#!/usr/bin/env python3
"""Fetch new federal tax guidance and emit structured JSON for the weekly pulse.

Two sources, deliberately independent so one failing never kills the run:

  federal_register — api.federalregister.gov, no auth, well-documented and stable.
      Catches proposed regs (PRORULE), final regs / Treasury Decisions (RULE),
      and IRS notices published in the Register (NOTICE).

  irb — the Internal Revenue Bulletin index at irs.gov/irb, parsed from HTML.
      Catches Rev. Ruls., Rev. Procs., Notices, Announcements, and T.D.s as the
      Service publishes them weekly. There is no official JSON API for the IRB,
      so this path is best-effort: it is parsed tolerantly and a failure is
      reported in `errors` rather than raised.

Like the Tax Court fetch, this script is READ-ONLY with respect to the watermark.
It reads the watermark to filter already-digested items but never writes it. The
skill updates the watermark only after the week's note is successfully written,
so a crash never silently drops an item.

Usage:
    python fetch_fed_tax.py --state <watermark.json> --out <new.json>
    python fetch_fed_tax.py --source federal_register --since-days 14
    python fetch_fed_tax.py --check          # connectivity probe, no watermark
"""
import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

FR_API = "https://www.federalregister.gov/api/v1/documents.json"
IRB_INDEX = "https://www.irs.gov/irb"
HEADERS = {"User-Agent": "FedTaxPulse/1.0 (solo CPA practice tool)"}

# Document types worth surfacing. PRESDOCU and CORRECT are noise for this purpose.
FR_TYPES = ["RULE", "PRORULE", "NOTICE"]
FR_AGENCIES = ["internal-revenue-service", "treasury-department"]

FR_FIELDS = [
    "document_number", "title", "type", "abstract", "action",
    "publication_date", "effective_on", "comments_close_on",
    "html_url", "pdf_url", "docket_ids", "regulation_id_numbers",
    "cfr_references", "agencies",
]

TYPE_LABEL = {
    "RULE": "Final rule / Treasury Decision",
    "PRORULE": "Proposed regulation",
    "NOTICE": "Notice (Federal Register)",
}

# Matches the guidance designators the IRB actually uses.
IRB_ITEM_RE = re.compile(
    r"\b("
    r"Rev\.\s?Rul\.\s?\d{4}-\d+"
    r"|Rev\.\s?Proc\.\s?\d{4}-\d+"
    r"|Notice\s?\d{4}-\d+"
    r"|Announcement\s?\d{4}-\d+"
    r"|Ann\.\s?\d{4}-\d+"
    r"|T\.D\.\s?\d{4,5}"
    r"|REG-\d+-\d+"
    r")\b"
)
IRB_LINK_RE = re.compile(r'href="(/irb/(\d{4}-\d+)_IRB[^"]*)"', re.I)


def strip_html(s: str) -> str:
    s = re.sub(r"(?is)<(script|style).*?</\1>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"&nbsp;?", " ", s)
    s = re.sub(r"&amp;?", "&", s)
    return re.sub(r"\s+", " ", s).strip()


# --------------------------------------------------------------------------
# Federal Register
# --------------------------------------------------------------------------

def fetch_federal_register(since: str, max_items: int) -> list:
    """Return Federal Register tax documents published on or after `since`."""
    params = [
        ("per_page", str(min(max_items, 100))),
        ("order", "newest"),
        ("conditions[publication_date][gte]", since),
    ]
    for agency in FR_AGENCIES:
        params.append(("conditions[agencies][]", agency))
    for t in FR_TYPES:
        params.append(("conditions[type][]", t))
    for f in FR_FIELDS:
        params.append(("fields[]", f))

    r = requests.get(FR_API, params=params, headers=HEADERS, timeout=60)
    r.raise_for_status()
    payload = r.json()

    items = []
    for d in payload.get("results", []) or []:
        doc_no = d.get("document_number") or ""
        agencies = [a.get("name", "") for a in (d.get("agencies") or []) if isinstance(a, dict)]
        items.append({
            "id": f"fr:{doc_no}",
            "source": "federal_register",
            "designator": doc_no,
            "kind": TYPE_LABEL.get(d.get("type"), d.get("type") or "Document"),
            "title": (d.get("title") or "").strip(),
            "abstract": (d.get("abstract") or "").strip(),
            "action": (d.get("action") or "").strip(),
            "date": d.get("publication_date") or "",
            "effective_on": d.get("effective_on") or "",
            "comments_close_on": d.get("comments_close_on") or "",
            "url": d.get("html_url") or "",
            "pdf_url": d.get("pdf_url") or "",
            "docket_ids": d.get("docket_ids") or [],
            "rins": d.get("regulation_id_numbers") or [],
            "cfr_references": d.get("cfr_references") or [],
            "agencies": agencies,
        })
    return items


# --------------------------------------------------------------------------
# Internal Revenue Bulletin
# --------------------------------------------------------------------------

def fetch_irb(max_bulletins: int) -> list:
    """Return guidance items listed in the most recent IRB issues.

    Best-effort HTML parse — the IRB has no JSON API. Callers should treat an
    exception here as a partial failure, not a fatal one.
    """
    r = requests.get(IRB_INDEX, headers=HEADERS, timeout=60)
    r.raise_for_status()

    seen_bulletins = []
    for href, label in IRB_LINK_RE.findall(r.text):
        if label not in [b[1] for b in seen_bulletins]:
            seen_bulletins.append((href, label))
    seen_bulletins = seen_bulletins[:max_bulletins]

    items = []
    for href, label in seen_bulletins:
        url = href if href.startswith("http") else f"https://www.irs.gov{href}"
        try:
            br = requests.get(url, headers=HEADERS, timeout=60)
            br.raise_for_status()
        except Exception:  # noqa: BLE001 — one bad bulletin must not kill the rest
            continue

        text = strip_html(br.text)
        # Walk each designator occurrence and take the sentence-ish span after it
        # as the item's description.
        for m in IRB_ITEM_RE.finditer(text):
            designator = re.sub(r"\s+", " ", m.group(1)).strip()
            tail = text[m.end():m.end() + 400]
            desc = re.split(r"(?<=[.])\s+(?=[A-Z])", tail.strip(" .,—-"), maxsplit=1)[0]
            desc = desc.strip()
            if len(desc) < 25:
                continue
            item_id = f"irb:{label}:{designator}"
            if any(i["id"] == item_id for i in items):
                continue
            items.append({
                "id": item_id,
                "source": "irb",
                "designator": designator,
                "kind": classify_irb(designator),
                "title": desc[:300],
                "abstract": "",
                "action": "",
                "date": "",
                "bulletin": label,
                "url": url,
                "pdf_url": "",
                "docket_ids": [],
                "rins": [],
                "cfr_references": [],
                "agencies": ["Internal Revenue Service"],
            })
    return items


def classify_irb(designator: str) -> str:
    d = designator.lower().replace(" ", "")
    if d.startswith("rev.rul"):
        return "Revenue Ruling"
    if d.startswith("rev.proc"):
        return "Revenue Procedure"
    if d.startswith("notice"):
        return "Notice"
    if d.startswith(("announcement", "ann.")):
        return "Announcement"
    if d.startswith("t.d"):
        return "Treasury Decision"
    if d.startswith("reg-"):
        return "Proposed regulation"
    return "Guidance"


# --------------------------------------------------------------------------

def load_watermark(path: str) -> set:
    if not path:
        return set()
    p = Path(path)
    if not p.exists():
        return set()
    try:
        return set(json.loads(p.read_text(encoding="utf-8")))
    except Exception:  # noqa: BLE001 — a corrupt watermark should not block the run
        return set()


def run_check() -> int:
    """Probe both sources and report reachability. Exit 0 only if both work."""
    ok = True
    try:
        items = fetch_federal_register((date.today() - timedelta(days=30)).isoformat(), 5)
        print(f"federal_register: OK — {len(items)} document(s) in the last 30 days")
    except Exception as e:  # noqa: BLE001
        print(f"federal_register: FAILED — {e}")
        ok = False
    try:
        items = fetch_irb(1)
        print(f"irb: OK — {len(items)} item(s) parsed from the latest bulletin")
        if not items:
            print("irb: WARNING — reachable but nothing parsed; the page layout may have changed")
    except Exception as e:  # noqa: BLE001
        print(f"irb: FAILED — {e}")
        ok = False
    return 0 if ok else 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", default=None,
                    help="watermark JSON path (list of already-digested item ids). Read-only.")
    ap.add_argument("--out", default=None, help="write output JSON here (default: stdout)")
    ap.add_argument("--since-days", type=int, default=8,
                    help="Federal Register lookback window in days (default 8)")
    ap.add_argument("--max", type=int, default=100,
                    help="max Federal Register documents to request (default 100)")
    ap.add_argument("--bulletins", type=int, default=2,
                    help="how many recent IRB issues to scan (default 2)")
    ap.add_argument("--source", choices=["all", "federal_register", "irb"], default="all",
                    help="restrict to one source (default all)")
    ap.add_argument("--check", action="store_true",
                    help="probe both sources and exit; ignores watermark")
    args = ap.parse_args()

    if args.check:
        sys.exit(run_check())

    since = (date.today() - timedelta(days=args.since_days)).isoformat()
    seen = load_watermark(args.state)
    items, errors = [], []

    if args.source in ("all", "federal_register"):
        try:
            items.extend(fetch_federal_register(since, args.max))
        except Exception as e:  # noqa: BLE001
            errors.append(f"federal_register: {e}")

    if args.source in ("all", "irb"):
        try:
            items.extend(fetch_irb(args.bulletins))
        except Exception as e:  # noqa: BLE001
            errors.append(f"irb: {e}")

    new = [i for i in items if i["id"] not in seen]
    new.sort(key=lambda i: (i.get("date") or "", i.get("designator") or ""), reverse=True)

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "window_start": since,
        "sources": {"federal_register": FR_API, "irb": IRB_INDEX},
        "new_count": len(new),
        "errors": errors,
        "items": new,
    }
    payload = json.dumps(result, indent=2, ensure_ascii=False)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
        print(f"wrote {len(new)} new item(s) -> {out}")
        if errors:
            print("partial failures: " + "; ".join(errors))
    else:
        print(payload)


if __name__ == "__main__":
    main()
