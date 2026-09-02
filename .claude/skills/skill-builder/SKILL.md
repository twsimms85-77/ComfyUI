---
name: skill-builder
description: Use this skill whenever Tyler wants to create a NEW skill from a plain-English description. Triggers on phrases like "build me a skill that...", "make a skill for...", "create a new skill", "I want a skill that does X", or "turn this into a skill". Gathers the skill's purpose, writes a properly formatted SKILL.md, and saves it as a new folder in the git-backed skill library (.claude/skills in the ComfyUI repo), which is linked into the Obsidian vault's "08 Skills" directory on every machine.
---

# Skill Builder

Turn a plain-English request from Tyler into a new, properly formatted skill folder in his skill library.

**Library (source of truth):** `.claude/skills/` in the ComfyUI repo, branch `claude/1031-build-to-suit-skill-4b05s1`. On Tyler's machines this folder is junction-linked into `C:\Dellcockpit home\Tyler's Vault\08 Skills` and into the local Claude skills directory by `install.ps1`, so writing here is writing everywhere.

Each skill is its own folder containing a single `SKILL.md` file. The folder name and the `name:` field must match (kebab-case).

---

## Process

### 1. Understand what Tyler wants
From his request, extract:
- **What the skill does** — the core capability or output it produces.
- **When it should trigger** — the situations, phrasings, or file types that should activate it.
- **The output format** — structured template, tone, length, required sections.

If any of these three is unclear or missing, ask ONE concise round of clarifying questions before building. Don't over-interrogate — infer sensible defaults where you can and confirm only what matters.

### 2. Choose a name
- kebab-case, lowercase, hyphen-separated (e.g., `email-drafter`, `trade-journal-logger`).
- Short and descriptive. This is both the folder name and the `name:` frontmatter field.
- Check the library first — if a folder with that name already exists, either update it (if Tyler wants a revision) or pick a distinct name. Never silently overwrite.

### 3. Write a strong description
The `description:` field is what decides whether the skill triggers later, so make it specific and trigger-rich:
- Start with "Use this skill when/whenever..."
- List concrete trigger phrases and situations.
- Name the output it produces.
- If it should fire for Tyler's conversational phrasings, say so explicitly.

### 4. Write the SKILL.md
Use this structure:

```markdown
---
name: <kebab-case-name>
description: <trigger-rich description, see step 3>
---

# <Human Readable Skill Title>

<One or two sentences on what this skill does and the standard it upholds.>

---

## <Sections as needed>

<Instructions, output template, examples, rules, edge cases — whatever the skill needs to perform reliably. Match the depth of the existing skills in this vault.>
```

Keep instructions concrete and example-driven. Look at neighboring skills (e.g. `iaacc-tax-research`, `app-architect`) as a style reference for depth and formatting.

### 5. Create the folder, commit, push
Write `.claude/skills/<name>/SKILL.md` in the repo. Then:

```
git add .claude/skills/<name>
git commit -m "Add <name> skill"
git push -u origin claude/1031-build-to-suit-skill-4b05s1
```

Because the library is linked into the vault and the local Claude skills directory, nothing else needs copying. Tyler runs `git pull` in `$HOME\skill-library` on any other machine.

If a file-delivery tool is available (`SendUserFile`), also package the skill with `python -m scripts.package_skill <folder>` from the skill-creator skill and send the `.skill` file. Its card carries a **Save skill** button that installs it into Tyler's claude.ai profile, the one place git does not reach.

Then confirm to Tyler with the path, a one-line summary, and the trigger phrases. New skills load on the next Claude session.

---

## Rules
- One skill = one folder = one `SKILL.md`. Folder name matches `name:`.
- Never overwrite an existing skill without confirming.
- Keep frontmatter valid YAML — no stray colons or unescaped special characters in the description (wrap in quotes if needed).
- After creating, tell Tyler the path and the trigger phrases so he knows how to invoke it.
- A new skill pushed to the library is available to Claude on the next session load — mention this if relevant.
