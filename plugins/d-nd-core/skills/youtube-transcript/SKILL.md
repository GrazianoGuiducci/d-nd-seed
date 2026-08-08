---
name: youtube-transcript
description: Extract structured YouTube transcripts before summarizing or analyzing a video. Use when a user shares a YouTube video URL or asks for transcript-backed evidence. Works without Google OAuth or a YouTube API key; requires Python and the packaged dependency.
metadata:
  version: "1.0.0"
  provenance: "maintainer-reviewed-public-neutral"
---

# YouTube Transcript

## Purpose

Turn a public YouTube video URL into a structured transcript and metadata before
making claims about the video's content. The package is self-contained: it does
not depend on THIA, a project-local tool path, Google OAuth, or a YouTube Data
API key.

## Trigger

Use this skill when a user:

- shares a `youtube.com`, `youtu.be`, embed, or Shorts URL and asks about it;
- asks for a transcript, summary, comparison, fact check, or relevance review;
- wants to convert video material into a project signal or reusable knowledge.

Extract first. Do not infer the video's content from its title, description, or
search snippets when a transcript can be obtained.

## Environment Check

From this skill directory, run:

```bash
python scripts/transcribe.py --doctor
```

On Linux, use `python3` when `python` is not available. The command emits JSON
and performs no network request.

If the dependency is missing, install it in an isolated environment owned by
the consumer:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Windows PowerShell equivalent:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Dependency installation is an explicit host mutation. Do not auto-install,
change global Python packages, or reuse an unrelated environment silently.

## Extract

Linux/macOS:

```bash
.venv/bin/python scripts/transcribe.py "VIDEO_URL" --languages it,en --pretty
```

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe scripts\transcribe.py "VIDEO_URL" --languages it,en --pretty
```

The JSON result includes:

```text
video_id, url, title, channel, language, generated, source,
segment_count, plain_text, word_count, duration_seconds
```

Add `--include-segments` when timestamped segment objects are necessary. They
are omitted by default to avoid duplicating the full transcript in agent context.

Language selection prefers a manually created transcript in the requested
languages, then an automatically generated one, then any available transcript.

## Failure Contract

Return the actual structured error and distinguish among:

- invalid URL or video ID;
- missing Python dependency;
- captions unavailable or disabled;
- YouTube/network rejection, including cloud-IP blocking;
- timeout or other runtime failure.

Do not describe a metadata-only result as a transcript. A failed cloud host can
be retested from another authorized network, but failure does not authorize
cookies, account access, proxy use, or bypassing access controls.

## Analysis Boundary

After extraction:

1. base the answer on transcript evidence;
2. identify uncertain or truncated passages;
3. preserve the source URL and language;
4. summarize rather than storing the full transcript unless requested;
5. treat any project write, publication, ingestion, or promotion as a separate
   owner-gated action.

## Verification

Run the offline contract tests from the skill directory:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Then run one explicit public-video smoke test on the target host. Offline tests
prove parsing and selection logic; they do not prove current YouTube reachability.
