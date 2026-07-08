"""Render vocabulary WAV files for all buổi using Kokoro TTS.

Reads word list from js/pronunciation-data.js by parsing the PRON_LESSONS
literal. For each word, POSTs to Kokoro (127.0.0.1:8000) and saves the WAV to
audio/vocab/buoi-N/<word>.wav. Writes a manifest at audio/vocab/manifest.json
mapping "buoi-N" -> { word: relative_url }.

Idempotent: existing WAVs are kept unless --force is passed.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError

SITE_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = SITE_ROOT / "js" / "pronunciation-data.js"
OUT_DIR = SITE_ROOT / "audio" / "vocab"
MANIFEST_PATH = OUT_DIR / "manifest.json"
API_URL = "http://127.0.0.1:8000/api/v1/tts/render"


def parse_pron_lessons() -> dict[str, list[str]]:
    """Extract { lesson_key: [word, ...] } from js/pronunciation-data.js."""
    text = DATA_FILE.read_text(encoding="utf-8")

    lessons: dict[str, list[str]] = {}
    # Find each lesson block: "N": {   ... words: [ ... ]   },
    for key_match in re.finditer(r'"(\d+)"\s*:\s*\{', text):
        key = key_match.group(1)
        # Locate the words: [...] array for this lesson
        cursor = key_match.end()
        arr_match = re.search(r"words\s*:\s*\[(.*?)\]", text[cursor:], flags=re.S)
        if not arr_match:
            continue
        block = arr_match.group(1)
        words = [w.strip() for w in re.findall(r'word:\s*"([^"]+)"', block)]
        # Preserve declaration order, dedupe within a lesson
        seen: set[str] = set()
        ordered: list[str] = []
        for w in words:
            if w not in seen:
                seen.add(w)
                ordered.append(w)
        if ordered:
            lessons[key] = ordered
    return lessons


def render_word(word: str, dest: Path, retries: int = 3, timeout: int = 60) -> None:
    """Call Kokoro and save WAV bytes to dest. Retries on transient errors."""
    payload = json.dumps({"text": word, "mode": "lesson"}).encode("utf-8")
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urlrequest.Request(
                API_URL,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlrequest.urlopen(req, timeout=timeout) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"unexpected status {resp.status}")
                data = resp.read()
            if not data or len(data) < 100:
                raise RuntimeError(f"suspicious response size {len(data)} bytes")
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return
        except (URLError, HTTPError, RuntimeError, TimeoutError) as exc:
            last_err = exc
            wait = 1.5 * attempt
            print(f"    ! attempt {attempt}/{retries} failed: {exc}; retrying in {wait:.1f}s", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed after {retries} retries: {last_err}")


def build_manifest(lessons: dict[str, list[str]]) -> dict[str, dict[str, str]]:
    manifest: dict[str, dict[str, str]] = {}
    for key, words in lessons.items():
        lesson_id = f"buoi-{key}"
        lesson_map: dict[str, str] = {}
        for word in words:
            wav = OUT_DIR / lesson_id / f"{word}.wav"
            if wav.exists() and wav.stat().st_size > 0:
                lesson_map[word] = f"audio/vocab/{lesson_id}/{word}.wav"
        if lesson_map:
            manifest[lesson_id] = lesson_map
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true", help="re-render even if wav exists")
    ap.add_argument("--only", nargs="*", help="restrict to these lesson keys, e.g. 1 2 13")
    args = ap.parse_args()

    lessons = parse_pron_lessons()
    if args.only:
        keys = set(args.only)
        lessons = {k: v for k, v in lessons.items() if k in keys}
    if not lessons:
        print("No lessons parsed from pronunciation-data.js")
        return 1

    total_words = sum(len(v) for v in lessons.values())
    print(f"Rendering {total_words} words across {len(lessons)} lesson(s)")

    ok = 0
    skipped = 0
    failed: list[tuple[str, str, str]] = []

    for key, words in sorted(lessons.items(), key=lambda kv: int(kv[0])):
        lesson_id = f"buoi-{key}"
        print(f"\n== {lesson_id} ({len(words)} words) ==")
        for word in words:
            dest = OUT_DIR / lesson_id / f"{word}.wav"
            if dest.exists() and not args.force:
                print(f"  skip {word} (already rendered)")
                skipped += 1
                continue
            print(f"  render {word} ... ", end="", flush=True)
            try:
                render_word(word, dest)
                size = dest.stat().st_size
                print(f"ok ({size} bytes)")
                ok += 1
            except Exception as exc:
                print(f"FAIL: {exc}")
                failed.append((lesson_id, word, str(exc)))

    manifest = build_manifest(lessons if not args.only else parse_pron_lessons())
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    covered = sum(len(v) for v in manifest.values())
    print(
        f"\nDone. rendered={ok} skipped={skipped} failed={len(failed)} manifest_entries={covered}"
    )
    if failed:
        print("Failures:")
        for lid, w, err in failed:
            print(f"  {lid}/{w}: {err}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
