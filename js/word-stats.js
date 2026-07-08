// Shared per-word stats — bridges the 4-in-1 drills into the Review Mix
// spaced-repetition pool. Writes to the SAME localStorage key ('rm_stats')
// that js/review-mix.js reads, so a word missed in a drill immediately
// resurfaces more often in Review Mix.
//
// Stats shape (per word):  { right, wrong, seen, last }
// Plain global (no ES module) so inline drill scripts can call it directly.
(function (global) {
  'use strict';

  var STATS_KEY = 'rm_stats';

  function load() {
    try { return JSON.parse(localStorage.getItem(STATS_KEY) || '{}'); }
    catch (e) { return {}; }
  }

  function save(stats) {
    try { localStorage.setItem(STATS_KEY, JSON.stringify(stats)); } catch (e) {}
  }

  // words:    array of the lesson's word objects (needs .word)
  // mistakes: array of { word, phase, detail } accumulated during the drill
  // Each distinct lesson word counts as one "seen"; wrong if it appears in
  // mistakes (any phase), otherwise right. Returns how many were marked wrong.
  function recordDrill(words, mistakes) {
    if (!words || !words.length) return 0;
    var missed = {};
    (mistakes || []).forEach(function (m) {
      if (m && m.word) missed[m.word.toLowerCase()] = true;
    });

    var stats = load();
    var now = Date.now();
    var wrongCount = 0;
    var seenThisRun = {};

    words.forEach(function (w) {
      var word = (w && w.word) ? w.word : w;
      if (!word) return;
      var lc = word.toLowerCase();
      if (seenThisRun[lc]) return;   // dedupe within one run
      seenThisRun[lc] = true;

      var e = stats[word] || { right: 0, wrong: 0, seen: 0, last: 0 };
      e.seen++;
      if (missed[lc]) { e.wrong++; wrongCount++; }
      else { e.right++; }
      e.last = now;
      stats[word] = e;
    });

    save(stats);
    return wrongCount;
  }

  global.WordStats = { recordDrill: recordDrill, STATS_KEY: STATS_KEY };
})(window);
