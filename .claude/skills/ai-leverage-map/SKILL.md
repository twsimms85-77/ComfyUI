---
name: ai-leverage-map
description: Use this skill whenever Tyler asks how he should be using AI, what to automate next, where the practice is leaking time or money, or which of several competing ideas is worth building first. Triggers on "what should I automate", "how should I be using AI", "highest leverage thing I could build", "what's the ROI on this", "where am I leaving money on the table", "what should I build next for the practice", or any request to prioritize among automation ideas. Also triggers when Tyler names one of the ten standing plays — default-holder, call capture, own-corpus RAG, examiner red team, digest-to-outreach, intake pricing, capacity simulation, skill evals, productized state knowledge, kids' skills — and wants to start or resume it. Holds each play with build steps, effort/payoff, and a status ledger. Do NOT use for generating new skills to fill gaps in the library — that is adjacent-possible or skill-builder.
---

# AI Leverage Map

Ten standing high-leverage plays for Tyler's solo NH tax practice and household, each scoped so it can be started in one session. This skill is a **reference and a prioritizer**, not a generator. The work of deciding what is worth building is already done here; the job when this fires is to pick the right play, or to test a new idea against the frame.

## How to use this skill

Three modes. Read the request and pick one.

**Mode A — "what should I do next":** Read the status ledger at the bottom. Recommend exactly one play, not a menu. Justify it in two sentences against the leverage frame. Then ask whether to start it now.

**Mode B — "let's build [play]":** Jump to that play, read its build steps, and start at the first unchecked one. Do not re-pitch the idea; he already bought it.

**Mode C — "is X worth doing":** Score X against the five tests below. Say plainly whether it beats the top unbuilt play in the ledger. If it doesn't, say so and name what does.

Always end by updating the status ledger if anything moved.

## The leverage frame

Five tests. A play worth building passes at least three. Use these to evaluate any new idea, not just the ten below.

1. **Ceiling test** — does it break hours-for-dollars, or just widen the pipe? Breaking the ceiling beats widening it every time. Only one play below (productized knowledge) actually breaks it; that is why it ranks higher than its effort suggests.
2. **Inertia test** — does it work *with* the Enneagram 9 pattern instead of against it? Anything requiring him to initiate cold, repeatedly, will die in week three. Anything that converts a decision into a veto, or makes the default state productive, survives.
3. **Reuse test** — does it assemble things he already built (skills, vault, digest, Perplexity Light graph) rather than requiring net-new invention? Assembly ships; invention stalls.
4. **Compounding test** — does the output become an input to future work? A play that deepens the corpus or tightens the library beats one that produces a one-time artifact.
5. **Cold-decision test** — does it force a hard call at a moment when it is emotionally cheap (November, not February; before the fee is quoted, not after)? Timing is most of the leverage on the practice-management plays.

## The ten plays

### 1. Default-holder — make AI hold the position, not the to-do list
A scheduled agent that converts each open decision into "unless you veto by 4pm, I'm doing X," with the draft email, calendar hold, or fee letter already written.

- **Why his:** 9-enneagram-helper treats AI as a finisher. Wrong lever. A 9 doesn't lack capacity, he lacks ignition — but will move decisively to *stop* something already in motion. This converts every initiation into a veto.
- **First move:** Pick three recurring stalled decisions. Write the cron prompt that drafts each one and pushes at 8am with a 4pm veto window.
- **Build steps:** (a) list the standing decision types; (b) write one draft template per type; (c) cron entry on the existing daily rail; (d) veto channel — reply-to-kill, not approve-to-send; (e) two-week trial, count how many drafts he let through.
- **Effort/payoff:** 1 session / compounds into every other play. Highest leverage on this list.
- **Done looks like:** He has vetoed at least one thing and let at least three through unedited.

### 2. Call capture — voice memo after every client call
Three minutes of rambling into the phone, transcribed, then an agent extracts billable time, action items, open questions, and the client's own framing, and files it to the vault with links.

- **Why his:** The biggest leak in a solo shop is unbilled time and dropped follow-ups, not research speed. Recovering four unbilled hours a month pays for a decade of tokens. He has the vault and the pipeline chops; he just hasn't pointed them at the boring thing.
- **First move:** Wire transcription → a single structured note format. Do not build the whole pipeline; do one call end to end.
- **Build steps:** (a) capture path (phone memo → watched folder or email-in); (b) transcription; (c) extraction prompt with a fixed schema — client, minutes, actions, questions, quotes; (d) vault write with client backlinks; (e) weekly rollup of uncaptured time.
- **Effort/payoff:** 1-2 sessions / direct revenue recovery, measurable in month one.
- **Done looks like:** A week of calls where every one produced a note without him opening a laptop.

### 3. Own-corpus RAG — point Perplexity Light at himself
Rebuild the LangGraph/Tavily graph against memos, prior-year workpapers, and client emails instead of the web.

