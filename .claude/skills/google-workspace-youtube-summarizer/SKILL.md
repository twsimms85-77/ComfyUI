---
name: google-workspace-youtube-summarizer
description: "Use this skill whenever Tyler wants a YouTube video or YouTube search topic summarized and saved to Google Workspace (Google Drive / Google Docs). Triggers on requests like 'summarize this YouTube video to Drive', 'YouTube summary to Google Docs', 'put a summary of this video in my Drive', 'research <topic> on YouTube and save it to Google', or any message containing a youtube.com / youtu.be URL together with a mention of Drive, Docs, or Google Workspace. Fetches the video's page and transcript, produces a structured research note, and creates the note as a file in Google Drive."
---

# Google Workspace YouTube Summarizer

Turn public YouTube videos into structured research notes saved directly to Tyler's Google Drive. This is the cloud-native sibling of the `you-tube-researcher` skill (which writes to the Obsidian vault via a local script) — same note quality, but the output lands in Google Workspace so it's readable from any device and shareable.

No local script is required. Everything runs with tools available in the Claude session:

- **WebSearch / WebFetch** — find videos and pull page content, descriptions, and transcripts.
- **mcp__Google_Drive__search_files** — check for an existing "YouTube Summaries" folder and avoid duplicate notes.
- **mcp__Google_Drive__create_file** — write the finished note to Drive.
- **mcp__Google_Drive__read_file_content** — read an existing index or note before updating it.

---

## Inputs

Accept any of:

1. **A specific video** — a `youtube.com/watch?v=...` or `youtu.be/...` URL.
2. **A search subject** — e.g. "Wyckoff distribution", "S-corp reasonable comp". Default to the top 3 relevant videos unless Tyler gives a count.
3. **A channel + topic** — e.g. "latest Minervini interview".

If Tyler gives only a URL with no other instruction, assume he wants one summary note saved to Drive.

## Process

### 1. Gather the video(s)
- For a URL: WebFetch the video page. Capture title, channel, date, duration, and description.
- For a subject: WebSearch `site:youtube.com <subject>`, pick the most substantive results (favor long-form talks, interviews, and lectures over shorts and clickbait), and confirm the list with Tyler only if the subject is ambiguous.
- Try to obtain the transcript: WebFetch the watch page (transcript text is often in the initial payload), or search for a transcript of the video. If no transcript is reachable, summarize from the description, comments, and any coverage of the talk found via WebSearch — and say clearly in the note that it was built without the full transcript.

### 2. Summarize
Use the same note skeleton as the Obsidian YouTube researcher so notes are consistent across both systems:

- **Source** — title, channel, URL, date, duration
- **One-sentence takeaway**
- **Core ideas** (3–7 bullets)
- **Key claims or lessons**
- **Practical rules or frameworks** — anything actionable, stated as rules
- **Examples mentioned**
- **Tensions or caveats** — where the speaker hedges, contradicts, or oversimplifies
- **Quotes or near-quotes** — timestamped when the transcript allows
- **Tyler follow-up questions** — 3–5 questions worth digging into next
- **Tags**

Write for a smart reader who has not watched the video. Concrete numbers, names, and rules beat vibes.

### 3. Save to Google Drive
- Folder convention: a **"YouTube Summaries"** folder in Drive, with one subfolder per subject (`YouTube Summaries/<Subject>`). Use `mcp__Google_Drive__search_files` to find the folder; create the file into it if it exists, otherwise create the file with the folder path requested and tell Tyler where it landed.
- File name: `<Video Title> — <Channel> (YYYY-MM-DD).md` (or as a Google Doc if the create tool supports it — prefer Google Doc format so it opens natively in Workspace).
- One file per video. For multi-video subject runs, also create or update a `<Subject> Index` file listing each note with its one-sentence takeaway and link.
- Before writing, search Drive for an existing note for the same video URL — if found, update/extend rather than duplicating.

### 4. Report back
End with a short recap in chat: each video's one-sentence takeaway plus a link (or name/location) of every Drive file created. Do not paste the full notes into chat unless asked.

## Guardrails

- Public videos only; never attempt to bypass login walls or age gates.
- If the Google Drive tools are not connected in the session, say so and offer the fallback: produce the notes in chat or as local markdown files instead. Do not silently drop the Drive step.
- Quote sparingly — near-quotes and paraphrase over long verbatim transcript dumps.
- If a video turns out to be thin content (a short, a teaser, pure promo), say so and skip it rather than padding a note.
