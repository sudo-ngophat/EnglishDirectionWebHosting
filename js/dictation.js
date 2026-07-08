class DictationEngine {
  constructor(lessonData) {
    this.data = lessonData;
    this.mode = 'vocabulary';
    this.currentIndex = 0;
    this.score = { correct: 0, total: 0 };
    this.speed = 0.7;
    this.synth = window.speechSynthesis;
    this.voice = null;
    this.answered = false;
    this.queue = [];
    this.storageKey = `dictation_${lessonData.name}`;
    this.mistakesKey = `mistakes_${lessonData.name}`;
    this.autoRepeatCount = 0;

    this.init();
  }

  init() {
    this.loadVoices();
    this.bindEvents();
    this.loadProgress();
    this.switchMode('vocabulary');
  }

  loadVoices() {
    const setVoice = () => {
      const voices = this.synth.getVoices();
      this.voice = voices.find(v => v.lang.startsWith('en') && v.name.includes('Female'))
        || voices.find(v => v.lang.startsWith('en-US'))
        || voices.find(v => v.lang.startsWith('en'))
        || voices[0];

      const select = document.getElementById('voiceSelect');
      if (select) {
        select.innerHTML = '';
        voices.filter(v => v.lang.startsWith('en')).forEach((v, i) => {
          const opt = document.createElement('option');
          opt.value = i;
          opt.textContent = `${v.name} (${v.lang})`;
          if (v === this.voice) opt.selected = true;
          select.appendChild(opt);
        });
      }
    };
    setVoice();
    this.synth.onvoiceschanged = setVoice;
  }

  bindEvents() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => this.switchMode(btn.dataset.mode));
    });

    document.getElementById('btnPlay').addEventListener('click', () => this.autoRepeat());
    document.getElementById('btnReplay').addEventListener('click', () => this.speak());
    document.getElementById('btnCheck').addEventListener('click', () => this.checkAnswer());
    document.getElementById('btnShowAnswer').addEventListener('click', () => this.showAnswer());
    document.getElementById('btnNext').addEventListener('click', () => this.next());

    const btnSpell = document.getElementById('btnSpell');
    if (btnSpell) btnSpell.addEventListener('click', () => this.spellOut());

    const btnContext = document.getElementById('btnContext');
    if (btnContext) btnContext.addEventListener('click', () => this.speakContext());

    const input = document.getElementById('dictInput');
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') this.checkAnswer();
      if (e.ctrlKey && e.code === 'Space') { e.preventDefault(); this.speak(); }
      if (e.ctrlKey && e.code === 'KeyS') { e.preventDefault(); this.spellOut(); }
    });

    document.getElementById('speedSelect').addEventListener('change', (e) => {
      this.speed = parseFloat(e.target.value);
    });

    document.getElementById('voiceSelect').addEventListener('change', (e) => {
      const voices = this.synth.getVoices().filter(v => v.lang.startsWith('en'));
      this.voice = voices[parseInt(e.target.value)] || this.voice;
    });
  }

  switchMode(mode) {
    this.mode = mode;
    this.currentIndex = 0;
    this.score = { correct: 0, total: 0 };
    this.answered = false;

    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    const spellBtn = document.getElementById('btnSpell');
    const ctxBtn = document.getElementById('btnContext');
    if (spellBtn) spellBtn.style.display = (mode === 'vocabulary') ? '' : 'none';
    if (ctxBtn) ctxBtn.style.display = (mode === 'vocabulary') ? '' : 'none';

    this.buildQueue();
    this.updateUI();
  }

  buildQueue() {
    const items = this.getRawItems();
    this.queue = items.map((item, i) => ({ item, originalIndex: i, retries: 0 }));
    this.currentIndex = 0;
  }

  getRawItems() {
    switch (this.mode) {
      case 'vocabulary': return this.data.vocabulary;
      case 'sentences': return this.data.sentences;
      case 'passage': return this.data.passage;
      case 'fillblank': return this.data.fillblank;
      default: return [];
    }
  }

  getCurrentEntry() {
    if (this.currentIndex >= this.queue.length) return null;
    return this.queue[this.currentIndex];
  }

  getCurrentText() {
    const entry = this.getCurrentEntry();
    if (!entry) return null;
    const item = entry.item;
    switch (this.mode) {
      case 'vocabulary': return item.word;
      case 'sentences': return item;
      case 'passage': return item;
      case 'fillblank': return item.answer;
      default: return null;
    }
  }

  getSpeakText() {
    const entry = this.getCurrentEntry();
    if (!entry) return null;
    const item = entry.item;
    switch (this.mode) {
      case 'vocabulary': return item.word;
      case 'sentences': return item;
      case 'passage': return item;
      case 'fillblank': return item.sentence;
      default: return null;
    }
  }

  getAudioKey() {
    const entry = this.getCurrentEntry();
    if (!entry) return null;
    const item = entry.item;
    const number = String(entry.originalIndex + 1).padStart(3, '0');

    switch (this.mode) {
      case 'vocabulary': return `dictation:vocabulary:${item.word}`;
      case 'sentences': return `dictation:sentence:${number}`;
      case 'passage': return `dictation:passage:${number}`;
      case 'fillblank': return `dictation:fillblank:${number}`;
      default: return null;
    }
  }

  getPromptText() {
    const entry = this.getCurrentEntry();
    if (!entry) return '';
    const item = entry.item;
    switch (this.mode) {
      case 'vocabulary':
        return item.hint ? `Gợi ý: ${item.hint}` : 'Nghe từ và gõ lại';
      case 'sentences':
        return 'Nghe câu và gõ lại chính xác';
      case 'passage':
        return 'Nghe từng câu trong đoạn văn và gõ lại';
      case 'fillblank':
        return item.display;
      default:
        return '';
    }
  }

  // --- Listening Strategies ---

  playWithHumanAudio(text, rate, onend = null) {
    const lessonId = this.data.lessonId;
    const key = this.getAudioKey();
    const options = { lessonId, key, text, rate, voice: this.voice, onend };

    if (window.AudioEngine && typeof window.AudioEngine.play === 'function') {
      window.AudioEngine.play(options);
      return;
    }
    if (window.HumanAudio) {
      window.HumanAudio.play(options);
      return;
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = this.voice;
    utterance.rate = rate;
    utterance.pitch = 1;
    if (typeof onend === 'function') utterance.onend = onend;
    this.synth.speak(utterance);
  }

  autoRepeat() {
    const text = this.getSpeakText();
    if (!text) return;
    this.synth.cancel();
    this.autoRepeatCount = 0;
    const speeds = [0.6, 0.85, 1.0];
    this._chainSpeak(text, speeds, 0);
  }

  _chainSpeak(text, speeds, idx) {
    if (idx >= speeds.length) return;
    this.playWithHumanAudio(text, speeds[idx], () => {
      this.autoRepeatCount++;
      setTimeout(() => this._chainSpeak(text, speeds, idx + 1), 600);
    });
  }

  speak() {
    const text = this.getSpeakText();
    if (!text) return;
    this.synth.cancel();
    this.playWithHumanAudio(text, this.speed);
  }

  spellOut() {
    const text = this.getCurrentText();
    if (!text) return;
    this.synth.cancel();
    const letters = text.split('').filter(c => c !== ' ').join(', ');
    if (window.AudioEngine && typeof window.AudioEngine.play === 'function') {
      window.AudioEngine.play({
        lessonId: this.data.lessonId,
        key: `dictation:spell:${this.getAudioKey() || text}`,
        text: letters,
        rate: 0.5,
        voice: this.voice,
      });
    } else {
      const utterance = new SpeechSynthesisUtterance(letters);
      utterance.voice = this.voice;
      utterance.rate = 0.5;
      utterance.pitch = 1;
      this.synth.speak(utterance);
    }

    const ipaEl = document.getElementById('ipaHint');
    if (ipaEl) {
      const entry = this.getCurrentEntry();
      const item = entry ? entry.item : null;
      if (item && item.ipa) {
        ipaEl.textContent = `${item.syllables || '?'} âm tiết: ${item.ipa}`;
        ipaEl.style.display = 'block';
      }
    }
  }

  speakContext() {
    const entry = this.getCurrentEntry();
    if (!entry || this.mode !== 'vocabulary') return;
    const item = entry.item;
    if (item.context) {
      this.synth.cancel();
      if (window.AudioEngine && typeof window.AudioEngine.play === 'function') {
        window.AudioEngine.play({
          lessonId: this.data.lessonId,
          key: `dictation:context:${item.word}`,
          text: item.context,
          rate: 0.8,
          voice: this.voice,
        });
        return;
      }
      const utterance = new SpeechSynthesisUtterance(item.context);
      utterance.voice = this.voice;
      utterance.rate = 0.8;
      utterance.pitch = 1;
      this.synth.speak(utterance);
    }
  }

  // --- Core Logic ---

  checkAnswer() {
    if (this.answered) return;
    const input = document.getElementById('dictInput');
    const userAnswer = input.value.trim();
    if (!userAnswer) return;

    const correctAnswer = this.getCurrentText();
    if (!correctAnswer) return;

    this.answered = true;
    this.score.total++;

    const isCorrect = this.normalize(userAnswer) === this.normalize(correctAnswer);

    if (isCorrect) {
      this.score.correct++;
      input.classList.add('correct');
      this.showFeedback(`<span class="answer">Correct!</span>`);
    } else {
      input.classList.add('incorrect');
      const entry = this.getCurrentEntry();
      entry.retries++;
      if (entry.retries <= 2) {
        this.queue.push(entry);
      }
      this.saveMistake(userAnswer, correctAnswer);
      if (this.mode === 'fillblank') {
        this.showFeedback(`<span class="wrong-word">Sai!</span> Đáp án: <span class="answer">${correctAnswer}</span>`);
      } else {
        const diff = this.getDiff(userAnswer, correctAnswer);
        this.showFeedback(`${diff}<br><span class="answer">${correctAnswer}</span>`);
      }
    }

    document.getElementById('btnNext').disabled = false;
    this.saveProgress();
  }

  normalize(str) {
    return str.toLowerCase().replace(/[^a-z0-9\s]/g, '').replace(/\s+/g, ' ').trim();
  }

  getDiff(user, correct) {
    const userWords = user.split(/\s+/);
    const correctWords = correct.split(/\s+/);
    let html = '';
    const maxLen = Math.max(userWords.length, correctWords.length);
    for (let i = 0; i < maxLen; i++) {
      const uw = (userWords[i] || '').toLowerCase().replace(/[^a-z0-9]/g, '');
      const cw = (correctWords[i] || '').toLowerCase().replace(/[^a-z0-9]/g, '');
      if (uw === cw) {
        html += `<span class="correct-word">${correctWords[i] || ''}</span> `;
      } else {
        html += `<span class="wrong-word">${userWords[i] || '___'}</span> `;
      }
    }
    return html;
  }

  showAnswer() {
    const correctAnswer = this.getCurrentText();
    if (!correctAnswer) return;
    this.answered = true;
    this.score.total++;
    const entry = this.getCurrentEntry();
    if (entry) {
      entry.retries++;
      if (entry.retries <= 2) this.queue.push(entry);
    }
    this.saveMistake('(skipped)', correctAnswer);
    this.showFeedback(`<span class="answer">Đáp án: ${correctAnswer}</span>`);
    document.getElementById('btnNext').disabled = false;
    document.getElementById('dictInput').classList.add('incorrect');
    this.saveProgress();
  }

  next() {
    this.currentIndex++;
    this.answered = false;

    if (this.currentIndex >= this.queue.length) {
      this.showComplete();
      return;
    }
    this.updateUI();
  }

  updateUI() {
    const input = document.getElementById('dictInput');
    input.value = '';
    input.style.display = '';
    input.classList.remove('correct', 'incorrect');
    input.focus();

    document.getElementById('btnPlay').disabled = false;
    document.getElementById('btnReplay').disabled = false;
    document.getElementById('btnCheck').disabled = false;
    document.getElementById('btnShowAnswer').disabled = false;
    document.getElementById('btnNext').disabled = true;
    document.getElementById('feedback').innerHTML = '';
    document.getElementById('scoreBoard').style.display = 'none';

    const ipaEl = document.getElementById('ipaHint');
    if (ipaEl) {
      const entry = this.getCurrentEntry();
      const item = entry ? entry.item : null;
      if (this.mode === 'vocabulary' && item && item.ipa) {
        ipaEl.textContent = `${item.syllables || '?'} âm tiết: ${item.ipa}`;
        ipaEl.style.display = 'block';
      } else {
        ipaEl.style.display = 'none';
      }
    }

    const total = this.queue.length;
    const current = Math.min(this.currentIndex + 1, total);
    document.getElementById('progressText').textContent = `${current} / ${total}`;
    document.getElementById('progressFill').style.width = `${(current / total) * 100}%`;

    document.getElementById('promptText').textContent = this.getPromptText();

    if (this.mode === 'fillblank') {
      input.placeholder = 'Gõ từ cần điền...';
    } else {
      input.placeholder = 'Gõ lại những gì bạn nghe...';
    }

    setTimeout(() => this.autoRepeat(), 400);
  }

  showFeedback(html) {
    document.getElementById('feedback').innerHTML = html;
  }

  showComplete() {
    const pct = this.score.total > 0
      ? Math.round((this.score.correct / this.score.total) * 100) : 0;

    document.getElementById('scoreBoard').style.display = 'block';
    document.getElementById('scoreNumber').textContent = `${pct}%`;
    document.getElementById('scoreDetail').textContent =
      `${this.score.correct} / ${this.score.total} câu đúng`;

    document.getElementById('dictInput').style.display = 'none';
    document.getElementById('promptText').textContent = 'Hoàn thành!';
    document.getElementById('btnPlay').disabled = true;
    document.getElementById('btnReplay').disabled = true;
    document.getElementById('btnCheck').disabled = true;
    document.getElementById('btnNext').disabled = true;
    document.getElementById('btnShowAnswer').disabled = true;

    this.saveProgress();
  }

  restart() {
    this.buildQueue();
    this.score = { correct: 0, total: 0 };
    this.answered = false;
    this.updateUI();
  }

  // --- Persistence ---

  saveProgress() {
    const progress = this.loadAllProgress();
    progress[this.mode] = {
      correct: this.score.correct,
      total: this.score.total,
      pct: this.score.total > 0 ? Math.round((this.score.correct / this.score.total) * 100) : 0,
      lastAttempt: new Date().toISOString()
    };
    localStorage.setItem(this.storageKey, JSON.stringify(progress));
    this.renderHistory();
  }

  loadProgress() {
    this.renderHistory();
    this.renderMistakes();
  }

  loadAllProgress() {
    try {
      return JSON.parse(localStorage.getItem(this.storageKey)) || {};
    } catch { return {}; }
  }

  renderHistory() {
    const el = document.getElementById('historyPanel');
    if (!el) return;
    const progress = this.loadAllProgress();
    const modes = { vocabulary: 'Từ vựng', sentences: 'Câu ví dụ', passage: 'Đoạn văn', fillblank: 'Điền từ' };
    let html = '';
    for (const [mode, label] of Object.entries(modes)) {
      const p = progress[mode];
      if (p) {
        const date = new Date(p.lastAttempt).toLocaleDateString('vi-VN');
        html += `<div class="history-item"><span>${label}</span><span class="history-score">${p.pct}%</span><span class="history-date">${date}</span></div>`;
      }
    }
    el.innerHTML = html || '<div class="history-empty">Chưa có lịch sử</div>';
  }

  // --- Mistakes DB ---

  saveMistake(userAnswer, correctAnswer) {
    const mistakes = this.loadMistakes();
    const key = this.normalize(correctAnswer);
    const existing = mistakes.find(m => this.normalize(m.correct) === key);

    if (existing) {
      existing.count++;
      existing.lastWrong = userAnswer;
      existing.lastDate = new Date().toISOString();
    } else {
      mistakes.push({
        mode: this.mode,
        correct: correctAnswer,
        lastWrong: userAnswer,
        count: 1,
        lastDate: new Date().toISOString()
      });
    }

    localStorage.setItem(this.mistakesKey, JSON.stringify(mistakes));
    this.renderMistakes();
  }

  loadMistakes() {
    try {
      return JSON.parse(localStorage.getItem(this.mistakesKey)) || [];
    } catch { return []; }
  }

  clearMistakes() {
    localStorage.removeItem(this.mistakesKey);
    this.renderMistakes();
  }

  renderMistakes() {
    const el = document.getElementById('mistakesPanel');
    if (!el) return;

    const mistakes = this.loadMistakes();
    if (mistakes.length === 0) {
      el.innerHTML = '<div class="mistakes-empty">Chưa có câu sai nào.</div>';
      return;
    }

    const sorted = mistakes.sort((a, b) => b.count - a.count);

    let html = `<div class="mistakes-header">
      <h3>Câu sai (${mistakes.length})</h3>
      <button class="btn btn-secondary btn-sm" onclick="engine.clearMistakes()">Xóa tất cả</button>
    </div>`;
    html += '<table class="mistakes-table"><thead><tr><th>Đáp án đúng</th><th>Bạn gõ</th><th>Lần sai</th><th>Ngày</th></tr></thead><tbody>';

    for (const m of sorted.slice(0, 30)) {
      const date = new Date(m.lastDate).toLocaleDateString('vi-VN');
      html += `<tr>
        <td><span class="correct-word">${m.correct}</span></td>
        <td><span class="wrong-word">${m.lastWrong}</span></td>
        <td><span class="mistake-count">${m.count}x</span></td>
        <td><span class="history-date">${date}</span></td>
      </tr>`;
    }

    html += '</tbody></table>';
    el.innerHTML = html;
  }
}
