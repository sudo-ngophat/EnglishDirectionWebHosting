import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const siteDir = path.resolve(__dirname, '..', '..');
const wordsPath = path.join(siteDir, 'app', 'data', 'words.json');
const indexPath = path.join(siteDir, 'index.html');
const lessonPath = path.join(siteDir, 'lessons', 'buoi-1-dba-architecture.html');

const expectedTerms = [
  'architecture',
  'topology',
  'deployment',
  'service',
  'component',
  'endpoint',
  'source',
  'target',
  'hub',
  'hub-based',
];

let pass = 0, fail = 0;
function t(name, fn) {
  try { fn(); pass++; console.log('ok -', name); }
  catch (e) { fail++; console.error('FAIL -', name, '\n  ', e.message); }
}

t('main index links to the DBA architecture lesson', () => {
  const html = fs.readFileSync(indexPath, 'utf8');
  assert.ok(html.includes('lessons/buoi-1-dba-architecture.html'));
  assert.ok(html.includes('DBA/GoldenGate — Buổi 1'));
});

t('DBA architecture lesson contains the required mental model and reading terms', () => {
  const html = fs.readFileSync(lessonPath, 'utf8');
  assert.ok(html.includes('Oracle source'));
  assert.ok(html.includes('GoldenGate hub'));
  assert.ok(html.includes('PostgreSQL target'));
  for (const term of expectedTerms) assert.ok(html.includes(term), `${term} missing from lesson`);
});

t('Adaptive Hub word data includes the ten DBA architecture terms', () => {
  const data = JSON.parse(fs.readFileSync(wordsPath, 'utf8'));
  const words = data.words.map(w => w.word);
  for (const term of expectedTerms) assert.ok(words.includes(term), `${term} missing from words.json`);
});

console.log(`\n${pass} passed, ${fail} failed`);
if (fail > 0) process.exit(1);
