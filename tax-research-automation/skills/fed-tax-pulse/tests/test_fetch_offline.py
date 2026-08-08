#!/usr/bin/env python3
"""Offline tests for fetch_fed_tax.py — everything except the socket.

Stubs `requests.get` with realistic Federal Register JSON and IRB HTML so the
parsers, the JSON contract, watermark filtering, sort order, and the partial-
failure path are all exercised without network access.

Run:  python tests/test_fetch_offline.py
"""
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

MOD_PATH = Path(__file__).resolve().parent.parent / "scripts" / "fetch_fed_tax.py"
spec = importlib.util.spec_from_file_location("fetch_fed_tax", MOD_PATH)
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)

FR_JSON = {
    "count": 3,
    "results": [
        {
            "document_number": "2026-14231",
            "title": "Guidance Under Section 643 Regarding Trust Distributions",
            "type": "PRORULE",
            "abstract": "This document contains proposed regulations regarding the "
                        "computation of distributable net income.",
            "action": "Notice of proposed rulemaking.",
            "publication_date": "2026-08-05",
            "effective_on": None,
            "comments_close_on": "2026-10-05",
            "html_url": "https://www.federalregister.gov/documents/2026/08/05/2026-14231/x",
            "pdf_url": "https://www.govinfo.gov/content/pkg/FR-2026-08-05/pdf/2026-14231.pdf",
            "docket_ids": ["REG-112180-25"],
            "regulation_id_numbers": ["1545-BR12"],
            "cfr_references": [{"title": 26, "part": 1}],
            "agencies": [{"name": "Internal Revenue Service"}],
        },
        {
            "document_number": "2026-14099",
            "title": "Tangible Property Regulations; Correcting Amendment",
            "type": "RULE",
            "abstract": "Final regulations under section 263(a).",
            "action": "Final rule.",
            "publication_date": "2026-08-01",
            "effective_on": "2026-09-01",
            "comments_close_on": None,
            "html_url": "https://www.federalregister.gov/documents/2026/08/01/2026-14099/y",
            "pdf_url": "",
            "docket_ids": [],
            "regulation_id_numbers": [],
            "cfr_references": [],
            "agencies": [{"name": "Internal Revenue Service"}, {"name": "Treasury Department"}],
        },
        {
            "document_number": "2026-13980",
            "title": "Proposed Collection; Comment Request for Form 1041",
            "type": "NOTICE",
            "abstract": None,
            "action": "Notice and request for comments.",
            "publication_date": "2026-07-29",
            "effective_on": None,
            "comments_close_on": "2026-09-29",
            "html_url": "https://www.federalregister.gov/documents/2026/07/29/2026-13980/z",
            "pdf_url": "",
            "docket_ids": [],
            "regulation_id_numbers": [],
            "cfr_references": [],
            "agencies": [{"name": "Internal Revenue Service"}],
        },
    ],
}

IRB_INDEX_HTML = """
<html><body>
  <a href="/irb/2026-32_IRB">Internal Revenue Bulletin: 2026-32</a>
  <a href="/irb/2026-32_IRB#RR-2026-14">duplicate link to same bulletin</a>
  <a href="/irb/2026-31_IRB">Internal Revenue Bulletin: 2026-31</a>
  <a href="/irb/2026-30_IRB">Internal Revenue Bulletin: 2026-30</a>
</body></html>
"""

IRB_BULLETIN_HTML = """
<html><body>
<script>var junk = "Rev. Rul. 9999-99 should not be picked up from script";</script>
<p>Rev. Rul. 2026-14 provides the applicable federal rates for August 2026 under
section 1274(d) of the Code. Notice 2026-45 grants filing and payment relief to
taxpayers affected by severe storms in New England. T.D. 10012 finalizes
regulations under section 199A regarding the treatment of specified service
trades or businesses. Rev. Proc. 2026-31 sets forth the inflation-adjusted
amounts for tax year 2027.</p>
</body></html>
"""


class FakeResponse:
    def __init__(self, *, json_data=None, text=""):
        self._json = json_data
        self.text = text

    def json(self):
        return self._json

    def raise_for_status(self):
        return None


def install_stub(*, fr_ok=True, irb_ok=True):
    """Patch fx.requests.get to serve canned payloads."""
    def fake_get(url, params=None, headers=None, timeout=None):
        if "federalregister.gov" in url:
            if not fr_ok:
                raise RuntimeError("simulated Federal Register outage")
            return FakeResponse(json_data=FR_JSON)
        if url.rstrip("/").endswith("/irb"):
            if not irb_ok:
                raise RuntimeError("simulated IRB outage")
            return FakeResponse(text=IRB_INDEX_HTML)
        if "/irb/" in url:
            return FakeResponse(text=IRB_BULLETIN_HTML)
        raise AssertionError(f"unexpected URL: {url}")

    fx.requests.get = fake_get


