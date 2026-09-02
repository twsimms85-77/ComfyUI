---
name: marinade-chef
description: Use this skill whenever Tyler asks about marinating, brining, or seasoning steak or chicken before cooking. Triggers on "marinade for steak", "how long should I marinate chicken", "what do I do with these chicken thighs", "I've got flank steak, ideas?", "dry brine", "should I marinate this", "make a marinade with what I have", or any request to build, scale, time, or troubleshoot a marinade. Also fires when Tyler names a cut (flank, skirt, hanger, sirloin, ribeye, chicken thighs, breasts, wings, spatchcocked bird) and asks how to prep it. Returns a scaled recipe with exact amounts, a marinating window, and cook targets. Do NOT use for full weekly meal planning — that's dinner-winner.
---

# Marinade Chef

Build marinades that actually work on the specific cut in front of you, scaled to weight, with a defensible time window and a cook target. No vague "marinate 2–4 hours or overnight." Every answer commits to a number.

**Governing principle:** salt is the only ingredient that meaningfully penetrates meat. Everything else lives in the top 2–3 mm. Design accordingly — build flavor for the surface, build seasoning for the interior, and never let acid or enzymes run long enough to wreck texture.

---

## Step 1 — Classify the protein

Route to the right treatment before writing a single ingredient.

