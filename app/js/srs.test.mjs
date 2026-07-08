import assert from 'node:assert';
import { newCard, review, addDays, todayStr } from './srs.js';

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log('ok -', name); }
  catch (e) { fail++; console.error('FAIL -', name, '\n  ', e.message); }
}

t('newCard defaults', () => {
  const c = newCard('2026-06-18');
  assert.equal(c.ease, 2.5);
  assert.equal(c.interval, 0);
  assert.equal(c.reps, 0);
  assert.equal(c.lapses, 0);
  assert.equal(c.due, '2026-06-18');
});

t('addDays handles month rollover', () => {
  assert.equal(addDays('2026-06-30', 1), '2026-07-01');
});

t('first correct -> interval 1 day', () => {
  const c = review(newCard('2026-06-18'), 'correct', '2026-06-18');
  assert.equal(c.reps, 1);
  assert.equal(c.interval, 1);
  assert.equal(c.due, '2026-06-19');
});

t('second correct -> interval 6 days', () => {
  let c = review(newCard('2026-06-18'), 'correct', '2026-06-18');
  c = review(c, 'correct', '2026-06-19');
  assert.equal(c.reps, 2);
  assert.equal(c.interval, 6);
  assert.equal(c.due, '2026-06-25');
});

t('third correct -> interval round(prev*ease)', () => {
  let c = review(newCard('2026-06-18'), 'correct', '2026-06-18');
  c = review(c, 'correct', '2026-06-19');
  const before = c.ease;
  c = review(c, 'correct', '2026-06-25');
  assert.equal(c.reps, 3);
  assert.equal(c.interval, Math.round(6 * before));
});

t('wrong resets reps and interval, due today', () => {
  let c = review(newCard('2026-06-18'), 'correct', '2026-06-18');
  c = review(c, 'wrong', '2026-06-19');
  assert.equal(c.reps, 0);
  assert.equal(c.interval, 0);
  assert.equal(c.due, '2026-06-19');
  assert.equal(c.lapses, 1);
});

t('wrong lowers ease but not below 1.3', () => {
  let c = newCard('2026-06-18');
  for (let i = 0; i < 20; i++) c = review(c, 'wrong', '2026-06-18');
  assert.ok(c.ease >= 1.3);
});

t('correct raises ease', () => {
  const c = review(newCard('2026-06-18'), 'correct', '2026-06-18');
  assert.ok(c.ease > 2.5);
});

console.log(`\n${pass} passed, ${fail} failed`);
if (fail > 0) process.exit(1);
