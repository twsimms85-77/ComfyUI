---
type: reference
domain: tax-research
tool: Blue J
last_updated: 2026-08-08
tags: [tax-research, blue-j, prompts, reference]
---

# Blue J Prompt Playbook

The difference between a mediocre Blue J session and a good one is almost entirely in the first prompt and the three follow-ups. Blue J's own guidance names three ingredients — **clarity, context, specificity**. This is that, operationalized.

> **Rule of thumb:** if the prompt you're about to send could have been asked by someone who has never met the client, it is too vague. Blue J answers the question you asked. Ask a narrower one.

---

## The skeleton

Every research prompt carries four parts, in this order.

**1 — Facts.** Entity type, state, method of accounting, tax year, dollar magnitude, and the one or two facts that actually drive the issue. Real numbers, not "substantial."

**2 — The question.** One sentence, legally precise. Name the code section if you know it. If you don't, describe the transaction and let Blue J find it.

**3 — The adversarial follow-up.** Always: *"What authority cuts against this, and what is the strongest argument the Service would make?"*

**4 — The deliverable.** "Draft this as a research memo" / "three-paragraph client email" / "bullets for my file."

Parts 3 and 4 can be sent as follow-ups — Ask Blue J holds conversation context, so you never need to restate the facts.

---

## Fill-in template

```
FACTS
[Entity type], [state of residence/formation], [cash or accrual], tax year [YYYY].
[The driving facts, with numbers.]
[Anything already elected, filed, or missed.]

QUESTION
[One precise sentence. Cite the section if known.]

Then, as follow-ups:
→ What authority cuts against this, and what is the strongest argument the Service
  would make?
→ What is the weight of authority here — is this Substantial Authority, or only
  Reasonable Basis? What would move it up a tier?
→ Draft this as [a research memo / a client email / bullets for my file].
```

---

## Worked examples

### 1041 — trust distributions

> A complex trust, calendar-year, situs NH, tax year 2025. Gross income of $140,000 — $95,000 dividends and $45,000 long-term capital gain allocated to corpus under the governing instrument. Trustee made a discretionary distribution of $60,000 to a single beneficiary in September 2025. No 65-day election made.
>
> How is DNI computed here, and how much of the $60,000 distribution carries out taxable income to the beneficiary under §§643 and 661? Does the capital gain allocated to corpus enter DNI given the trustee's discretionary authority?

*Then:* → adversarial → tier → memo.

### 1065 — basis and losses

> A two-member NH LLC taxed as a partnership, cash basis, tax year 2025. Member A has an outside basis of $18,000 at the start of the year and is allocated a $47,000 ordinary loss. Member A personally guaranteed a $200,000 bank note but the LLC has no other recourse debt.
>
> How much of the $47,000 loss can Member A deduct in 2025? Does the personal guarantee increase Member A's basis under §752, and does the at-risk limitation of §465 change the answer?

### 1040 — multi-state

> A NH resident, single, tax year 2025. Wages of $180,000 from a Massachusetts employer, worked 3 days a week in Boston and 2 days remotely from home in NH. Also has $22,000 of net rental income from a VT property.
>
> How is the Massachusetts source income determined for the remote workdays, and what is the correct nonresident apportionment on Form 1-NR/PY? Separately, does the VT rental income create a VT filing obligation and how does it interact with the NH position?

*Note: take the state mechanics to `vt-tax-research` / `state-tax-landscape` — verify Blue J's state answers against primary authority.*

### 1120-S — reasonable compensation

> A NH S corporation, single shareholder-employee, tax year 2025. Net income before officer compensation of $310,000. Shareholder took $60,000 in W-2 wages and $250,000 in distributions. Shareholder is the sole revenue producer, a licensed professional working full time.
>
> What is the authority on reasonable compensation here, and what is the exposure if the Service recharacterizes distributions as wages? What factors do the courts actually weight?

---

## The follow-up ladder

Run these in order. Most of the value is below the first answer.

1. **Adversarial** — *"What authority cuts against this, and what is the strongest argument the Service would make?"*
2. **Weight** — *"Is this Substantial Authority or only Reasonable Basis? What would move it up a tier?"* — feeds §6662 tiering directly.
3. **Circuit** — *"Is the case law you cited binding in the First Circuit, or persuasive only?"*
4. **Currency** — *"Has any of this been changed by legislation or guidance in the last 24 months?"*
5. **Facts that flip it** — *"What single change to my facts would reverse this conclusion?"* — the best planning question there is.
6. **Deliverable** — memo, email, or bullets.

---

## Anti-patterns

| Don't | Do |
|---|---|
| "Is this deductible?" | Give the entity, year, amount, and the specific expenditure. |
| Ask a fresh question in a new chat when it's a follow-up | Stay in the thread — it holds context. |
| Accept the first answer | Run the adversarial pass. Always. |
| Take a citation on faith | Click through. Confirm the authority says what it's cited for. |
| Ask it to be "thorough" | Ask a narrower question instead. Specificity beats adjectives. |
| Use it as primary authority for state issues | Federal + Tax Notes is its strength; state coverage is thin. |
| Leave the answer in Blue J | Run `bluej-capture`. The chat is not work product. |

---

## What Blue J is *not* for

- **State-specific mechanics** — thin coverage. Use `vt-tax-research`, `state-tax-landscape-out-of-state-preparer`, and primary state authority.
- **Anything from the last few weeks** — guidance published very recently may not be indexed yet. `fed-tax-pulse` covers that gap.
- **Client-specific numbers you haven't given it** — it cannot see the return. Upload the document or state the facts.
- **Final authority** — it is a very fast research associate with good citations. The §6662 tier is your call, not its.

---

## After every session

Paste the conversation into `bluej-capture`. It citation-checks, restructures to IAACC with a §6662 tier, records where you departed from Blue J's read, tags affected clients, and files it. Ten minutes on capture is what makes the research compound instead of evaporating.

---

*Related: `iaacc-tax-research` · `bluej-capture` · `fed-tax-pulse` · `vt-tax-research`*
