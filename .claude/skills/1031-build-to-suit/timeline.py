#!/usr/bin/env python3
"""Day-count calendar for a §1031 build-to-suit exchange.

Usage:
    python timeline.py 2026-11-03 --filer 1040
    python timeline.py 2026-06-15 --filer 1065 --reverse

Day 0 is the relinquished transfer date (forward) or the date the EAT takes
title to the replacement land (reverse). Prints Day 45, Day 180, the
unextended return due date, and whether an extension must be filed to
preserve the full 180 days under IRC §1031(a)(3)(B).
"""
import argparse
import datetime as dt

DUE_MONTH_DAY = {
    "1040": (4, 15),
    "1041": (4, 15),
    "1120": (4, 15),
    "1065": (3, 15),
    "1120-S": (3, 15),
    "1120S": (3, 15),
}


def next_weekday(d: dt.date) -> dt.date:
    """Roll a weekend due date forward to Monday (holiday rolls not modeled)."""
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("day0", help="YYYY-MM-DD")
    ap.add_argument("--filer", default="1040", choices=sorted(DUE_MONTH_DAY), help="return type (calendar year assumed)")
    ap.add_argument("--reverse", action="store_true", help="Day 0 is the EAT parking date, not the relinquished sale")
    args = ap.parse_args()

    day0 = dt.date.fromisoformat(args.day0)
    day45 = day0 + dt.timedelta(days=45)
    day180 = day0 + dt.timedelta(days=180)
    m, d = DUE_MONTH_DAY[args.filer]
    due = next_weekday(dt.date(day0.year + 1, m, d))
    needs_ext = day180 > due
    hard_stop = due if needs_ext else day180

    label = "EAT takes title to replacement land" if args.reverse else "relinquished property transferred"
    ident = "identify RELINQUISHED property" if args.reverse else "identify replacement LAND + IMPROVEMENTS"
    print(f"Day 0    {day0}  ({label})")
    print(f"Day 45   {day45}  ({ident}, in writing, delivered)")
    print(f"Day 180  {day180}  (taxpayer must RECEIVE affixed real property; all exchange funds converted)")
    print(f"Return   {due}  (unextended due date, {args.filer}, calendar year)")
    if needs_ext:
        print(f"** EXTENSION REQUIRED ** Day 180 falls after the due date. Without Form 4868/7004 the exchange period ends {due}.")
    else:
        print("Extension not required to preserve the 180 days (do not file the return before day 180).")
    print(f"Hard stop as things stand: {hard_stop}")


if __name__ == "__main__":
    main()
