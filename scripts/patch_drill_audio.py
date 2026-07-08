"""Patch buoi-4..20.html drill pages to route audio through HumanAudio.

Changes per file:
  1. Insert <script src="../js/human-audio.js"></script> before kokoro-audio.js
     (if not already present).
  2. Replace the DrillEngine.speak() body with a Promise-returning version
     that prefers vocab WAV via window.HumanAudio.play().
  3. Replace DrillEngine.stopPlayback() so it also cancels HumanAudio.
  4. Replace DrillEngine.playRepeated() so it awaits the Promise returned
     by speak() (needed because HumanAudio uses <audio> not speechSynthesis;
     the old wait-loop only watches synth.speaking).
  5. Replace DrillEngine.waitForPlaybackToFinish() with a no-op that
     returns immediately — playRepeated no longer calls it, but keep it
     defined in case other code paths do.

The patch is idempotent: re-running it will skip files already patched
(detected by the presence of the sentinel "HumanAudio.play" inside speak()).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = SITE_ROOT / "lessons"


NEW_SPEAK_TPL = """  speak(text, {{ cancelFirst = true }} = {{}}) {{
    if (cancelFirst) this.stopPlayback();
    const lessonId = '{lesson_id}';
    return new Promise((resolve) => {{
      let done = false;
      const finish = () => {{ if (!done) {{ done = true; resolve(); }} }};
      const safety = setTimeout(finish, 6000);
      const wrapEnd = () => {{ clearTimeout(safety); finish(); }};
      if (this.phase === 0 && window.HumanAudio) {{
        window.HumanAudio.play({{
          lessonId,
          key: text,
          text,
          rate: this.rate,
          voice: this.voice,
          onend: wrapEnd,
        }});
        return;
      }}
      const u = new SpeechSynthesisUtterance(text);
      u.voice = this.voice;
      u.rate = this.rate;
      u.onend = wrapEnd;
      u.onerror = wrapEnd;
      this.synth.speak(u);
    }});
  }}"""


NEW_STOP = """  stopPlayback() {
    this._playToken += 1;
    this.synth.cancel();
    if (window.HumanAudio && window.HumanAudio.cancel) window.HumanAudio.cancel();
  }"""


NEW_PLAY_REPEATED = """  async playRepeated(text, times = 3) {
    const token = ++this._playToken;
    for (let i = 0; i < times; i++) {
      if (token !== this._playToken) return;
      await this.speak(text, { cancelFirst: i === 0 });
      if (token !== this._playToken) return;
      if (i < times - 1) await this.delay(250);
    }
  }"""


NEW_WAIT = """  async waitForPlaybackToFinish(token) {
    if (token !== this._playToken) return;
  }"""


def patch_file(path: Path) -> str:
    """Return 'patched', 'skipped', or 'no-match'."""
    text = path.read_text(encoding="utf-8")

    match = re.search(r"buoi-(\d+)\.html$", path.name)
    if not match:
        return "no-match"
    lesson_id = f"buoi-{match.group(1)}"

    original = text

    # 1. Add human-audio.js include before kokoro-audio.js
    if '<script src="../js/human-audio.js"></script>' not in text:
        text = text.replace(
            '<script src="../js/kokoro-audio.js"></script>',
            '<script src="../js/human-audio.js"></script>\n  <script src="../js/kokoro-audio.js"></script>',
            1,
        )

    # 2. Replace speak() body — match from the "speak(text," signature up
    #    through the closing brace of that method (the line ending with `}`
    #    that is at 2-space indent and directly precedes a blank line).
    speak_re = re.compile(
        r"^  speak\(text, \{ cancelFirst = true \} = \{\}\) \{[\s\S]*?^  \}",
        re.MULTILINE,
    )
    if speak_re.search(text):
        text = speak_re.sub(NEW_SPEAK_TPL.format(lesson_id=lesson_id), text, count=1)

    # 3. Replace stopPlayback (both single-line and multi-line variants).
    stop_re = re.compile(
        r"^  stopPlayback\(\) \{[\s\S]*?^  \}"  # multi-line form
        r"|^  stopPlayback\(\) \{ [^\n]*\}",     # single-line form
        re.MULTILINE,
    )
    if stop_re.search(text):
        text = stop_re.sub(NEW_STOP, text, count=1)

    # 4. Replace playRepeated
    play_re = re.compile(
        r"^  async playRepeated\(text, times = 3\) \{[\s\S]*?^  \}",
        re.MULTILINE,
    )
    if play_re.search(text):
        text = play_re.sub(NEW_PLAY_REPEATED, text, count=1)

    # 5. Replace waitForPlaybackToFinish
    wait_re = re.compile(
        r"^  async waitForPlaybackToFinish\(token\) \{[\s\S]*?^  \}",
        re.MULTILINE,
    )
    if wait_re.search(text):
        text = wait_re.sub(NEW_WAIT, text, count=1)

    if text == original:
        return "skipped"

    path.write_text(text, encoding="utf-8")
    return "patched"


def main() -> int:
    targets = [LESSONS_DIR / f"buoi-{n}.html" for n in range(4, 21)]
    missing = [p for p in targets if not p.exists()]
    if missing:
        print("Missing files:", *missing, sep="\n  ", file=sys.stderr)
        return 1

    results: dict[str, list[str]] = {"patched": [], "skipped": [], "no-match": []}
    for path in targets:
        outcome = patch_file(path)
        results[outcome].append(path.name)

    for outcome, files in results.items():
        print(f"{outcome}: {len(files)}")
        for f in files:
            print(f"  - {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
