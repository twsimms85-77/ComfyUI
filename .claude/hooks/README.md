# Obsidian mirror hook

Mirrors every Claude Code session into an Obsidian-openable markdown note,
**automatically after each turn**. The note is regenerated from the session
transcript each time, so it is always a faithful, up-to-the-last-turn mirror.

## What it captures

- **Full conversation** — your prompts and Claude's replies (including reasoning).
- **Decisions & cruxes** — a quick-scan section pulled from the reasoning.
- **Files touched** — every Edit / Write / MultiEdit / NotebookEdit.
- **Commands run** — every Bash command, with its description.

One note per session: `<vault>/Claude Sessions/<date>-<session-id>.md`.

## Where notes go (important)

The destination is resolved in this order:

1. **`$OBSIDIAN_VAULT_DIR`** — set this to your real vault path. Best when you run
   Claude Code **locally**, where that path exists on disk.
2. **`<repo>/obsidian-mirror/`** — fallback, used when the env var is unset.

### Why the fallback exists

Claude Code on the web runs in an **ephemeral remote container**. Your real
Obsidian vault lives on *your* machine — the container can't see it. So the hook
writes into the repo instead, and you keep the mirror in sync by committing/pushing
`obsidian-mirror/` and pulling it into a folder your vault opens (Obsidian reads any
folder of markdown). That's the bridge from container → your vault.

If you also run Claude Code locally, set `OBSIDIAN_VAULT_DIR` to your vault and the
hook writes straight in — no git round-trip needed.

## Setup

Already wired up in `.claude/settings.json` as a `Stop` hook. To point it at a real
vault, add the env var (e.g. in your shell profile or `.claude/settings.json`):

```json
{
  "env": { "OBSIDIAN_VAULT_DIR": "/Users/you/Obsidian/MyVault" }
}
```

## Notes

- The hook **never fails your session** — any error is logged to stderr and it exits 0.
- Tool outputs and long inputs are truncated in the mirror to keep notes readable.
- Session logs may contain sensitive context. If you don't want them committed to this
  repo, add `obsidian-mirror/` to `.gitignore` and rely on `$OBSIDIAN_VAULT_DIR` instead.