- **Why his:** The question that matters isn't "what does §280A say," it's "what did I tell the last three clients with this fact pattern, and am I about to contradict myself?" Consistency across clients is both a speed multiplier and a §6662 defense. No solo shop has this; every Big 4 tax practice does.
- **First move:** Swap the Tavily node for a local retriever over one year of memos. Keep the rest of the graph.
- **Build steps:** (a) corpus inventory and PII boundary — decide what never leaves local; (b) chunk and index memos first, workpapers second, email last; (c) replace the search node, keep the synthesis node; (d) force citations back to the source note; (e) add the contradiction check — retrieve prior advice on the same issue and flag divergence.
- **Effort/payoff:** 2-3 sessions / permanent, and it compounds as the corpus grows.
- **Done looks like:** He asks a live client question and gets his own prior memo back with a citation.
- **Watch:** Client confidentiality. Local embeddings or an explicit data-handling decision before any client content moves.

### 4. Examiner red team — adversarial pre-filing gate
Feed the completed memo or return to a **fresh** instance prompted as an IRS examiner or hostile Appeals officer whose job is to find the weakest link and the missing substantiation. Run it *before* assigning the §6662 tier.

- **Why his:** The `do-better` skill shows he already distrusts first-pass output; this formalizes the instinct as a gate rather than a mood. Adversarial-and-separate beats self-review — a model reviewing its own work grades generously.
- **First move:** Write the examiner persona prompt and run it against the last three memos he already filed. See what it finds retroactively.
- **Build steps:** (a) examiner persona — hostile, cites authority, demands substantiation, no credit for good intentions; (b) require a ranked list of attack surfaces, not prose; (c) require the substantiation he'd need to survive each; (d) wire it into iaacc-tax-research as the step before tier assignment; (e) log findings so recurring weaknesses surface.
- **Effort/payoff:** 1 session / defensibility, plus real tier accuracy.
- **Done looks like:** A tier gets revised downward at least once because of what the red team found. That's the skill working, not failing.

### 5. Digest-to-outreach — the Tax Court digest as a revenue engine
Cross-reference each new opinion against the actual client roster and positions actually taken, and output "this touches three clients — here are three drafted one-paragraph emails."

- **Why his:** Best ROI upgrade to something already built and already running daily. Same job, but the output becomes retention and billable conversations instead of awareness.
- **First move:** Build the client-position index — a table of client × issues × positions taken. That's the missing input, not the matching logic.
- **Build steps:** (a) client-position index in the vault; (b) matching pass added to tax-court-daily-digest after scoring; (c) draft email per match, one paragraph, plain English, no fee ask; (d) route through the default-holder (play 1) so silence sends nothing but a veto is one word; (e) track which sends produce replies.
- **Effort/payoff:** 1-2 sessions / directly revenue-generating.
- **Done looks like:** One client replies "thanks for thinking of me" — that's the whole product.

### 6. Intake pricing — quote before the call
Client uploads prior-year returns → agent produces a complexity score, an hours estimate against his historical actuals, a fee quote, and the five questions to ask on the call.

- **Why his:** Solo practitioners bleed most on fixed fees agreed to in the first ten minutes. He already has the pdf and state-landscape skills; this is assembly, not invention. Passes the cold-decision test hard — the price gets set before rapport makes it awkward.
- **First move:** Score fifteen *existing* clients against last year's actual hours and calibrate the complexity model before pointing it at a prospect.
- **Build steps:** (a) complexity factors — entities, states, K-1s, rentals, crypto, foreign, messy books; (b) calibrate weights against historical hours; (c) PDF extraction of the prior-year return; (d) output: score, hours band, fee range, five questions; (e) one-page client-facing version.
- **Effort/payoff:** 2 sessions / protects margin on every engagement afterward.
- **Done looks like:** He quotes a new client from the sheet and the actual hours land in the predicted band.

### 7. Capacity simulation — simulate busy season in November
Client list × complexity score × historical hours → a week-by-week capacity forecast that names who to reprice, defer, or release, produced in autumn.

- **Why his:** Two things make it fit. It forces the hard call when it's emotionally cold rather than in February when it's hot, and a 9 will act on a number far more readily than on a feeling. Pair with play 1 — the model proposes the fee letters, he vetoes the ones he can't stomach.
- **First move:** Requires play 6's complexity scores. Don't start this first.
- **Build steps:** (a) inherit complexity scores; (b) map deadlines to weeks; (c) overlay available hours honestly, including the four kids' calendar; (d) surface the overflow weeks; (e) rank clients by hours-per-dollar and name the bottom decile; (f) draft the reprice/release letters.
- **Effort/payoff:** 1 session on top of play 6 / one of the few things that changes how the whole season feels.
- **Done looks like:** At least one fee letter goes out before December 1.
- **Timing:** Run annually, first week of November. Cron it.

### 8. Skill evals — treat the library like software
Thirty real prompts he'd actually type, each asserting which skill should fire, run monthly through skill-creator's eval tooling.

