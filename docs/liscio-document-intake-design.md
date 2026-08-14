# Document Intake System — Design

**Simms CPA | Built on Liscio's documented features | August 2026**

This design turns the two prior planning documents — *QUAESTOR: Liscio as Document Hub (Plan v1)* and the *Tax Season Workflow Redesign Plan* (Aug 9, 2026) — into a concrete intake system, where every component maps to a feature that actually exists in Liscio's user documentation. Nothing below depends on an unverified integration.

---

## 1. Design Goal

One sentence: **every client document, regardless of how it arrives, lands in one place, attached to the right client, checked against that client's expected list, and visibly either RECEIVED, MISSING, or NEW — without Tyler being the index.**

Constraints carried forward from the prior plans:

- ~560 returns, ~220 concurrent in season; solo owner + Ilene (prep) + Lyndsey (admin) + kids (scanning).
- Liscio is the client-facing front door; SmartVault stays the system of record; the Liscio→SmartVault bridge is **manual** (verified — no auto-sync, no confirmed Zapier).
- Two intake mouths only: everything electronic arrives in Liscio, everything paper arrives through the Sharp copier.

---

## 2. Intake Channels → One Front Door

| Channel | How it lands in Liscio | Liscio feature (per user manual) |
|---|---|---|
| Portal upload | Client uploads against a Request or to Files | Requests; Uploading Files |
| Mobile photo | Client scans with phone; auto-crop, light adjustment, PDF conversion | Mobile app Document Scanner |
| Email attachment | Captured and linked to the client's Contact/Account | Outlook 365 / Gmail Email Integration |
| Paper drop-off | Kids scan on Sharp ("Tax Intake" preset: 300 dpi, PDF, duplex) → staff uploads to the client's account | Uploading Files (firm side) |
| Text message | Client texts a photo; staff moves it onto the client record | Liscio texting |

**Rule: no third mouth.** Documents handed to Tyler personally, mailed in, or emailed to a personal address get scanned/forwarded into one of the five channels above the same day. The system only works if the exceptions route into it.

---

## 3. Feature Mapping — What Implements What

Each piece of the intake system is a documented Liscio capability, not a custom build:

**Requests = the per-client expected-documents checklist.**
The core insight from the redesign plan — "last year's return predicts this year's documents" — is implemented as Liscio Requests:

- Build **request templates** for the firm's return archetypes: Base 1040, + Schedule C add-on, + Rental add-on, + Brokerage add-on, + Entity (1120-S/1065) list.
- The Claude PY-return-to-checklist generator reads each prior-year return and outputs the tailored item list, pasted into that client's January Request.
- **Conditional questions** handle the judgment gaps ("Did you sell property this year?" → follow-up items appear only if yes).
- **Automatic reminders** do the chasing. Nobody manually nags.
- **Bulk send** delivers the January wave (engagement letter + checklist) across the whole client list.
- Request status (open items vs. complete) *is* the completeness review — visible to Lyndsey, not resident in Tyler's head.

**Files + Tags + Month/Year = the organization layer.**
- Firm Admin defines the tag taxonomy once (see §4).
- Every inbound file gets Tag + Year on upload; filterable by Month/Year, Account, Active/Archived.
- Liscio's File Intelligence (AI classification/renaming, ~90% claimed accuracy) is a *suggestion layer* — staff confirms, never trusts blind. Same guardrail philosophy as GruntWorx.

**Email Integration = the email mouth.**
- Client emails are linked to the Contact/Account automatically; unknown senders can be turned into new Contacts from the email itself.
- Any email that requires action becomes a **Task** directly from the email ("Turn an Email into a Task").

**Request Export = the SmartVault bridge.**
- When a client's Request completes, the **Export to ZIP** (completed Request PDF + all uploaded files) is the unit of transfer to SmartVault — one download, one filing action into the client/tax-year folder. This makes the manual bridge a *per-client-on-completion* event rather than a daily rummage. Interim sweep for long-running clients: weekly.

**Tasks / Recurring Tasks = the exception queue and the bridge cadence** (see §6).

