# Document Intake System — Build Plan

**Simms CPA | Companion to `liscio-document-intake-design.md` | August 2026**

The design doc says what the system is. This says how it gets built, in order, with owners. The guiding fact: **almost nothing here is software.** It's Liscio configuration, five templates, one Claude-built generator, and habits installed before January. The build is sequenced so every step is testable before the next one depends on it.

---

## Phase 0 — Prove the Tool (now → end of September)

*Owner: Tyler. Exit criterion: keep/drop decision on Liscio.*

1. Start the Liscio trial. Run the **7-point test** (the workflow plan's 5 points + the 2 added in the design doc §9):
   - Outlook capture → email lands on the correct client record (also send one from an address Liscio doesn't know; time how long it takes to notice and link).
   - Load 10 real clients; send yourself a Request; experience the reminder cadence as a client.
   - Engagement letter template + e-sign one as a fake client (confirm KBA works for 8879 purposes).
   - Ilene and Lyndsey each pull a document out of Liscio to the intake folder.
   - Honest friction notes.
   - Send a Request built from a real prior-year return; confirm conditional questions + check-off.
   - Complete it and run Export ZIP → SmartVault filing, timed (>3 min/client = rethink the bridge).
2. During the trial, answer the two open design questions:
   - **Multi-entity households**: confirm one Contact can link to multiple Accounts, and decide the mapping convention.
   - **Role granularity**: can a scanning-only login be restricted from browsing other clients? If not: kids scan to the Sharp folder, Lyndsey uploads.
3. In parallel: GruntWorx demo + trial Populate on ~20 returns' worth of docs; make the StanfordTax call (lean: skip).

**If the 7 points pass, tool decisions are done and everything below is mechanical.**

## Phase 1 — Foundation Configuration (October)

*Owner: Tyler (decisions), Lyndsey (clicks). ~2–3 afternoons total.*

1. Create the **tag taxonomy** in Liscio (Firm Admin): the 12 tags from design §4. Resist adding more.
2. Write the **naming convention** on one page (the `{Seq}-{Category}-{Issuer}-{Year}` scheme) and pin it where scanning happens.
3. Configure the Sharp **"Tax Intake" one-touch preset** (300 dpi, PDF, duplex).
4. Connect **Outlook** for every firm user whose mail should be captured; MFA verified on each mailbox.
5. Set up **user roles**: Tyler (admin), Ilene, Lyndsey, kids (narrowest role that passed Phase 0 testing).
6. Update the **WISP**: add Liscio, the email-capture flow, the export landing folder (defined, encrypted, cleared after filing), and seasonal-account deactivation to the off-boarding list.

## Phase 2 — The Content Build (November)

*This is the real build month. Owner: Tyler with Claude; Lyndsey loads.*

1. **Load the client list** into Liscio (Contacts + Accounts, using the multi-entity convention from Phase 0). Link Liscio accounts to SmartVault accounts (Account Linking) once, up front.
2. **Build the five Request templates** — the load-bearing artifact:
   - Base 1040
   - + Schedule C add-on
   - + Rental add-on
   - + Brokerage add-on
   - Entity (1120-S / 1065)
   - Draft each from two representative prior-year returns; include conditional questions for the judgment gaps ("Sell any property this year?" → follow-ups).
3. **Build the checklist generator** (the one piece of software): Claude reads a prior-year return PDF → outputs that client's tailored item list, formatted to paste into a Liscio Request built on the right template. Build it, run it on 10 clients, have Tyler spot-check against his mental model — then run the full list in batches.
4. **Template the engagement letter** for e-sign delivery alongside the January Request.

## Phase 3 — Dry Run & Training (December)

*Owner: Lyndsey runs it; Tyler observes. One week of low-intensity testing.*

1. **End-to-end rehearsal with dummy files**: fake client uploads via portal + mobile scan + email + a paper scan → tag/name → check off Request → export ZIP → file in SmartVault → GruntWorx pass → Ilene opens the stack. Every role does their own step.
2. Write the **one-page SOPs** (one per role: scanning, request monitoring + Needs-Filing queue, export/filing). If it doesn't fit on a page, the process is too complicated — simplify it, don't write page two.
3. Set up the **recurring Tasks** in Liscio: weekly unmatched-upload sweep, the Needs-Filing queue conventions.
4. **Draft the January letter**: engagement letter + checklist announcement + portal migration from SmartVault + the March 20 extension-by-default policy (stated now, so it's policy and not a fight in April).

## Phase 4 — Launch (first week of January 2027)

1. **Bulk send** engagement letters + personalized Requests through Liscio.
2. Auto-reminders on. Answers start flowing weeks before the drop-off-first model would produce anything.
3. From here the system is in *operate* mode: the design doc's §5 flow and §6 exception queues are the daily runbook, and the status board runs the day.

## April 16–30 — The Compounding Step

For every extended or painful return, log what was missing into next year's checklist inputs. This is the step that makes year two better than year one — schedule it as a recurring Task now so it survives the post-season exhale.

---

## What Actually Gets Built vs. Configured

| Artifact | Type | Owner | When |
|---|---|---|---|
| 7-point trial results | Decision record | Tyler | Sept |
| Tag taxonomy, roles, Sharp preset, Outlook connections | Configuration | Lyndsey/Tyler | Oct |
| Naming convention + 3 role SOPs | One-pagers | Tyler | Oct–Dec |
| Five Request templates | Liscio content | Tyler | Nov |
| **PY-return → checklist generator** | **Software (Claude)** | **Tyler + Claude** | **Nov** |
| Engagement letter template | Liscio content | Tyler | Nov |
| January letter | Document | Tyler | Dec |
| Recurring exception-queue Tasks | Configuration | Lyndsey | Dec |

Later, only if earned: gap-letter drafter (Feb), business-sale workpaper extractor (Mar), automation of the SmartVault bridge (only if the timed export exceeds ~3 min/client and only after verifying Liscio's API/Zapier situation properly).

## The Two Ways This Fails, and the Guard for Each

1. **A third mouth opens.** Someone hands Tyler a folder and it skips the system. Guard: the same-day rule — anything received personally gets scanned/forwarded into a channel that day, no exceptions, including by Tyler.
2. **The checklist stops being trusted.** If check-offs lag reality, everyone reverts to asking Tyler. Guard: check-off is part of *filing* a document, not a separate chore — a doc isn't "processed" until its Request line is marked. That's in Lyndsey's SOP as the definition of done.
