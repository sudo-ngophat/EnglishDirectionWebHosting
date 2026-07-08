// Pure SM-2 scheduler. No DOM, no storage. Date-only ISO strings (YYYY-MM-DD), local time.

export function todayStr(d = new Date()) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

export function addDays(dateStr, n) {
  const [y, m, d] = dateStr.split('-').map(Number);
  const dt = new Date(y, m - 1, d);
  dt.setDate(dt.getDate() + n);
  return todayStr(dt);
}

export function newCard(today) {
  return { ease: 2.5, interval: 0, reps: 0, due: today, lapses: 0 };
}

export function review(card, grade, today) {
  const c = { ...card };
  if (grade === 'wrong') {
    c.reps = 0;
    c.interval = 0;
    c.lapses = (c.lapses || 0) + 1;
    c.ease = Math.max(1.3, c.ease - 0.2);
    c.due = today;
    return c;
  }
  c.reps = (c.reps || 0) + 1;
  if (c.reps === 1) c.interval = 1;
  else if (c.reps === 2) c.interval = 6;
  else c.interval = Math.round(c.interval * c.ease);
  c.ease = Math.min(3.0, c.ease + 0.1);
  c.due = addDays(today, c.interval);
  return c;
}
