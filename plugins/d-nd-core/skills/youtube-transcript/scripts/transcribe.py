#!/usr/bin/env python3
"""Public-neutral YouTube transcript extractor with a stable JSON contract."""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import re
import sys
import urllib.parse
import urllib.request
from typing import Any, Iterable

SCHEMA = "dnd.seed.youtube_transcript.v1"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(value: str) -> str | None:
    value = value.strip()
    if VIDEO_ID_RE.fullmatch(value):
        return value
    try:
        parsed = urllib.parse.urlparse(value)
    except ValueError:
        return None
    host = parsed.netloc.lower().split(":", 1)[0]
    if host in {"youtu.be", "www.youtu.be"}:
        candidate = parsed.path.strip("/").split("/", 1)[0]
    elif host in {"youtube.com", "www.youtube.com", "m.youtube.com", "music.youtube.com"}:
        if parsed.path == "/watch":
            candidate = urllib.parse.parse_qs(parsed.query).get("v", [""])[0]
        else:
            parts = [part for part in parsed.path.split("/") if part]
            candidate = parts[1] if len(parts) >= 2 and parts[0] in {"embed", "shorts", "live"} else ""
    else:
        candidate = ""
    return candidate if VIDEO_ID_RE.fullmatch(candidate) else None


def dependency_version() -> str | None:
    try:
        return importlib.metadata.version("youtube-transcript-api")
    except importlib.metadata.PackageNotFoundError:
        return None


def _metadata(video_id: str) -> dict[str, str | None]:
    url = "https://www.youtube.com/oembed?" + urllib.parse.urlencode(
        {"url": f"https://www.youtube.com/watch?v={video_id}", "format": "json"}
    )
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "DND-Seed-Transcript/1.0"})
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return {"title": payload.get("title"), "channel": payload.get("author_name")}
    except Exception:
        return {"title": None, "channel": None}


def select_transcript(transcripts: Iterable[Any], languages: list[str]) -> Any | None:
    available = list(transcripts)
    for generated in (False, True):
        for language in languages:
            for transcript in available:
                if bool(transcript.is_generated) == generated and transcript.language_code == language:
                    return transcript
    return available[0] if available else None


def _segment_dict(segment: Any) -> dict[str, Any]:
    if isinstance(segment, dict):
        start = segment.get("start", 0)
        duration = segment.get("duration", 0)
        text = segment.get("text", "")
    else:
        start = getattr(segment, "start", 0)
        duration = getattr(segment, "duration", 0)
        text = getattr(segment, "text", "")
    return {"start": float(start), "duration": float(duration), "text": str(text)}


def extract(url_or_id: str, languages: list[str]) -> dict[str, Any]:
    video_id = extract_video_id(url_or_id)
    if not video_id:
        raise ValueError("invalid YouTube URL or video ID")

    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError as error:
        raise RuntimeError("missing dependency: install requirements.txt in an isolated environment") from error

    api = YouTubeTranscriptApi()
    chosen = select_transcript(api.list(video_id), languages)
    if chosen is None:
        raise RuntimeError("no transcript is available for this video")

    segments = [_segment_dict(segment) for segment in chosen.fetch()]
    plain_text = " ".join(segment["text"] for segment in segments).strip()
    end = max((segment["start"] + segment["duration"] for segment in segments), default=0)
    metadata = _metadata(video_id)
    return {
        "schema": SCHEMA,
        "ok": True,
        "video_id": video_id,
        "url": f"https://www.youtube.com/watch?v={video_id}",
        "title": metadata["title"],
        "channel": metadata["channel"],
        "language": chosen.language_code,
        "generated": bool(chosen.is_generated),
        "source": "youtube-transcript-api",
        "segments": segments,
        "plain_text": plain_text,
        "word_count": len(plain_text.split()),
        "duration_seconds": round(end, 3),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", nargs="?", help="YouTube URL or 11-character video ID")
    parser.add_argument("--languages", default="it,en", help="comma-separated preference order")
    parser.add_argument("--doctor", action="store_true", help="check runtime and dependency without network")
    parser.add_argument("--include-segments", action="store_true", help="include timestamped segments in JSON")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON")
    args = parser.parse_args()

    if args.doctor:
        version = dependency_version()
        payload = {
            "schema": SCHEMA,
            "ok": version is not None,
            "python": sys.version.split()[0],
            "dependency": "youtube-transcript-api",
            "dependency_version": version,
            "network_checked": False,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
        return 0 if version else 2

    if not args.video:
        parser.error("video URL or ID is required unless --doctor is used")

    try:
        languages = [item.strip() for item in args.languages.split(",") if item.strip()]
        payload = extract(args.video, languages or ["it", "en"])
        payload["segment_count"] = len(payload["segments"])
        if not args.include_segments:
            del payload["segments"]
        code = 0
    except Exception as error:
        payload = {
            "schema": SCHEMA,
            "ok": False,
            "input": args.video,
            "error_type": type(error).__name__,
            "error": str(error),
        }
        code = 1
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
