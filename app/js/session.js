// Pure: decides today's queue. No DOM, no storage.
import { newCard } from './srs.js';
import { cardKey } from './store.js';

export const SKILLS = ['listening', 'meaning', 'grammar', 'toeic'];
export const DEFAULT_LIMITS = { newWordsPerDay: 5, maxReviews: 40 };

// Returns ordered array of { wordId, skill }.
export function buildSession(words, state, today, limits = DEFAULT_LIMITS) {
  const items = [];

  // 1) Due reviews: any existing card with due <= today.
  const due = [];
  for (const w of words) {
    for (const skill of SKILLS) {
      const card = state.cards[cardKey(w.id, skill)];
      if (card && card.due <= today) {
        due.push({ wordId: w.id, skill, card });
      }
    }
  }
  // Most overdue first, then weakest (lowest reps) first.
  due.sort((a, b) => (a.card.due < b.card.due ? -1 : a.card.due > b.card.due ? 1 : a.card.reps - b.card.reps));
  for (const d of due.slice(0, limits.maxReviews)) {
    items.push({ wordId: d.wordId, skill: d.skill });
  }

  // 2) New words: words with no cards yet, capped per day.
  const introduced = (state.daily && state.daily.date === today) ? state.daily.newIntroduced : 0;
  let budget = Math.max(0, limits.newWordsPerDay - introduced);
  for (const w of words) {
    if (budget <= 0) break;
    const hasAny = SKILLS.some(s => state.cards[cardKey(w.id, s)]);
    if (!hasAny) {
      // New word starts with the listening skill, then its other skills follow in order.
      for (const skill of SKILLS) items.push({ wordId: w.id, skill, isNew: true });
      budget--;
    }
  }

  return items;
}

// Helper for app: ensure a card exists, creating a fresh one if needed.
export function ensureCard(state, id, skill, today) {
  const key = cardKey(id, skill);
  if (!state.cards[key]) state.cards[key] = newCard(today);
  return state.cards[key];
}