def check(label, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    print(f"[{status}] {label}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        check.failed += 1


check.failed = 0


def run_cli(argv):
    """Invoke main() with argv and return the parsed --out payload."""
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "new.json"
        old = sys.argv
        sys.argv = ["fetch_fed_tax.py", "--out", str(out)] + argv
        try:
            fx.main()
        finally:
            sys.argv = old
        return json.loads(out.read_text(encoding="utf-8"))


def main():
    print("== Federal Register parser ==")
    install_stub()
    fr = fx.fetch_federal_register("2026-07-01", 100)
    check("3 documents parsed", len(fr) == 3, f"got {len(fr)}")
    check("id namespaced", fr[0]["id"] == "fr:2026-14231", fr[0]["id"])
    check("PRORULE labelled", fr[0]["kind"] == "Proposed regulation", fr[0]["kind"])
    check("RULE labelled", fr[1]["kind"] == "Final rule / Treasury Decision", fr[1]["kind"])
    check("NOTICE labelled", fr[2]["kind"] == "Notice (Federal Register)", fr[2]["kind"])
    check("null abstract -> empty string", fr[2]["abstract"] == "", repr(fr[2]["abstract"]))
    check("comment deadline kept", fr[0]["comments_close_on"] == "2026-10-05")
    check("agencies flattened", fr[1]["agencies"] == ["Internal Revenue Service", "Treasury Department"],
          str(fr[1]["agencies"]))

    print("\n== IRB parser ==")
    irb = fx.fetch_irb(2)
    designators = [i["designator"] for i in irb]
    check("Rev. Rul. found", "Rev. Rul. 2026-14" in designators, str(designators))
    check("Notice found", "Notice 2026-45" in designators, str(designators))
    check("T.D. found", "T.D. 10012" in designators, str(designators))
    check("Rev. Proc. found", "Rev. Proc. 2026-31" in designators, str(designators))
    check("script contents excluded", not any("9999-99" in d for d in designators), str(designators))
    kinds = {i["designator"]: i["kind"] for i in irb}
    check("Rev. Rul. classified", kinds.get("Rev. Rul. 2026-14") == "Revenue Ruling")
    check("T.D. classified", kinds.get("T.D. 10012") == "Treasury Decision")
    check("bulletin dedup by label",
          len({i["id"].split(":")[1] for i in irb}) == 2,
          str({i["id"].split(":")[1] for i in irb}))

    print("\n== End-to-end, no watermark ==")
    install_stub()
    res = run_cli(["--bulletins", "1"])
    check("errors empty", res["errors"] == [], str(res["errors"]))
    check("new_count matches items", res["new_count"] == len(res["items"]))
    check("both sources present",
          {i["source"] for i in res["items"]} == {"federal_register", "irb"},
          str({i["source"] for i in res["items"]}))
    dates = [i.get("date") or "" for i in res["items"]]
    check("sorted newest first", dates == sorted(dates, reverse=True), str(dates))
    contract = {"id", "source", "designator", "kind", "title", "abstract", "action",
                "date", "url", "pdf_url", "docket_ids", "rins", "cfr_references", "agencies"}
    check("fetch contract complete on every item",
          all(contract <= set(i) for i in res["items"]))

    print("\n== Watermark filtering ==")
    with tempfile.TemporaryDirectory() as td:
        wm = Path(td) / "watermark.json"
        wm.write_text(json.dumps(["fr:2026-14231", "fr:2026-14099"]), encoding="utf-8")
        res2 = run_cli(["--state", str(wm), "--bulletins", "1"])
        ids = {i["id"] for i in res2["items"]}
        check("watermarked ids excluded", "fr:2026-14231" not in ids and "fr:2026-14099" not in ids)
        check("unseen id retained", "fr:2026-13980" in ids)
        check("watermark not mutated",
              json.loads(wm.read_text(encoding="utf-8")) == ["fr:2026-14231", "fr:2026-14099"])

        corrupt = Path(td) / "corrupt.json"
        corrupt.write_text("{not json", encoding="utf-8")
        check("corrupt watermark degrades to empty set", fx.load_watermark(str(corrupt)) == set())
        check("missing watermark degrades to empty set",
              fx.load_watermark(str(Path(td) / "nope.json")) == set())

    print("\n== Partial failure ==")
    install_stub(fr_ok=False)
    res3 = run_cli(["--bulletins", "1"])
    check("FR failure recorded in errors",
          any("federal_register" in e for e in res3["errors"]), str(res3["errors"]))
    check("IRB items still returned",
          res3["new_count"] > 0 and all(i["source"] == "irb" for i in res3["items"]))

    install_stub(fr_ok=False, irb_ok=False)
    res4 = run_cli([])
    check("both failures recorded", len(res4["errors"]) == 2, str(res4["errors"]))
    check("no items on total failure", res4["new_count"] == 0)

    print("\n== --check exit codes ==")
    install_stub()
    check("check returns 0 when both sources OK", fx.run_check() == 0)
    install_stub(fr_ok=False)
    check("check returns 1 when a source fails", fx.run_check() == 1)

    print()
    if check.failed:
        print(f"{check.failed} test(s) FAILED")
        sys.exit(1)
    print("all tests passed")


if __name__ == "__main__":
    main()
