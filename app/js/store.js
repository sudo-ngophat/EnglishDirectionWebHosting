// The ONLY module that touches localStorage. Single key: ash_state_v1.
import { todayStr } from './srs.js';

const KEY = 'ash_state_v1';

export function defaultState() {
  return {
    version: 1,
    createdAt: new Date().toISOString(),
    cards: {},
    daily: { date: todayStr(), newIntroduced: 0, reviewsDone: 0 },
    streak: { count: 0, lastCompleted: null },
    history: []
  };
}

export function load() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return defaultState();
    const s = JSON.parse(raw);
    if (!s || s.version !== 1 || typeof s.cards !== 'object') return defaultState();
    return s;
  } catch {
    return defaultState();
  }
}

export function save(state) {
  localStorage.setItem(KEY, JSON.stringify(state));
}

export function cardKey(id, skill) { return `${id}:${skill}`; }

export function getCard(state, id, skill) {
  return state.cards[cardKey(id, skill)] || null;
}

export function putCard(state, id, skill, card) {
  state.cards[cardKey(id, skill)] = card;
  return state;
}

export function resetAll() {
  localStorage.removeItem(KEY);
}
