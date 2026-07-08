(() => {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const synth = window.speechSynthesis;

  const el = {
    lessonSel: document.getElementById('lessonSel'),
    voiceSel: document.getElementById('voiceSel'),
    wordBig: document.getElementById('wordBig'),
    wordIpa: document.getElementById('wordIpa'),
    wordMeaning: document.getElementById('wordMeaning'),
    btnListen: document.getElementById('btnListen'),
    btnMic: document.getElementById('btnMic'),
    scoreRing: document.getElementById('scoreRing'),
    scoreVal: document.getElementById('scoreVal'),
    heard: document.getElementById('heard'),
    tipMsg: document.getElementById('tipMsg'),
    curNum: document.getElementById('curNum'),
    totalNum: document.getElementById('totalNum'),
    btnPrev: document.getElementById('btnPrev'),
    btnNext: document.getElementById('btnNext'),
    avgBar: document.getElementById('avgBar'),
    avgVal: document.getElementById('avgVal'),
    avgCount: document.getElementById('avgCount'),
    supportWarn: document.getElementById('supportWarn')
  };

  const state = { lesson: '13', idx: 0, words: [], scores: [], recognizing: false, voice: null };

  // --- Voice list for the "listen sample" (browser TTS) ---
  function loadVoices() {
    const voices = synth.getVoices().filter(v => v.lang && v.lang.toLowerCase().startsWith('en'));
    el.voiceSel.innerHTML = '';
    if (!voices.length) {
      const opt = document.createElement('option');
      opt.textContent = 'Mặc định';
      el.voiceSel.appendChild(opt);
      state.voice = null;
      return;
    }
    voices.forEach((v, i) => {
      const opt = document.createElement('option');
      opt.value = String(i);
      opt.textContent = `${v.name} (${v.lang})`;
      el.voiceSel.appendChild(opt);
    });
    const preferred = voices.findIndex(v => v.lang.toLowerCase().startsWith('en-us'));
    const chosen = preferred >= 0 ? preferred : 0;
    el.voiceSel.value = String(chosen);
    state.voice = voices[chosen];
    el.voiceSel.onchange = () => { state.voice = voices[parseInt(el.voiceSel.value, 10)] || null; };
  }
  loadVoices();
  if (typeof synth.onvoiceschanged !== 'undefined') synth.onvoiceschanged = loadVoices;

  // --- Lesson selector ---
  function buildLessonSelector() {
    el.lessonSel.innerHTML = '';
    Object.keys(PRON_LESSONS).forEach(key => {
      const opt = document.createElement('option');
      opt.value = key;
      opt.textContent = PRON_LESSONS[key].title;
      el.lessonSel.appendChild(opt);
    });
    el.lessonSel.value = state.lesson;
    el.lessonSel.onchange = () => { loadLesson(el.lessonSel.value); };
  }

  function loadLesson(key) {
    state.lesson = key;
    state.words = PRON_LESSONS[key].words.slice();
    state.idx = 0;
    state.scores = [];
    el.totalNum.textContent = state.words.length;
    el.avgBar.classList.remove('show');
    renderWord();
  }

  // --- Render current word ---
  function renderWord() {
    const w = state.words[state.idx];
    el.wordBig.textContent = w.word;
    el.wordIpa.textContent = w.ipa || '';
    el.wordMeaning.textContent = w.meaning || '';
    el.curNum.textContent = state.idx + 1;
    el.scoreRing.style.display = 'none';
    el.heard.innerHTML = '';
    el.tipMsg.textContent = '';
    const prev = state.scores[state.idx];
    if (typeof prev === 'number') showScore(prev, null, true);
  }

  // --- Listen to the sample ---
  function listen() {
    const word = state.words[state.idx].word;
    if (window.HumanAudio) {
      window.HumanAudio.play({
        lessonId: `buoi-${state.lesson}`,
        key: word,
        text: word,
        rate: 0.85,
        voice: state.voice,
      });
      return;
    }
    if (!synth) return;
    synth.cancel();
    const u = new SpeechSynthesisUtterance(word);
    if (state.voice) u.voice = state.voice;
    u.lang = state.voice ? state.voice.lang : 'en-US';
    u.rate = 0.85;
    synth.speak(u);
  }

  // --- Levenshtein distance for fuzzy similarity ---
  function levenshtein(a, b) {
    const m = a.length, n = b.length;
    if (!m) return n;
    if (!n) return m;
    const d = Array.from({ length: m + 1 }, (_, i) => [i, ...Array(n).fill(0)]);
    for (let j = 0; j <= n; j++) d[0][j] = j;
    for (let i = 1; i <= m; i++) {
      for (let j = 1; j <= n; j++) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost);
      }
    }
    return d[m][n];
  }

  function normalize(s) {
    return String(s || '').toLowerCase().trim().replace(/[^a-z]/g, '');
  }

  // --- Score a transcript against the target word ---
  function scoreTranscript(target, alternatives) {
    const t = normalize(target);
    let best = 0;
    let bestHeard = '';
    alternatives.forEach(alt => {
      // an alternative may contain several words; test each token + whole string
      const tokens = normalize(alt.transcript).length ? [normalize(alt.transcript)] : [];
      alt.transcript.split(/\s+/).forEach(tok => { const n = normalize(tok); if (n) tokens.push(n); });
      tokens.forEach(tok => {
        if (!tok) return;
        const dist = levenshtein(t, tok);
        const sim = 1 - dist / Math.max(t.length, tok.length);
        const conf = typeof alt.confidence === 'number' && alt.confidence > 0 ? alt.confidence : 0.75;
        // blend character similarity (weight 0.8) with ASR confidence (weight 0.2)
        const raw = sim * 0.8 + conf * 0.2;
        const score = Math.round(Math.max(0, Math.min(1, raw)) * 100);
        if (score > best) { best = score; bestHeard = tok; }
      });
    });
    return { score: best, heard: bestHeard };
  }

  function showScore(score, heard, isReplay) {
    el.scoreRing.style.display = 'flex';
    el.scoreVal.textContent = score;
    el.scoreRing.classList.remove('good', 'mid', 'low');
    el.scoreRing.classList.add(score >= 80 ? 'good' : score >= 55 ? 'mid' : 'low');
    if (heard) el.heard.innerHTML = `Nghe được: <b>${heard}</b>`;
    if (!isReplay) {
      el.tipMsg.textContent =
        score >= 80 ? 'Rất tốt! Phát âm rõ và đúng.' :
        score >= 55 ? 'Khá ổn. Nghe lại mẫu và thử nhấn âm rõ hơn.' :
        'Chưa đúng lắm. Nghe mẫu, chú ý IPA rồi thử lại.';
    }
  }

  function updateAverage() {
    const done = state.scores.filter(s => typeof s === 'number');
    if (!done.length) return;
    const avg = Math.round(done.reduce((a, b) => a + b, 0) / done.length);
    el.avgVal.textContent = avg;
    el.avgCount.textContent = `(${done.length}/${state.words.length} từ đã luyện)`;
    el.avgBar.classList.add('show');
    try {
      const key = `pron_${state.lesson}_avg`;
      const hist = JSON.parse(localStorage.getItem(key) || '[]');
      hist.push({ date: new Date().toISOString(), avg, count: done.length });
      localStorage.setItem(key, JSON.stringify(hist.slice(-20)));
    } catch (e) { /* localStorage unavailable */ }
  }

  // --- Speech recognition ---
  function startRecognition() {
    if (!SR || state.recognizing) return;
    const rec = new SR();
    rec.lang = 'en-US';
    rec.interimResults = false;
    rec.maxAlternatives = 5;
    state.recognizing = true;
    el.btnMic.classList.add('recording');
    el.btnMic.textContent = '● Đang nghe...';
    el.heard.textContent = '';
    el.tipMsg.textContent = '';

    rec.onresult = (event) => {
      const res = event.results[0];
      const alternatives = [];
      for (let i = 0; i < res.length; i++) {
        alternatives.push({ transcript: res[i].transcript, confidence: res[i].confidence });
      }
      const { score, heard } = scoreTranscript(state.words[state.idx].word, alternatives);
      state.scores[state.idx] = score;
      showScore(score, heard || alternatives[0].transcript, false);
      updateAverage();
    };
    rec.onerror = (event) => {
      el.tipMsg.textContent = event.error === 'not-allowed'
        ? 'Chưa cấp quyền micro. Hãy cho phép micro trong trình duyệt.'
        : event.error === 'no-speech'
          ? 'Không nghe thấy giọng nói. Thử lại và nói to hơn.'
          : `Lỗi nhận diện: ${event.error}`;
    };
    rec.onend = () => {
      state.recognizing = false;
      el.btnMic.classList.remove('recording');
      el.btnMic.innerHTML = '&#127908; Nói';
    };
    try { rec.start(); } catch (e) { state.recognizing = false; }
  }

  // --- Wire up events ---
  el.btnListen.onclick = listen;
  el.btnMic.onclick = startRecognition;
  el.btnPrev.onclick = () => { if (state.idx > 0) { state.idx--; renderWord(); } };
  el.btnNext.onclick = () => { if (state.idx < state.words.length - 1) { state.idx++; renderWord(); } };
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'SELECT') return;
    if (e.key === 'ArrowLeft') el.btnPrev.click();
    else if (e.key === 'ArrowRight') el.btnNext.click();
    else if (e.code === 'Space') { e.preventDefault(); startRecognition(); }
  });

  if (!SR) {
    el.supportWarn.style.display = 'block';
    el.btnMic.disabled = true;
    el.btnMic.title = 'Trình duyệt không hỗ trợ nhận diện giọng nói';
  }

  buildLessonSelector();
  loadLesson(state.lesson);
})();
