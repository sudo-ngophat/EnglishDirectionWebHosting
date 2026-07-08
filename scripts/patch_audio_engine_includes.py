"""Add AudioEngine includes to pages that still use speech synthesis."""
from __future__ import annotations

from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]

LESSON_READING_SCRIPT = """  <script src="../js/human-audio.js"></script>
  <script src="../js/audio-engine.js"></script>
  <script src="../js/audio-settings.js"></script>
"""

TOEIC_SCRIPT = """  <script src="../js/audio-engine.js"></script>
  <script src="../js/audio-settings.js"></script>
"""

TOEIC_AUDIO_OLD = """    if (!q.audio_script) return;
    this.synth.cancel();
    const utt = new SpeechSynthesisUtterance(q.audio_script);
    utt.voice = this.voice;
    utt.rate = 0.85;
    this.synth.speak(utt);"""

TOEIC_AUDIO_NEW = """    if (!q.audio_script) return;
    this.synth.cancel();
    if (window.AudioEngine) {
      window.AudioEngine.play({ key: `toeic:${q.id}`, text: q.audio_script, rate: 0.85, voice: this.voice });
      return;
    }
    const utt = new SpeechSynthesisUtterance(q.audio_script);
    utt.voice = this.voice;
    utt.rate = 0.85;
    this.synth.speak(utt);"""


def insert_before_inline_script(text: str, script: str) -> str:
    marker = "  <script>\n"
    if script.strip() in text:
        return text
    if marker not in text:
        return text
    return text.replace(marker, script + marker, 1)


def main() -> None:
    changed = []

    for path in sorted((SITE_ROOT / "lessons").glob("buoi-*-reading.html")):
        text = path.read_text(encoding="utf-8")
        new_text = insert_before_inline_script(text, LESSON_READING_SCRIPT)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed.append(path.relative_to(SITE_ROOT).as_posix())

    for folder in (SITE_ROOT / "toeic", SITE_ROOT / "toeic-v2"):
        for path in sorted(folder.glob("buoi-*.html")):
            text = path.read_text(encoding="utf-8")
            new_text = insert_before_inline_script(text, TOEIC_SCRIPT)
            if TOEIC_AUDIO_OLD in new_text:
                new_text = new_text.replace(TOEIC_AUDIO_OLD, TOEIC_AUDIO_NEW, 1)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
                changed.append(path.relative_to(SITE_ROOT).as_posix())

    print(f"changed={len(changed)}")
    for name in changed:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
