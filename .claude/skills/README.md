# Tyler's Skill Library

Single source of truth for every custom Claude skill. One folder per skill, one `SKILL.md` per folder, folder name equals the `name:` field.

Anything Claude Code runs inside this repo loads every skill here automatically. Nothing needs to be copied for that.

## Getting the library onto a machine

Run once per machine, from a PowerShell prompt:

```powershell
git clone https://github.com/twsimms85-77/ComfyUI.git "$HOME\skill-library"
cd "$HOME\skill-library"
git checkout claude/1031-build-to-suit-skill-4b05s1
powershell -ExecutionPolicy Bypass -File .claude\skills\install.ps1
```

`install.ps1` links this folder into the two places that matter:

- the Vault at `08 Skills` (Obsidian sees every skill as notes)
- the local Claude skills directory under `AppData\Roaming\Claude` (Claude desktop loads them)

Links, not copies. Edit or pull once and every location updates.

## Day to day

- **New skill:** ask Claude in this repo to build it. It lands here, gets committed, gets pushed.
- **Other machines:** `git pull` in `$HOME\skill-library`. Done.
- **claude.ai web:** skills there still come from your profile. Upload the `.skill` file Claude hands you, or drag the folder in under Settings, Capabilities, Skills. That is the one place git cannot reach.

## Rules

- Never delete a folder here without meaning to retire the skill.
- Keep frontmatter valid YAML. Quote the description if it contains colons.
- Anthropic-shipped skills (docx, pdf, xlsx, pptx, skill-creator, morning, import-memory) are not stored here. They come with Claude.
