"""Wire lesson drill and reading pages to AudioEngine while keeping fallbacks."""
from __future__ import annotations

from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
LESSONS_DIR = SITE_ROOT / "lessons"

READING_SENTENCE_OLD = """  listenSentence(num) {
    const sentence = this.data.sentences[num];
    if (!sentence) return;
    this.synth.cancel();
    const utt = new SpeechSynthesisUtterance(sentence);
    utt.voice = this.voice;
    utt.rate = 0.8;
    this.synth.speak(utt);
  }"""

READING_SENTENCE_NEW = """  listenSentence(num) {
    const sentence = this.data.sentences[num];
    if (!sentence) return;
    this.synth.cancel();
    const lessonId = this.data.lessonId || null;
    if (window.AudioEngine) {
      window.AudioEngine.play({ lessonId, key: `reading:sentence:${num}`, text: sentence, rate: 0.8, voice: this.voice });
      return;
    }
    const utt = new SpeechSynthesisUtterance(sentence);
    utt.voice = this.voice;
    utt.rate = 0.8;
    this.synth.speak(utt);
  }"""

READING_ALL_OLD = """  listenAll() {
    const fullText = this.data.passage.filter(l => l !== '').join(' ').replace(/\\{\\d+\\}/g, (m) => {
      const num = m.replace(/[{}]/g, '');
      return this.data.answers[num];
    });
    this.synth.cancel();
    const utt = new SpeechSynthesisUtterance(fullText);
    utt.voice = this.voice;
    utt.rate = 0.85;
    this.synth.speak(utt);
  }"""

READING_ALL_NEW = """  listenAll() {
    const fullText = this.data.passage.filter(l => l !== '').join(' ').replace(/\\{\\d+\\}/g, (m) => {
      const num = m.replace(/[{}]/g, '');
      return this.data.answers[num];
    });
    this.synth.cancel();
    const lessonId = this.data.lessonId || null;
    if (window.AudioEngine) {
      window.AudioEngine.play({ lessonId, key: 'reading:passage', text: fullText, rate: 0.85, voice: this.voice });
      return;
    }
    const utt = new SpeechSynthesisUtterance(fullText);
    utt.voice = this.voice;
    utt.rate = 0.85;
    this.synth.speak(utt);
  }"""

DRILL_SPEAK_OLD_TPL = """  speak(text, {{ cancelFirst = true }} = {{}}) {{
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

DRILL_SPEAK_NEW_TPL = """  speak(text, {{ cancelFirst = true }} = {{}}) {{
    if (cancelFirst) this.stopPlayback();
    const lessonId = '{lesson_id}';
    return new Promise((resolve) => {{
      let done = false;
      const finish = () => {{ if (!done) {{ done = true; resolve(); }} }};
      const safety = setTimeout(finish, 8000);
      const wrapEnd = () => {{ clearTimeout(safety); finish(); }};
      const audioOptions = {{
        lessonId,
        key: this.phase === 0 ? text : `drill:phase${{this.phase}}:${{text}}`,
        text,
        rate: this.rate,
        voice: this.voice,
        onend: wrapEnd,
      }};
      if (window.AudioEngine) {{
        window.AudioEngine.play(audioOptions);
        return;
      }}
      if (this.phase === 0 && window.HumanAudio) {{
        window.HumanAudio.play(audioOptions);
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


def patch_reading(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    if READING_SENTENCE_OLD in text:
        text = text.replace(READING_SENTENCE_OLD, READING_SENTENCE_NEW, 1)
    if READING_ALL_OLD in text:
        text = text.replace(READING_ALL_OLD, READING_ALL_NEW, 1)
    if text == original:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def patch_drill(path: Path) -> bool:
    lesson_id = path.stem
    text = path.read_text(encoding="utf-8")
    old = DRILL_SPEAK_OLD_TPL.format(lesson_id=lesson_id)
    new = DRILL_SPEAK_NEW_TPL.format(lesson_id=lesson_id)
    if old not in text:
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> None:
    reading_ok, reading_skip = [], []
    drill_ok, drill_skip = [], []

    for reading in sorted(LESSONS_DIR.glob("buoi-*-reading.html")):
        (reading_ok if patch_reading(reading) else reading_skip).append(reading.name)

    for drill in sorted(LESSONS_DIR.glob("buoi-*.html")):
        if "-reading" in drill.name or "-dictation" in drill.name:
            continue
        (drill_ok if patch_drill(drill) else drill_skip).append(drill.name)

    print(f"reading patched: {len(reading_ok)}")
    for name in reading_ok:
        print(f"  - {name}")
    if reading_skip:
        print(f"reading skipped: {len(reading_skip)}")
        for name in reading_skip:
            print(f"  ~ {name}")

    print(f"drill patched: {len(drill_ok)}")
    for name in drill_ok:
        print(f"  - {name}")
    if drill_skip:
        print(f"drill skipped: {len(drill_skip)}")
        for name in drill_skip:
            print(f"  ~ {name}")


if __name__ == "__main__":
    main()
