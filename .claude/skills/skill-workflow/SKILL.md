---
name: skill-workflow
description: "Skills workflow instructions"
---

ame: skill-builder-workflow
description: Walk Tyler through building a new Claude skill and saving it to Obsidian. Use this skill whenever Tyler says "build me a skill", "turn this into a skill", "make a skill for", "new skill", "help me create a skill", or asks how to capture a workflow as a skill. Also trigger when he says "I keep re-explaining this to Claude" or "I want Claude to remember how to do X." This skill handles the full loop from identifying the skill through drafting, packaging, uploading to Claude.ai, and copying into the Obsidian Vault.
---

# Skill Builder Workflow

> **Current process:** skills live in the git-backed library at `.claude/skills/` in the ComfyUI repo and are linked into the vault by `install.ps1`. Use the `skill-builder` skill, which commits and pushes. The upload steps below only apply to claude.ai web, where a skill still has to be saved into the profile.

Tyler is a solo CPA building Claude skills to capture repeated workflows. He is not a developer — walk him through every step plainly. He uses Claude.ai (not Claude Code), Obsidian with Sync across four machines, and stores skills at `08 Skills/` inside Tyler's Vault.

## Step 1: Identify the Skill

Ask: "What's the thing you keep re-explaining to Claude?" The signal is repetition — if he's described the same workflow, research framework, or set of instructions more than twice, that's a skill.

Clarify three things before drafting:
- What should Claude do when this skill fires?
- What phrases would Tyler naturally type that should trigger it?
- What should the output look like?

## Step 2: Draft the SKILL.md

Build the file with two parts:

### Part 1: YAML Frontmatter
```
---
name: skill-name-here
description: What this skill does and when to trigger it.
  Include the actual phrases Tyler would type. Be pushy —
  Claude undertriggers, so cast a wide net. 200 chars max.
---
```

### Part 2: Markdown Instructions
Write everything below the frontmatter as a briefing to a competent associate:
- Who Tyler is and what context matters
- What sections to cover, in what order
- What format the output should take
- What to watch out for (edge cases, gotchas)
- Keep the whole file under 500 lines

### Key principles for the description field:
- Include the literal phrases Tyler would type ("got a client in [state]", "what do I need to know about")
- Include related keywords Claude might match on
- Be slightly pushy — "Always use this skill when..." / "Also trigger when..."
- 200 character limit for Claude.ai

## Step 3: Package and Deliver

Generate the SKILL.md file and package it as a ZIP:
```
skill-name/
  SKILL.md
```
The ZIP should contain the skill folder at its root, not nested inside another folder.

Present the ZIP for download.

## Step 4: Walk Through Upload to Claude.ai

Give these steps ONE AT A TIME, waiting for confirmation after each:
1. Download the ZIP file
2. In Claude.ai, click profile (bottom-left) → Settings
3. Go to Customize → Skills
4. Click the "+" button → Create skill
5. Upload the ZIP
6. Toggle the skill ON

## Step 5: Walk Through Vault Copy

Give these steps ONE AT A TIME:
1. Find the downloaded ZIP on the computer and unzip it
2. Open Windows Explorer to the Vault path (check Obsidian bottom-left for path)
3. Navigate to the `08 Skills` folder
4. Copy the skill folder (containing SKILL.md) into `08 Skills`
5. Confirm it appears in Obsidian's sidebar
6. Sync will carry it to the other machines

## Step 6: Test

Remind Tyler to open a NEW chat (skills load at conversation start). Suggest a natural test prompt that should trigger the skill. If it doesn't fire, adjust the description keywords, re-zip, and re-upload.

## Rules
- One step at a time. Do not stack steps.
- Be direct. No throat-clearing.
- If Tyler says "next step," give exactly one step.
- Do not suggest automating this process. It is a manual capture habit, not a build.