---

## 4. Conventions (decide once, in November)

**Naming** — return-flow order, matching the paper habit that already works:

```
{Seq}-{Category}-{Issuer}-{TaxYear}.pdf
10-W2-Acme-2026.pdf
20-1099INT-Chase-2026.pdf
30-1099B-Fidelity-2026.pdf
40-K1-SimmsHoldings-2026.pdf
50-SchC-Receipts-2026.pdf
60-Deductions-Property Tax-2026.pdf
```

Sequence bands mirror the return: 10s wages, 20s interest/dividends, 30s brokerage, 40s passthrough, 50s business, 60s deductions/credits, 90s other. GruntWorx output and File Intelligence suggestions get renamed into this scheme at verification.

**Tag taxonomy** (Firm Admin creates; keep it under ~12 tags): `Wages`, `Interest-Dividends`, `Brokerage`, `K-1`, `Business`, `Rental`, `Deductions`, `Estimates-Paid`, `Entity`, `Signed-Docs`, `Needs-Filing`, `Junk`.

**Statuses** — the return tracker stays in ProSeries HomeBase / shared sheet, unchanged: *Not In / Partial / With Ilene / With Tyler / Waiting on Client / Ready / Done*. Liscio Request status feeds it: Request complete → return moves from *Partial* to prep queue.

---

## 5. The Flow, End to End

```
JANUARY (bulk)          IN-SEASON (per document)             ON REQUEST COMPLETE
───────────────         ─────────────────────────            ────────────────────
Engagement letter  →    Doc arrives via any channel          Export Request ZIP
+ personalized          → lands on client record             → file into SmartVault
Request sent via        → tagged + named (§4)                  client/tax-year
bulk send               → checked off on the Request         → GruntWorx pass
(e-sign + auto-         → auto-reminders chase the rest      → Ilene verifies/keys
reminders on)           → exceptions → Needs-Filing queue    → Tyler reviews
                                                             → status: Ready
```

Division of labor (unchanged from Plan v1, now with sharper edges):

- **Kids**: scan paper → upload to the client's Liscio account, apply tags.
- **Lyndsey**: owns Requests (send, monitor, check off), the Needs-Filing queue, and the export-to-SmartVault step on Request completion.
- **Ilene**: works only from complete, GruntWorx-processed stacks; verifies instead of keying.
- **Tyler**: judgment gaps, review, business/sale complexity. Pulled in by the system, not by default.

---

## 6. Exception Handling (the part that usually goes undesigned)

Every intake system fails at its edges. These are named queues, not ad-hoc decisions:

1. **Unmatched sender / unknown email** → Liscio's create-Contact-from-email if it's a real client; otherwise a `Needs-Filing` Task assigned to Lyndsey. Never auto-guess the account.
2. **Password-protected PDFs** → `Needs-Filing` Task; Lyndsey requests the password via Liscio message (not email).
3. **Wrong-client uploads** (spouse uploads to their own contact, business doc on personal account) → weekly recurring Task: sweep Files filtered by recent uploads with no Request match.
4. **Corrected/amended documents** (corrected 1099s, late K-1s) → the new version is uploaded *alongside* the original, tagged, and the filename gets `-CORR` suffix. The Request item is re-opened, which flips the return status back from Ready if needed. Never delete the original — that's the audit trail.
5. **Duplicates** (client uploads the same W-2 three ways) → keep first, archive the rest (Liscio Active/Archived toggle). Never hard-delete client uploads.
6. **The client who won't use the portal** → paper channel exists precisely for them; no shame lane. Track who they are; don't fight it in February.
7. **Junk pages** → GruntWorx discards mechanically; anything ambiguous gets the `Junk` tag and archived, not deleted.

---

## 7. 🔒 Security Flags

