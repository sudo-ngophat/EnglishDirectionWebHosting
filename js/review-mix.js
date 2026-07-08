// Review Mix — ôn trộn từ vựng 13 buổi với spaced repetition.
// Dùng chung dữ liệu PRON_LESSONS (js/pronunciation-data.js).
(function () {
  'use strict';

  var STATS_KEY = 'rm_stats';      // { word: {right, wrong, seen, last} }
  var HIST_KEY = 'rm_history';     // [{date, score, total}]

  // ---- Build word pool (dedupe by word, keep first lesson seen) ----
  function buildPool(scope) {
    var seen = {};
    var pool = [];
    Object.keys(PRON_LESSONS).forEach(function (key) {
      if (scope !== 'all' && scope !== key) return;
      var L = PRON_LESSONS[key];
      L.words.forEach(function (w) {
        if (seen[w.word]) return;
        seen[w.word] = true;
        pool.push({ word: w.word, ipa: w.ipa, meaning: w.meaning, lesson: key });
      });
    });
    return pool;
  }

  // full pool across all lessons — used for distractors regardless of scope
  function fullPool() { return buildPool('all'); }

  // ---- Stats ----
  function loadStats() {
    try { return JSON.parse(localStorage.getItem(STATS_KEY) || '{}'); }
    catch (e) { return {}; }
  }
  function saveStats(s) {
    try { localStorage.setItem(STATS_KEY, JSON.stringify(s)); } catch (e) {}
  }
  function recordAnswer(word, correct) {
    var s = loadStats();
    var e = s[word] || { right: 0, wrong: 0, seen: 0, last: 0 };
    e.seen++;
    if (correct) e.right++; else e.wrong++;
    e.last = Date.now();
    s[word] = e;
    saveStats(s);
  }

  // ---- Weight: higher = more likely to appear ----
  // New/unseen words get a solid baseline; wrong answers push weight up,
  // repeated correct answers push it down. Recently-seen words get damped
  // slightly so a session doesn't repeat the same word back-to-back.
  function weightFor(word, stats) {
    var e = stats[word];
    if (!e || e.seen === 0) return 3;            // unseen: study it
    var w = 1 + e.wrong * 3 - e.right * 0.8;
    if (w < 0.4) w = 0.4;                          // mastered words still recur rarely
    var ageMs = Date.now() - (e.last || 0);
    if (ageMs < 60 * 1000) w *= 0.5;              // seen <1 min ago: damp
    return w;
  }

  // Weighted sampling without replacement.
  function pickWeighted(pool, n, stats) {
    var items = pool.map(function (p) { return { p: p, w: weightFor(p.word, stats) }; });
    var out = [];
    var count = (n <= 0 || n > pool.length) ? pool.length : n;
    for (var k = 0; k < count && items.length; k++) {
      var total = items.reduce(function (a, b) { return a + b.w; }, 0);
      var r = Math.random() * total;
      var idx = 0;
      for (; idx < items.length; idx++) { r -= items[idx].w; if (r <= 0) break; }
      if (idx >= items.length) idx = items.length - 1;
      out.push(items[idx].p);
      items.splice(idx, 1);
    }
    return out;
  }

  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  // ---- Build one MCQ from a target word ----
  // Alternates direction: en2vi (show word, pick meaning) / vi2en (show meaning, pick word).
  function buildQuestion(target, all, dir) {
    var distractors = all.filter(function (p) {
      if (dir === 'en2vi') return p.meaning !== target.meaning;
      return p.word !== target.word;
    });
    var picks = shuffle(distractors).slice(0, 3);
    var choices = shuffle(picks.concat([target]));
    return {
      target: target,
      dir: dir,
      choices: choices.map(function (c) {
        return { text: dir === 'en2vi' ? c.meaning : c.word, correct: c === target };
      })
    };
  }

  // ---- TTS (native browser voice; no Kokoro dependency) ----
  var voice = null;
  function initVoice() {
    if (!('speechSynthesis' in window)) return;
    var set = function () {
      var v = window.speechSynthesis.getVoices();
      voice = v.find(function (x) { return x.lang && x.lang.indexOf('en-US') === 0; })
        || v.find(function (x) { return x.lang && x.lang.indexOf('en') === 0; }) || v[0];
    };
    set();
    window.speechSynthesis.onvoiceschanged = set;
  }
  function speak(text, lesson) {
    var audioOptions = {
      lessonId: lesson ? ('buoi-' + lesson) : null,
      key: text,
      text: text,
      rate: 0.9,
      voice: voice,
    };
    if (window.AudioEngine) {
      window.AudioEngine.play(audioOptions);
      return;
    }
    if (window.HumanAudio) {
      window.HumanAudio.play(audioOptions);
      return;
    }
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    var u = new SpeechSynthesisUtterance(text);
    if (voice) u.voice = voice;
    u.rate = 0.9;
    window.speechSynthesis.speak(u);
  }

  // ---- Quiz state + DOM ----
  var $ = function (id) { return document.getElementById(id); };
  var state = null;

  function buildScopeSelector() {
    var sel = $('scopeSel');
    var opt = document.createElement('option');
    opt.value = 'all'; opt.textContent = 'Tất cả 13 buổi';
    sel.appendChild(opt);
    Object.keys(PRON_LESSONS).forEach(function (key) {
      var o = document.createElement('option');
      o.value = key; o.textContent = PRON_LESSONS[key].title;
      sel.appendChild(o);
    });
  }

  function start() {
    var scope = $('scopeSel').value;
    var len = parseInt($('lenSel').value, 10);
    var pool = buildPool(scope);
    if (pool.length < 4) { alert('Cần ít nhất 4 từ để tạo câu hỏi.'); return; }
    var stats = loadStats();
    var picked = pickWeighted(pool, len, stats);
    state = {
      queue: picked,
      all: fullPool(),
      idx: 0,
      right: 0,
      streak: 0,
      total: picked.length,
      wrongWords: []
    };
    $('quizArea').style.display = 'block';
    $('summaryArea').style.display = 'none';
    $('totalNum').textContent = state.total;
    renderQuestion();
  }

  function renderQuestion() {
    var target = state.queue[state.idx];
    var dir = state.idx % 2 === 0 ? 'en2vi' : 'vi2en';
    var q = buildQuestion(target, state.all, dir);
    state.current = q;

    $('curNum').textContent = state.idx + 1;
    $('rightNum').textContent = state.right;
    $('streakNum').textContent = state.streak;
    $('progFill').style.width = (state.idx / state.total * 100) + '%';

    var st = loadStats()[target.word];
    var isWeak = st && st.wrong > st.right;
    var tag = isWeak
      ? '<span class="rm-tag weak">Hay sai — ôn kỹ</span>'
      : '<span class="rm-tag">Buổi ' + target.lesson + '</span>';

    var promptHtml, subHtml, label;
    if (dir === 'en2vi') {
      label = 'Từ này nghĩa là gì?';
      promptHtml = target.word + '<span class="listen" id="listenBtn" title="Nghe">&#128266;</span>';
      subHtml = target.ipa;
    } else {
      label = 'Chọn từ tiếng Anh đúng:';
      promptHtml = target.meaning;
      subHtml = '';
    }

    var choicesHtml = q.choices.map(function (c, i) {
      return '<button class="rm-choice" data-i="' + i + '">' + c.text + '</button>';
    }).join('');

    $('quizCard').innerHTML =
      tag +
      '<div class="rm-prompt-label">' + label + '</div>' +
      '<div class="rm-prompt">' + promptHtml + '</div>' +
      '<div class="rm-sub">' + subHtml + '</div>' +
      '<div class="rm-choices">' + choicesHtml + '</div>' +
      '<div class="rm-feedback" id="fb"></div>';

    $('btnNext').classList.remove('show');
    Array.prototype.forEach.call($('quizCard').querySelectorAll('.rm-choice'), function (b) {
      b.onclick = function () { answer(parseInt(b.getAttribute('data-i'), 10)); };
    });
    var lb = $('listenBtn');
    if (lb) { lb.onclick = function () { speak(target.word, target.lesson); }; speak(target.word, target.lesson); }
  }

  function answer(i) {
    var q = state.current;
    var target = q.target;
    var chosen = q.choices[i];
    var btns = $('quizCard').querySelectorAll('.rm-choice');
    Array.prototype.forEach.call(btns, function (b, bi) {
      b.disabled = true;
      if (q.choices[bi].correct) b.classList.add('correct');
      else if (bi === i) b.classList.add('wrong');
    });

    var correct = chosen.correct;
    recordAnswer(target.word, correct);
    if (correct) {
      state.right++;
      state.streak++;
      $('fb').innerHTML = 'Chính xác! <b>' + target.word + '</b> = ' + target.meaning + ' · ' + target.ipa;
    } else {
      state.streak = 0;
      state.wrongWords.push(target);
      $('fb').innerHTML = 'Sai. <b>' + target.word + '</b> = ' + target.meaning + ' · ' + target.ipa;
    }
    $('rightNum').textContent = state.right;
    $('streakNum').textContent = state.streak;
    $('progFill').style.width = ((state.idx + 1) / state.total * 100) + '%';
    $('btnNext').classList.add('show');
  }

  function next() {
    state.idx++;
    if (state.idx >= state.total) { finish(); return; }
    renderQuestion();
  }

  function finish() {
    var pct = Math.round(state.right / state.total * 100);
    try {
      var h = JSON.parse(localStorage.getItem(HIST_KEY) || '[]');
      h.push({ date: new Date().toISOString(), score: pct, total: state.total });
      localStorage.setItem(HIST_KEY, JSON.stringify(h.slice(-30)));
    } catch (e) {}

    // dedupe wrong words for the review list
    var seen = {}, weak = [];
    state.wrongWords.forEach(function (w) {
      if (seen[w.word]) return; seen[w.word] = true; weak.push(w);
    });
    var stats = loadStats();
    var weakHtml = '';
    if (weak.length) {
      weakHtml = '<div class="rm-weaklist"><h4>Cần ôn lại (' + weak.length + ' từ)</h4>' +
        weak.map(function (w) {
          var e = stats[w.word] || {};
          var rate = e.seen ? Math.round(e.right / e.seen * 100) : 0;
          return '<div class="rm-weakitem"><span class="w">' + w.word +
            '</span><span class="m">' + w.meaning +
            '</span><span class="miss">đúng ' + rate + '%</span></div>';
        }).join('') + '</div>';
    } else {
      weakHtml = '<p style="color:var(--success);margin-top:1rem;">Không sai câu nào. Xuất sắc!</p>';
    }

    $('quizArea').style.display = 'none';
    var area = $('summaryArea');
    area.style.display = 'block';
    area.innerHTML =
      '<div class="rm-card rm-summary">' +
      '<div class="rm-tag">Kết quả</div>' +
      '<div class="big-score">' + pct + '%</div>' +
      '<p>' + state.right + ' / ' + state.total + ' câu đúng</p>' +
      weakHtml +
      '<div style="margin-top:1.5rem;">' +
      '<button class="btn btn-play" id="btnAgain">Ôn tiếp &#8635;</button> ' +
      '<a class="btn btn-secondary" href="index.html" style="display:inline-block;">Về trang chủ</a>' +
      '</div></div>';
    $('btnAgain').onclick = start;
  }

  // ---- Init ----
  function init() {
    initVoice();
    buildScopeSelector();
    $('btnStart').onclick = start;
    $('btnNext').onclick = next;
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && $('btnNext').classList.contains('show')) next();
    });
  }
  document.addEventListener('DOMContentLoaded', init);
})();

