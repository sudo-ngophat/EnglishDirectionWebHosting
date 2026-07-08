import { todayStr, review } from './srs.js';
import * as store from './store.js';
import { buildSession, ensureCard, SKILLS } from './session.js';

const synth = window.speechSynthesis;
let voice = null;
function loadVoice() {
  const set = () => { const v = synth.getVoices(); voice = v.find(x => x.lang.startsWith('en-US')) || v.find(x => x.lang.startsWith('en')) || v[0]; };
  set(); synth.onvoiceschanged = set;
}
function speak(text, rate = 0.8) { synth.cancel(); const u = new SpeechSynthesisUtterance(text); u.voice = voice; u.rate = rate; synth.speak(u); }

const state = { words: [], data: null, queue: [], idx: 0, answered: false, st: null, today: todayStr() };

async function init() {
  loadVoice();
  const res = await fetch('data/words.json');
  state.data = await res.json();
  state.words = state.data.words;
  state.st = store.load();
  rollDaily();
  state.queue = buildSession(state.words, state.st, state.today);
  document.getElementById('cTotal').textContent = state.queue.length;
  document.getElementById('cStreak').textContent = state.st.streak.count;
  document.getElementById('btnNext').addEventListener('click', next);
  document.getElementById('btnProgress').addEventListener('click', renderProgress);
  renderCurrent();
}

function rollDaily() {
  if (state.st.daily.date !== state.today) {
    state.st.daily = { date: state.today, newIntroduced: 0, reviewsDone: 0 };
    store.save(state.st);
  }
}

function wordById(id) { return state.words.find(w => w.id === id); }

function renderCurrent() {
  state.answered = false;
  document.getElementById('btnNext').disabled = true;
  const card = document.getElementById('card');
  if (state.idx >= state.queue.length) return renderDone();
  const item = state.queue[state.idx];
  const w = wordById(item.wordId);
  if (item.skill === 'listening') renderListening(card, w);
  else if (item.skill === 'meaning') renderMeaning(card, w);
  else if (item.skill === 'grammar') renderGrammar(card, w);
  else renderToeic(card, w);
}

function grade(result) {
  const item = state.queue[state.idx];
  ensureCard(state.st, item.wordId, item.skill, state.today);
  const card = store.getCard(state.st, item.wordId, item.skill);
  const updated = review(card, result, state.today);
  store.putCard(state.st, item.wordId, item.skill, updated);
  if (item.isNew && item.skill === 'listening') state.st.daily.newIntroduced++;
  state.st.daily.reviewsDone++;
  store.save(state.st);
  document.getElementById('cDone').textContent = state.idx + 1;
  state.answered = true;
  document.getElementById('btnNext').disabled = false;
}

function next() { state.idx++; renderCurrent(); }

function shuffle(a){const r=[...a];for(let i=r.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[r[i],r[j]]=[r[j],r[i]];}return r;}

// PLACEHOLDER_RENDERERS

function renderListening(card, w) {
  card.innerHTML = `
    <div class="phase-label">Nghe & Viết</div>
    <div class="sub-prompt">Nghe và gõ lại từ bạn nghe</div>
    <button class="audio-btn" id="play">&#9654; Nghe</button>
    <input class="ash-input" id="inp" placeholder="Gõ từ..." autocomplete="off" spellcheck="false">
    <div class="feedback-box" id="fb"></div>`;
  const play = () => speak(w.word);
  document.getElementById('play').onclick = play;
  setTimeout(play, 300);
  const inp = document.getElementById('inp');
  inp.onkeydown = (e) => { if (e.key === 'Enter' && !state.answered) {
    const ok = inp.value.trim().toLowerCase() === w.word.toLowerCase();
    inp.classList.add(ok ? 'correct' : 'wrong');
    const fb = document.getElementById('fb');
    fb.className = 'feedback-box show ' + (ok ? 'ok' : 'err');
    fb.innerHTML = ok ? `Chính xác! "${w.word}" ${w.ipa}` : `Sai. Đáp án: <b>${w.word}</b> ${w.ipa}`;
    grade(ok ? 'correct' : 'wrong');
  }};
}