- **Access scope**: kids scanning paper should have the narrowest Liscio role available — upload to accounts, no browsing of other clients' documents, no export rights. Verify Liscio's role granularity during the trial; if it can't restrict this, the kids scan to the Sharp folder and *Lyndsey* uploads.
- **MFA** on every Liscio user and every mailbox in the capture path. Non-negotiable.
- **WISP update**: add Liscio, the email-capture channel, and the export-to-SmartVault step to the written security plan (FTC Safeguards Rule / IRS Pub 4557). The intake map in §2 *is* the data-flow diagram the WISP needs.
- **Client steering**: the January letter directs clients away from plain email toward the portal/app — the biggest exposure is documents clients email unencrypted, and only client behavior fixes it.
- **Export ZIPs land on a workstation** between Liscio and SmartVault. Define the landing folder, encrypt the drive, and clear the folder after filing — don't let a shadow archive of client SSNs accumulate in Downloads.
- **Off-boarding**: seasonal helpers (kids) get accounts deactivated at season end. Calendar it now.

---

## 8. 🕳️ Blind Spots Addressed (and two still open)

Addressed in this design: no completeness owner (→ Requests + Lyndsey), no exception paths (→ §6), no versioning of corrected docs (→ §6.4), no audit trail (→ archive-don't-delete + Request export PDF records what was received when), season scaling (bulk send + auto-reminders + conditional templates).

**Still open — needs Tyler's call:**

1. **Multi-entity households**: one family = 1040 + S-corp + rental LLC. Liscio Accounts vs. Contacts mapping must be decided before the November client-list load (one Contact linked to multiple Accounts is the natural fit — verify during trial).
2. **Mid-year knowledge capture**: the July "I sold the rental" phone call still needs its one-line note habit (per-client note in Liscio). No software substitutes for it; next January's checklist generator should read these notes.

---

## 9. Verification — the 5-Point Test, Extended

The existing 5-point trial test stands (Outlook capture → correct record; 10 real clients + reminder cadence; engagement-letter e-sign; staff pulls a document out; honest friction notes). Add two points from this design:

6. Send a **Request built from a real prior-year return** (via the checklist generator) to a test client and confirm conditional questions + check-off behave as designed.
7. Complete that Request and run the **Export ZIP → SmartVault filing** once, timed. If the round-trip exceeds ~3 minutes per client, the bridge cadence (§3) needs rethinking before January, not during it.

---

## 10. 📐 Next Step

**Build the request templates.** Everything else in this design is configuration or habit; the templates (Base 1040 + the four add-ons, with conditional questions) are the one artifact that must exist before the November client-list load and that the checklist generator writes into. Draft them from ten representative prior-year returns — two per archetype — and run test point #6 against them during the Liscio trial.

---

### Sources

- [Requests FAQs — Liscio Help Center](https://support.liscio.me/en/articles/10564518-requests-faqs)
- [Requests collection — Liscio Help Center](https://support.liscio.me/en/collections/11931428-requests)
- [Requests Template — Liscio Help Center](https://support.liscio.me/en/articles/10564489-requests-template)
- [Setting Up Outlook 365 & Gmail Integration — Liscio Help Center](https://support.liscio.me/en/articles/10564406-setting-up-outlook-365-gmail-integration)
- [Turning an Email into a Task — Liscio Help Center](https://support.liscio.me/en/articles/10564389-turning-an-email-into-a-task)
- [Easily Create Contacts in Liscio from Email — Liscio Help Center](https://support.liscio.me/en/articles/10564390-easily-create-contacts-in-liscio-from-email)
- [Files Overview — Liscio Help Center](https://support.liscio.me/en/articles/10561357-files-overview)
- [Uploading Files — Liscio Help Center](https://support.liscio.me/en/articles/10561371-uploading-files)
- [Tasks Overview — Liscio Help Center](https://support.liscio.me/en/articles/10562070-tasks-overview)
- [Recurring Tasks — Liscio Help Center](https://support.liscio.me/en/articles/10574169-recurring-tasks)
- [File Intelligence — Liscio](https://www.liscio.me/features/file-intelligence/)
- [Automated File Renaming — Liscio](https://www.liscio.me/features/automated-file-renaming)
- Internal: *QUAESTOR — Liscio as Document Hub (Plan v1)*, *Tax Season Workflow Redesign Plan* (Google Drive)