- **Why his:** ~25 skills plus two meta-skills that generate more. The library is software now, with software's failure mode: a tax skill that silently stops triggering doesn't error, it just produces confidently unstructured advice at the exact moment IAACC rigor was needed. Overlapping descriptions (iaacc-tax-research vs vt-tax-research vs repair-regulations-test) are where this bites.
- **First move:** Write ten prompts covering the tax skills only. Ten beats zero and ships today.
- **Build steps:** (a) 30 prompts from real history, phrased the way he actually phrases them; (b) assert expected skill per prompt; (c) baseline run, record failures; (d) fix descriptions, not skill bodies; (e) monthly cron; (f) add a case whenever a new skill lands.
- **Effort/payoff:** 1 session / protects everything else on this list. Boring and unglamorous, which is why it will keep getting deferred — schedule it rather than intending it.
- **Done looks like:** A trigger regression gets caught by the suite before it costs him a bad answer.

### 9. Productized state knowledge — the only ceiling-breaker here
Package `state-tax-landscape-out-of-state-preparer` and the VT work as a maintained skill pack, paid newsletter, or subscription digest for solo NH/VT/ME preparers.

- **Why his:** Encodes exactly what every other solo preparer fumbles and can't justify researching. Packaging is nearly free now, and he's ~80% of the way to the content. This is the only play that decouples revenue from his hours — every other one just makes his hours better.
- **First move:** Do not build a product. Post one genuinely useful VT-mechanics piece where other preparers gather and see if anyone bites.
- **Build steps:** (a) audience test with one free artifact; (b) pick the form — skill pack, newsletter, or digest — based on what got a response; (c) scope maintenance honestly, since stale state guidance is worse than none; (d) price it; (e) decide the annual update cadence *before* selling anything.
- **Effort/payoff:** Ongoing / the only uncapped payoff on this list.
- **Done looks like:** One stranger pays, or three ask when it's coming.
- **Watch:** Maintenance burden lands in busy season. Structure so a lapse degrades gracefully.

### 10. Kids' skills — build SKILL.md with the 12, 13, and 15-year-old
Not "let them use ChatGPT for homework." Sit down and build a real skill for something they actually care about, the way marinade-chef got built.

- **Why his:** The 15-year-old enters a labor market where composing and evaluating agents is baseline. The transfer from him is a decade of head start. Secondary benefit that's real: it's a shared project with a teenager, which is the scarcest resource in a house with kids at 6, 12, 13, and 15.
- **First move:** Ask each one what they'd want a computer to be good at. Build whichever answer is most absurd — engagement beats utility here.
- **Build steps:** (a) one kid, one skill, one sitting; (b) they write the description, he writes the structure; (c) test it live so they see it fire; (d) let it be bad; (e) revisit in a month and let them improve it.
- **Effort/payoff:** One evening / decades.
- **Done looks like:** One of them edits their skill without being asked.

## Bonus plays

**Brand pipeline (ComfyUI).** A locked workflow JSON plus fixed seed and LoRA gives 52 weeks of visually identical tax-explainer graphics at near-zero marginal cost. Pair with `graphic-designer` to fix the palette once. A CPA with genuinely consistent visual output is a rounding error away from nonexistent.

**Annual pattern read.** Feed a year of vault notes to `whats-underneath` longitudinally instead of in-the-moment, and ask what he kept circling and never resolved. 9s systematically under-register their own preferences in real time but leave the evidence in writing. This is the one thing he cannot do for himself.

## Recommended sequence

Play 1 first — it changes the odds on everything after it. Then 8 (cheap, protective, and will otherwise never happen). Then 5 and 4, both one-session upgrades to things already running. Then 6 → 7 as a pair, timed to land before November. Play 3 when there's a real block of time. Play 9 runs in the background at low intensity, permanently. Play 10 on a weekend, not a workday.

Never run more than two in-flight at once. Two half-built pipelines is the characteristic failure mode here, and it looks like progress right up until neither ships.

## Status ledger

Update on every use of this skill. Status: `unbuilt` / `in-flight` / `live` / `abandoned`.

| # | Play | Status | Last touched | Next step |
|---|------|--------|--------------|-----------|
| 1 | Default-holder | unbuilt | — | List three standing decisions |
| 2 | Call capture | unbuilt | — | Wire one call end to end |
| 3 | Own-corpus RAG | unbuilt | — | Decide the PII boundary |
| 4 | Examiner red team | unbuilt | — | Write the persona, test on 3 old memos |
| 5 | Digest-to-outreach | unbuilt | — | Build the client-position index |
| 6 | Intake pricing | unbuilt | — | Score 15 existing clients vs actual hours |
| 7 | Capacity simulation | unbuilt | — | Blocked on 6 |
| 8 | Skill evals | unbuilt | — | Write 10 tax-skill prompts |
| 9 | Productized state knowledge | unbuilt | — | Post one free VT piece |
| 10 | Kids' skills | unbuilt | — | Ask each kid the question |

## Adding a play

Score it against the five tests first and say the score out loud. Three or more passes, and it earns a row. Fewer, and say plainly why it doesn't — a list of twenty plays is a list of zero plays. When adding, match the existing shape: one-line description, why-his, first move, build steps, effort/payoff, done-looks-like.

Retire a play the moment it goes `live` and has run unattended for a month. It belongs to its own skill by then, not to this map.
