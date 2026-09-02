---
name: you-tube-researcher
description: "generate useful things from you tube search"
---

# YouTube Research To Obsidian Skill

## Purpose

Turn public YouTube videos on any subject into structured Obsidian markdown notes.

This is useful for research rabbit holes where Tyler wants the lessons, frameworks, claims, and follow-up questions without manually watching and summarizing every video.

## Local Script

```text
C:\Scripts\youtube_research_agent.py
```

## Default Output

```text
C:\Dellcockpit home\Tyler's Vault\09 - Reference\YouTube Research\<Subject>\
```

For trading topics, use a trading folder when useful:

```text
C:\Dellcockpit home\Tyler's Vault\02 - Trading\<Subject>\
```

## Basic Commands

Preview videos without writing notes:

```powershell
python C:\Scripts\youtube_research_agent.py --subject "Wyckoff distribution" --dry-run --max-videos 3
```

Create notes from search results:

```powershell
python C:\Scripts\youtube_research_agent.py --subject "Wyckoff distribution" --max-videos 3
```

Create a note from a specific video:

```powershell
python C:\Scripts\youtube_research_agent.py --subject "Mark Minervini" --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

Send trading research to a trading folder:

```powershell
python C:\Scripts\youtube_research_agent.py --subject "Wyckoff distribution" --output-folder "02 - Trading\Wyckoff\YouTube Research" --max-videos 3
```

## What It Creates

Each subject gets:

```text
Video Notes\
<Subject> Index.md
processed_videos.json
```

Each video note includes:

- Source
- One-sentence takeaway
- Core ideas
- Key claims or lessons
- Practical rules or frameworks
- Examples mentioned
- Tensions or caveats
- Quotes or near-quotes
- Tyler follow-up questions
- Tags

## Rules

- Public YouTube videos only.
- Uses captions/transcripts when available.
- Does not save full transcripts.
- Saves short quotes only when useful.
- Keeps source URLs so the original can be reviewed.
- Tracks processed videos so the same video is not processed repeatedly.

## Related Files

Claude skill package:

```text
C:\Users\twsim\Documents\Codex\2026-05-29\python-py-import-zipfile-os-src\Claude Skill\youtube-research-to-obsidian.skill
```

Custom GPT instructions:

```text
C:\Users\twsim\Documents\Codex\2026-05-29\python-py-import-zipfile-os-src\YouTube Research Agent\CUSTOM_GPT_INSTRUCTIONS.md
```