| Protein | Treatment | Why |
|---|---|---|
| Thick steak (ribeye, strip, filet, thick sirloin, 1"+) | **Dry brine only.** No wet marinade. | Wet surface kills the crust. Marinade never reaches the middle. Add flavor after the sear (compound butter, chimichurri, pan sauce). |
| Thin / tough steak (flank, skirt, hanger, flap, sirloin tip, chuck steak) | **Wet marinade.** | High surface-to-mass ratio — the 2–3 mm flavor zone is a real fraction of the bite. Acid also softens the surface of a chewy cut. |
| Chicken thighs (bone-in or boneless) | **Wet marinade.** Forgiving, hard to ruin. | Fat and connective tissue buffer both acid and overcooking. |
| Chicken breast | **Wet marinade with a dairy or brine base**, not a hard acid. | Lean and unforgiving; citrus/vinegar over ~2 hrs turns the surface chalky and mushy. |
| Wings / drumsticks | **Dry brine w/ baking powder**, then sauce after cooking. | Dry skin = crisp skin. A wet marinade on wings is a texture penalty for no flavor gain. |
| Whole / spatchcocked bird | **Dry brine, 12–24 hrs uncovered in the fridge.** | Seasons all the way through and dries the skin. |

If the cut is ambiguous, ask ONE question: thickness, or bone-in vs boneless. Then proceed.

---

## Step 2 — Build the marinade to formula

**Base architecture, per 2 lb of protein:**

- **Fat — 1/3 cup** (olive, neutral, sesame as accent). Carries fat-soluble aromatics onto the surface; prevents sticking.
- **Acid — 2 tbsp**, or **1/2 cup if dairy-based**. Flavor and surface tenderizing. This is the ingredient with a hard time limit.
- **Salt — 1.5 tsp Diamond Crystal kosher per lb** (≈1% by weight). Use 1 tsp/lb for Morton's, 3/4 tsp/lb for table salt. If soy sauce or fish sauce is in the build, count it: **1 tbsp soy ≈ 1/2 tsp kosher salt** and reduce accordingly.
- **Sugar — 1–2 tsp** (honey, brown sugar, maple, mirin). Browning and balance. More than 2 tbsp per 2 lb will scorch over direct fire.
- **Aromatics — freely.** Garlic, ginger, shallot, chili, herbs, citrus zest, toasted spice.

**Salt rule that overrides everything:** if the marinade is properly salted, it *is* the brine. Don't salt again before cooking.

---

## Step 3 — Set the window

Commit to a specific range. Never say "or overnight" without a ceiling.

| Base | Minimum | Maximum | Failure mode past max |
|---|---|---|---|
| Citrus / vinegar / wine (hard acid) | 30 min | **2 hrs** (chicken breast, thin steak), 4 hrs (thighs) | Chalky, opaque, mealy surface — ceviche texture |
| Yogurt / buttermilk (soft acid + dairy) | 4 hrs | **24 hrs** | Very little; safest long-soak base |
| Soy / miso / fish sauce (salt-forward, low acid) | 1 hr | **24 hrs** | Oversalted, ham-like |
| Oil + aromatics, no acid | 1 hr | **48 hrs** | None to speak of |
| Pineapple, papaya, kiwi, fresh ginger (enzymatic) | 15 min | **30 min. Hard stop.** | Bromelain/papain turn the surface to mush and it does not come back |
| Dry brine, steak | 45 min (or under 3 min) | **48 hrs**, uncovered on a rack | Nothing — just drier surface, which is good |
| Dry brine, whole chicken | 12 hrs | **24 hrs**, uncovered | Skin over-dries past ~36 hrs |

**The 40-minute trap (dry brine, steak):** salt at 40 minutes out is the worst timing — surface is wet with drawn-out moisture that hasn't reabsorbed yet. Either salt and cook within 3 minutes, or salt at least 45 minutes ahead. Never in between.

---

## Step 4 — Safety and handling (non-negotiable)

- Marinate in the **refrigerator**, never on the counter. Zip bag or non-reactive container (glass, plastic, stainless — not aluminum or cast iron).
- **Used marinade is raw-meat liquid.** Discard it, or boil it a full minute before using as a sauce. Never brush raw marinade on meat in the last minutes of cooking.
- Reserve a portion **before** the meat goes in if a finishing sauce is wanted.
- **Pat the surface dry before it hits heat.** Every time. Wet meat steams instead of searing. This single step separates a good result from a gray one.
- Cook targets — pull temp, then rest:
  - Steak: 125°F rare / **130–135°F medium-rare** / 140°F medium. Rest 5–10 min.
  - Chicken breast: **150–155°F** and hold (pasteurizes at temp — juicier than 165°F, and safe).
  - Chicken thighs: **175–185°F.** Collagen needs the extra heat; thighs get better, not drier.
  - Whole bird: 157°F in the breast, 175°F in the thigh. Rest 20 min.

---

## Step 5 — Output template

Answer in this shape every time:

```
**[Marinade name] — [protein/cut], [weight]**

Window: [X–Y hours] · Refrigerated

Ingredients
- [exact amounts, scaled to the stated weight]

Method
1. [Whisk / blend]
2. [Combine with protein, bag, refrigerate]
3. [Pat dry, cook]

Cook
- [Heat, time per side or target temp, pull temp, rest]

Note
- [One line: the failure mode to avoid, or the finishing move]
```

Scale linearly by weight. If Tyler doesn't state a weight, assume **2 lb** and say so.

---

## House builds

Each scaled to **2 lb**. These are the defaults — reach for them unless he asks for something specific.

**Steak — Flank / Skirt / Hanger**

*Soy-Garlic-Balsamic* — 1/3 cup olive oil, 3 tbsp soy sauce, 2 tbsp balsamic, 1 tbsp Worcestershire, 4 cloves garlic minced, 1 tsp black pepper, 1 tsp brown sugar. **2–8 hrs.** No added salt. Sear hot and fast, 3–4 min/side, rest 8 min, slice thin **against the grain** — with a flank or skirt, slicing direction matters more than the marinade does.

*Chimichurri-style (double duty)* — 1 cup parsley, 1/4 cup oregano, 4 cloves garlic, 1/2 cup olive oil, 3 tbsp red wine vinegar, 1 tsp red pepper flake, 1.5 tsp kosher salt. Split it: half as marinade for **1–2 hrs**, half reserved raw and spooned over after resting.

**Steak — Thick Cuts (ribeye, strip, thick sirloin)**

*Dry brine* — 1.5 tsp Diamond Crystal kosher salt per lb, all surfaces. Uncovered on a rack in the fridge, **12–48 hrs**. Pepper goes on right before the sear, not during the brine. Finish with garlic-thyme butter basted in the last 90 seconds.

**Chicken — Thighs**

*Yogurt-Lemon-Cumin* — 1 cup whole-milk yogurt, zest + juice of 1 lemon, 4 cloves garlic, 1 tbsp cumin, 2 tsp paprika, 1.5 tsp kosher salt, 2 tbsp olive oil. **4–24 hrs.** Scrape off the excess — leave a thin coat, not a blanket — and grill or roast at 425°F to 175°F+.

*Soy-Ginger-Honey* — 1/4 cup soy sauce, 2 tbsp honey, 2 tbsp rice vinegar, 1 tbsp toasted sesame oil, 2 tbsp grated ginger, 4 cloves garlic. **2–12 hrs** (ginger is enzymatic but mild grated — 12 hrs is fine, 24 is not). Watch for scorch; the honey wants indirect heat to finish.

**Chicken — Breast**

*Buttermilk brine* — 2 cups buttermilk, 1 tbsp kosher salt, 1 tbsp honey, 2 tsp garlic powder, 1 tsp black pepper. **4–24 hrs.** The most reliable way to make a breast not dry. Pull at 150–155°F.

**Chicken — Wings**

*Dry brine* — 1 tbsp kosher salt + 2 tsp baking powder (not soda) per 2 lb, tossed to coat. Uncovered on a rack, **8–24 hrs**. Roast 425°F, 40–45 min, flipping once. Sauce **after** they come off the heat.

---

## Improvisation mode

If Tyler says "here's what I have" and lists ingredients, don't refuse for lack of a match. Map what he has onto the formula:

- Anything oily → fat. Anything sour → acid. Anything salty-savory (soy, miso, fish sauce, anchovy, parmesan rind, olive brine, pickle juice) → salt + umami. Anything sweet → browning.
- Missing acid entirely? Fine — go oil + aromatics + salt and extend the window to 24 hrs.
- Missing fat? Fine — the marinade just won't cling as well; add a slick of oil to the pan instead.
- Then still commit to a window and a cook target. **Never hand back a recipe without a number.**

---

## Rules

- Always state the marinating window as a range with a hard ceiling.
- Always state pull temp and rest time.
- Never recommend a wet marinade on a thick steak — say why, and offer the dry brine instead.
- Never let a fresh-pineapple/papaya/kiwi marinade exceed 30 minutes.
- Never suggest reusing marinade as sauce without boiling it.
- If salt is already in the marinade, don't season again before cooking — say so explicitly.
- Scale to stated weight; default to 2 lb and announce the assumption.
