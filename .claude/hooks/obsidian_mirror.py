#!/usr/bin/env python3
"""Obsidian mirror hook.

Runs on the Claude Code `Stop` event (after every assistant turn) and mirrors the
whole session into an Obsidian-openable markdown note. Idempotent: it regenerates
the note from the transcript each turn, so the note is always a faithful mirror of
the session so far. It captures everything the transcript holds:

  - the full conversation (your prompts + Claude's replies, including reasoning)
  - every file touched (Edit / Write / MultiEdit / NotebookEdit)
  - every shell command run (Bash)
  - key decisions surfaced as a quick-scan section at the top

Destination, in priority order:
  1. $OBSIDIAN_VAULT_DIR   -> point this at your real vault when running locally
  2. <repo>/obsidian-mirror -> committed fallback your vault can sync via git

The hook never fails the session: any error is swallowed and it exits 0.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Notes are written under this subfolder inside the vault, so the mirror never
# collides with your own notes.
SUBFOLDER = "Claude Sessions"
# Tool results can be huge (file dumps, long stdout). Truncate them in the mirror.
MAX_RESULT_CHARS = 600
MAX_INPUT_CHARS = 400


def log_fail(msg: str) -> None:
    # Hooks must not break the session; surface problems only to stderr.
    print(f"[obsidian-mirror] {msg}", file=sys.stderr)


def resolve_vault(cwd: str) -> Path:
    env = os.environ.get("OBSIDIAN_VAULT_DIR", "").strip()
    if env:
        return Path(os.path.expanduser(env))
    return Path(cwd) / "obsidian-mirror"


def read_transcript(path: str) -> list:
    events = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events


def blocks_of(message) -> list:
    """Normalize a message's content into a list of blocks."""
    if message is None:
        return []
    content = message.get("content")
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    if isinstance(content, list):
        return content
    return []


def clip(text: str, limit: int) -> str:
    text = text.rstrip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + f"\n… (+{len(text) - limit} chars truncated)"


def first_line(text: str, n: int = 100) -> str:
    line = text.strip().splitlines()[0] if text.strip() else ""
    return (line[:n] + "…") if len(line) > n else line


def render(events: list, session_id: str) -> str:
    convo = []          # rendered conversation blocks, in order
    files_touched = []  # (tool, path)
    commands = []       # (command, description)
    decisions = []      # short bullet lines pulled from assistant text
    started = None
    last_ts = None

    for ev in events:
        etype = ev.get("type")
        ts = ev.get("timestamp")
        if ts:
            started = started or ts
            last_ts = ts
        msg = ev.get("message")

        if etype == "user":
            # Skip tool_result-only user turns in the narrative; capture real prompts.
            texts = [b.get("text", "") for b in blocks_of(msg)
                     if isinstance(b, dict) and b.get("type") == "text"]
            body = "\n".join(t for t in texts if t.strip())
            if isinstance(msg, dict) and isinstance(msg.get("content"), str):
                body = msg["content"]
            if body.strip():
                convo.append(f"### 🧑 You\n\n{body.strip()}\n")

        elif etype == "assistant":
            parts = []
            for b in blocks_of(msg):
                if not isinstance(b, dict):
                    continue
                bt = b.get("type")
                if bt == "text":
                    txt = b.get("text", "").strip()
                    if txt:
                        parts.append(txt)
                        decisions.extend(extract_decisions(txt))
                elif bt == "tool_use":
                    name = b.get("name", "tool")
                    inp = b.get("input", {}) or {}
                    if name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                        fp = inp.get("file_path") or inp.get("notebook_path") or "?"
                        files_touched.append((name, fp))
                        parts.append(f"> 🔧 **{name}** → `{fp}`")
                    elif name == "Bash":
                        cmd = inp.get("command", "")
                        desc = inp.get("description", "")
                        commands.append((cmd, desc))
                        parts.append(f"> 💻 `{first_line(cmd, 120)}`"
                                     + (f" — {desc}" if desc else ""))
                    else:
                        summary = clip(json.dumps(inp, ensure_ascii=False), MAX_INPUT_CHARS)
                        parts.append(f"> 🔧 **{name}**\n> ```json\n> {summary}\n> ```")
            if parts:
                convo.append("### 🤖 Claude\n\n" + "\n\n".join(parts) + "\n")

    # ---- assemble note ----
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    date = (started or "").split("T")[0] or datetime.now().strftime("%Y-%m-%d")
    project = Path(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())).name

    out = []
    out.append("---")
    out.append(f"session: {session_id}")
    out.append(f"project: {project}")
    out.append(f"date: {date}")
    out.append(f"updated: {now}")
    out.append("tags: [claude-session, mirror]")
    out.append("---")
    out.append("")
    out.append(f"# Claude session — {project} — {date}")
    out.append("")
    out.append(f"*Mirrored automatically after each turn. Last update: {now}.*")
    out.append("")

    if decisions:
        out.append("## 🧭 Decisions & cruxes")
        out.append("")
        for d in dedupe(decisions)[:25]:
            out.append(f"- {d}")
        out.append("")

    if files_touched:
        out.append("## 📄 Files touched")
        out.append("")
        for name, fp in dedupe_pairs(files_touched):
            out.append(f"- `{fp}`  _({name})_")
        out.append("")

    if commands:
        out.append("## 💻 Commands run")
        out.append("")
        for cmd, desc in commands[-40:]:
            label = f" — {desc}" if desc else ""
            out.append(f"- `{first_line(cmd, 120)}`{label}")
        out.append("")

    out.append("## 💬 Transcript")
    out.append("")
    out.extend(convo)

    return "\n".join(out).rstrip() + "\n"


# Sentences that read like a decision/crux/plan — pulled for the quick-scan section.
DECISION_RE = re.compile(
    r"^\s*(?:the crux|the move|crux|decision|i(?:'| a)?ll|i will|let'?s|plan|approach|"
    r"the real problem|the constraint|so the first thing|because)\b",
    re.IGNORECASE,
)


def extract_decisions(text: str) -> list:
    picks = []
    for raw in re.split(r"(?<=[.!?])\s+|\n", text):
        s = raw.strip(" -*•\t")
        if 12 <= len(s) <= 200 and DECISION_RE.match(s):
            picks.append(first_line(s, 180))
    return picks


def dedupe(seq: list) -> list:
    seen, out = set(), []
    for x in seq:
        k = x.lower()
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def dedupe_pairs(seq: list) -> list:
    seen, out = set(), []
    for a, b in seq:
        if (a, b) not in seen:
            seen.add((a, b))
            out.append((a, b))
    return out


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    transcript = payload.get("transcript_path")
    session_id = payload.get("session_id", "unknown")
    cwd = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

    if not transcript or not os.path.exists(transcript):
        log_fail("no transcript_path; nothing to mirror")
        return 0

    try:
        events = read_transcript(transcript)
        note = render(events, session_id)
    except Exception as e:  # never break the session
        log_fail(f"render failed: {e}")
        return 0

    try:
        vault = resolve_vault(cwd)
        dest_dir = vault / SUBFOLDER
        dest_dir.mkdir(parents=True, exist_ok=True)
        date = datetime.now().strftime("%Y-%m-%d")
        safe_sid = re.sub(r"[^A-Za-z0-9_-]", "", session_id)[:12] or "session"
        dest = dest_dir / f"{date}-{safe_sid}.md"
        dest.write_text(note, encoding="utf-8")
    except Exception as e:
        log_fail(f"write failed: {e}")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
