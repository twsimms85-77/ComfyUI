# Tax Research Automation

A research loop built around Blue J, for a solo NH practice.

Blue J has no public API on a solo seat, so nothing here automates *inside* Blue J. What it automates is the ring around it — the part that actually decides whether you research consistently or only when a client forces it.

```
INTAKE (unattended)  →  TRIAGE (scored, capped)  →  BLUE J (you, ~20 min)  →  CAPTURE (vault)
```

The mechanism that makes this work: **the intake layer drafts the Blue J prompt for you.** You open the vault to two or three fact-specific, paste-ready questions instead of a wall of headlines. That is the difference between intending to stay current and staying current.

---

## What's here

| Path | What it is |
|---|---|
| `skills/fed-tax-pulse/` | Weekly federal guidance digest — Federal Register API + Internal Revenue Bulletin. Includes `scripts/fetch_fed_tax.py`. **Drafts Blue J prompts.** |
| `skills/bluej-capture/` | Paste a Blue J answer → citation audit → IAACC + §6662 tier → client crosswalk → filed to the vault. |
| `skills/state-pulse/` | Weekly NH / VT / ME / MA digest. WebFetch-driven, no scraper. |
| `vault/Blue J Prompt Playbook.md` | The prompt skeleton, worked examples per entity type, the follow-up ladder, and anti-patterns. Drop into the vault. |

These join the two skills already in place — `tax-court-daily-digest` (intake) and `iaacc-tax-research` (analysis) — which the new skills hand off to rather than duplicate.

---

## Install

Copy the three skill folders into your skills directory, alongside the existing ones:

```
# macOS / Linux
cp -r skills/fed-tax-pulse skills/bluej-capture skills/state-pulse ~/.claude/skills/

# Windows (PowerShell)
Copy-Item -Recurse skills\fed-tax-pulse,skills\bluej-capture,skills\state-pulse $HOME\.claude\skills\
```

Then copy the playbook into the vault:

```
vault/Blue J Prompt Playbook.md  →  01 - Tax & CPA\Blue J Prompt Playbook.md
```

Install the one dependency:

```
python -m pip install requests
```

(`tax-court-daily-digest` also needs `pypdf`, which you already have if that digest is running.)

---

## Verify before you schedule

Run the connectivity probe once:

```
python ~/.claude/skills/fed-tax-pulse/scripts/fetch_fed_tax.py --check
```

Expect two `OK` lines. The Federal Register half is an official, stable, documented JSON API and should be solid. The IRB half is an HTML parse — the IRS publishes no JSON API for the Bulletin — so it is the fragile one by design. If it reports `reachable but nothing parsed`, the page layout moved; the digest degrades to Federal Register only rather than failing, and the regexes in `fetch_fed_tax.py` need a touch-up.

Then do a live dry run with no watermark, which prints to stdout and writes nothing:

```
python ~/.claude/skills/fed-tax-pulse/scripts/fetch_fed_tax.py --since-days 14
```

For `state-pulse`, walk the source table in its `SKILL.md` once and confirm each state URL still resolves. VT and ME have both reorganized their sites; fix any dead link in the table before the first scheduled run.

---

## Scheduling

**These must run where the vault is** — your Cowork desktop environment. Cloud-fired Routines run in a container that has neither `C:\Dellcockpit home\Tyler's Vault` nor outbound access to courtlistener.com, federalregister.gov, or irs.gov. Schedule them the same way `tax-court-daily-digest` is scheduled, as local Cowork scheduled tasks.

Suggested rhythm — deliberately staggered so no two land on the same morning:

| When | What | Time cost |
|---|---|---|
| Daily, 4:05 PM ET | `tax-court-daily-digest` *(already running)* | 2 min skim |
| Monday, 8:10 AM ET | `fed-tax-pulse` | ~5 min skim, then 20 min in Blue J on one prompt |
| Friday, 3:40 PM ET | `state-pulse` | 3 min skim |
| Ad hoc | `bluej-capture` after each Blue J session | ~10 min |
| Last Friday monthly | Rollup — sweep `#followup` tags | 20 min |

Off-the-hour minutes are intentional; they keep the jobs from stacking on the same tick.

**One Blue J session a week is the target.** The cap of three deep dives in `fed-tax-pulse` exists to protect that — three well-framed questions you actually research beat twenty you skim.

---

## Design notes

**Watermark discipline.** `fetch_fed_tax.py` reads the watermark and never writes it, matching `fetch_tax_opinions.py`. The skill updates the watermark only after the note is successfully written, so a crash never silently drops an item. On a partial run, only items from sources that actually succeeded get watermarked — a failed source is reported, never swallowed.

**Hard caps.** Every digest caps its deep-dive section at three. Volume is the enemy: a digest that surfaces everything gets skimmed and then ignored.

**Fail loudly.** Every skill has an explicit place to report an unreachable source. A weekly digest that silently omits a failed fetch reads as "nothing happened," which is the one thing it must never imply.

**Verification is the product.** `bluej-capture` exists because the failure mode of AI tax research is not a fabricated citation — it is a real citation attached to a proposition it doesn't quite support. The citation audit table is the point; the reformatting is incidental.

**Separate the machine's read from yours.** Every captured note keeps "what Blue J said" and "where I landed differently" apart. That delta is the professional judgment that makes the file defensible under exam.

---

## Not built

- **No Blue J API integration.** API access appears only in enterprise-tier marketing and is not available on a solo seat. If that changes, `bluej-capture` is the natural place to wire it in — it would replace the paste step, nothing else.
- **No scraper for state sites.** Four states, four HTML layouts, all of which change. WebFetch plus a maintained source table rots more gracefully.
- **No cloud Routines.** They cannot reach the vault. See Scheduling above.
