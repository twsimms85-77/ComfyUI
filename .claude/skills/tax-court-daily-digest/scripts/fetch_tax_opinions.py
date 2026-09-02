#!/usr/bin/env python3
"""Fetch recent U.S. Tax Court opinions from CourtListener and emit structured JSON.

Data source: CourtListener Atom feed for court `tax` (no auth required) for
metadata, plus the opinion PDF (public, no auth) for full text. The opinion HTML
page is behind an anti-bot WAF, so we use the PDF for text extraction.

The script is READ-ONLY with respect to the watermark: it reads the watermark to
filter out already-digested opinions, but does NOT update it. The digest skill
updates the watermark only after it has successfully written the day's note, so a
crash never silently drops an opinion.

Output: JSON with one object per NEW opinion, matching the SKILL.md fetch contract
(case_name, citation, opinion_type, docket_number, date_filed, opinion_url,
pdf_url, full_text).

Usage:
    python fetch_tax_opinions.py --state <watermark.json> --out <new.json>
    python fetch_tax_opinions.py --no-text            # metadata only, to stdout
"""
import argparse
import io
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import requests

FEED_URL = "https://www.courtlistener.com/feed/court/tax/"
ATOM = "{http://www.w3.org/2005/Atom}"
HEADERS = {"User-Agent": "TaxCourtDailyDigest/1.0 (solo CPA practice tool)"}

CITE_RE = re.compile(
    r"(T\.C\. Memo\. \d{4}-\d+"
    r"|T\.C\. Summary Opinion \d{4}-\d+"
    r"|\d+ T\.C\. No\. \d+"
    r"|T\.C\. No\.? \d+)"
)
DOCKET_RE = re.compile(r"Docket No[s]?\.?\s+([0-9A-Za-z\-,\s]+?)\.")
FILED_RE = re.compile(r"Filed\s+([A-Z][a-z]+ \d{1,2}, \d{4})")


def strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def classify_type(cite: str, summary: str) -> str:
    blob = f"{cite} {summary}"
    if "Memo" in cite or "Memo" in blob:
        return "Memorandum"
    if "Summary Opinion" in cite or "Summary Opinion" in blob:
        return "Summary"
    if "T.C." in cite:
        return "Regular"
    return "Unknown"


def parse_summary(summary: str) -> dict:
    cite_m = CITE_RE.search(summary)
    cite = cite_m.group(1) if cite_m else ""

    docket_m = DOCKET_RE.search(summary)
    docket = docket_m.group(1).strip() if docket_m else ""

    filed = ""
    filed_m = FILED_RE.search(summary)
    if filed_m:
        try:
            filed = datetime.strptime(filed_m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            filed = filed_m.group(1)

    return {
        "citation": cite or "not yet cited",
        "docket_number": docket,
        "date_filed": filed,
        "opinion_type": classify_type(cite, summary),
    }


def fetch_feed() -> str:
    r = requests.get(FEED_URL, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.text


def parse_entries(xml_text: str) -> list:
    root = ET.fromstring(xml_text)
    entries = []
    for e in root.findall(f"{ATOM}entry"):
        opinion_url = ""
        pdf_url = ""
        for link in e.findall(f"{ATOM}link"):
            if link.get("rel") == "alternate":
                opinion_url = link.get("href", "")
            elif link.get("rel") == "enclosure":
                pdf_url = link.get("href", "")

        summary = strip_html(e.findtext(f"{ATOM}summary", default=""))
        cat = e.find(f"{ATOM}category")

        entry = {
            "id": e.findtext(f"{ATOM}id", default="").strip(),
            "case_name": e.findtext(f"{ATOM}title", default="").strip(),
            "opinion_url": opinion_url,
            "pdf_url": pdf_url,
            "published": e.findtext(f"{ATOM}published", default="").strip(),
            "precedential_status": cat.get("term", "") if cat is not None else "",
            "summary_excerpt": summary[:500],
        }
        entry.update(parse_summary(summary))
        entries.append(entry)
    return entries


def extract_pdf_text(pdf_url: str) -> str:
    from pypdf import PdfReader

    r = requests.get(pdf_url, headers=HEADERS, timeout=120)
    r.raise_for_status()
    reader = PdfReader(io.BytesIO(r.content))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    return re.sub(r"[ \t]+", " ", text).strip()


def load_watermark(path: str) -> set:
    if not path:
        return set()
    p = Path(path)
    if not p.exists():
        return set()
    try:
        return set(json.loads(p.read_text(encoding="utf-8")))
    except Exception:
        return set()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--state", default=None,
                    help="watermark JSON path (list of already-digested opinion ids). Read-only.")
    ap.add_argument("--out", default=None,
                    help="write output JSON here (default: stdout)")
    ap.add_argument("--max", type=int, default=25,
                    help="max recent entries to consider (default 25)")
    ap.add_argument("--no-text", action="store_true",
                    help="skip PDF text extraction (metadata only)")
    args = ap.parse_args()

    seen = load_watermark(args.state)
    entries = parse_entries(fetch_feed())[: args.max]
    new = [e for e in entries if e["id"] not in seen]

    if not args.no_text:
        for e in new:
            if not e["pdf_url"]:
                e["full_text"] = ""
                e["text_source"] = "none"
                continue
            try:
                e["full_text"] = extract_pdf_text(e["pdf_url"])
                e["text_source"] = "pdf" if e["full_text"] else "empty"
            except Exception as ex:  # noqa: BLE001
                e["full_text"] = ""
                e["text_source"] = f"error: {ex}"

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": FEED_URL,
        "new_count": len(new),
        "opinions": new,
    }
    payload = json.dumps(result, indent=2, ensure_ascii=False)

    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
        print(f"wrote {len(new)} new opinion(s) -> {out}")
    else:
        print(payload)


if __name__ == "__main__":
    main()