function renderMeaning(card, w) {
  const opts = shuffle([{t:w.meaning,ok:true}, ...w.confusers.map((c,i)=>({t:`${c}: ${w.confuserMeanings[i]}`,ok:false}))]);
  card.innerHTML = `
    <div class="phase-label">Nghĩa</div>
    <div class="word-prompt">${w.word}</div>
    <div class="sub-prompt">Chọn nghĩa đúng:</div>
    <ul class="choices" id="ch">${opts.map((o,i)=>`<li data-ok="${o.ok}">${String.fromCharCode(65+i)}. ${o.t}</li>`).join('')}</ul>
    <div class="feedback-box" id="fb"></div>`;
  card.querySelectorAll('#ch li').forEach(li => li.onclick = () => {
    if (state.answered) return;
    card.querySelectorAll('#ch li').forEach(el => { if (el.dataset.ok === 'true') el.classList.add('correct'); });
    const ok = li.dataset.ok === 'true';
    if (!ok) li.classList.add('wrong');
    const fb = document.getElementById('fb'); fb.className = 'feedback-box show ' + (ok?'ok':'err');
    fb.innerHTML = ok ? 'Chính xác!' : `Sai. "${w.word}" = ${w.meaning}`;
    grade(ok ? 'correct' : 'wrong');
  });
}

function renderGrammar(card, w) {
  const g = w.grammar;
  card.innerHTML = `
    <div class="phase-label">Ngữ pháp</div>
    <div class="sub-prompt">${g.original}<br>&#8595; Viết lại (chứa: <b>${g.keywords.join(', ')}</b>)</div>
    <input class="ash-input" id="inp" placeholder="Viết lại câu..." autocomplete="off" spellcheck="false">
    <div class="feedback-box" id="fb"></div>`;
  const inp = document.getElementById('inp');
  inp.onkeydown = (e) => { if (e.key === 'Enter' && !state.answered) {
    const val = inp.value.trim().toLowerCase();
    const ok = g.keywords.every(k => val.includes(k.toLowerCase())) && val.length > 10;
    inp.classList.add(ok ? 'correct' : 'wrong');
    const fb = document.getElementById('fb'); fb.className = 'feedback-box show ' + (ok?'ok':'err');
    fb.innerHTML = ok ? `Tốt! <em>${g.target}</em>` : `Chưa đúng. Mẫu: <em>${g.target}</em>`;
    grade(ok ? 'correct' : 'wrong');
  }};
}

function renderToeic(card, w) {
  const t = w.toeic;
  const order = shuffle(t.choices.map((c,i)=>({c,i})));
  card.innerHTML = `
    <div class="phase-label">TOEIC</div>
    <div class="sub-prompt" style="font-size:1rem;line-height:1.8;">${t.text}</div>
    <ul class="choices" id="ch">${order.map((o,i)=>`<li data-ok="${o.i===t.answer}">${String.fromCharCode(65+i)}. ${o.c}</li>`).join('')}</ul>
    <div class="feedback-box" id="fb"></div>`;
  card.querySelectorAll('#ch li').forEach(li => li.onclick = () => {
    if (state.answered) return;
    card.querySelectorAll('#ch li').forEach(el => { if (el.dataset.ok === 'true') el.classList.add('correct'); });
    const ok = li.dataset.ok === 'true';
    if (!ok) li.classList.add('wrong');
    const fb = document.getElementById('fb'); fb.className = 'feedback-box show ' + (ok?'ok':'err');
    fb.innerHTML = (ok ? 'Chính xác! ' : 'Sai. ') + t.explain;
    grade(ok ? 'correct' : 'wrong');
  });
}

function bucket(w) {
  const cards = SKILLS.map(s => store.getCard(state.st, w.id, s));
  if (cards.every(c => !c)) return 'new';
  if (cards.every(c => c && c.interval >= 21)) return 'mastered';
  return 'learning';
}

function renderProgress() {
  const counts = { new: 0, learning: 0, mastered: 0 };
  state.words.forEach(w => counts[bucket(w)]++);
  document.getElementById('card').innerHTML = `
    <div class="phase-label">Tiến độ</div>
    <div class="progress-wrap">
      <div class="stat"><div class="n">${counts.new}</div><div class="l">Mới</div></div>
      <div class="stat"><div class="n">${counts.learning}</div><div class="l">Đang học</div></div>
      <div class="stat"><div class="n">${counts.mastered}</div><div class="l">Đã thuộc</div></div>
      <div class="stat"><div class="n">${state.st.streak.count}</div><div class="l">Streak</div></div>
    </div>`;
  document.getElementById('btnNext').disabled = true;
}

function renderDone() {
  if (state.st.streak.lastCompleted !== state.today) {
    const prev = state.st.streak.lastCompleted;
    const yesterday = todayStr(new Date(Date.now() - 86400000));
    state.st.streak.count = (prev === yesterday) ? state.st.streak.count + 1 : 1;
    state.st.streak.lastCompleted = state.today;
    store.save(state.st);
    document.getElementById('cStreak').textContent = state.st.streak.count;
  }
  document.getElementById('card').innerHTML = `<div class="empty">Hôm nay bạn đã ôn xong. Quay lại ngày mai để tiếp tục lộ trình.</div>`;
  document.getElementById('btnNext').disabled = true;
}

init();

