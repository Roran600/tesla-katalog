const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const output = process.argv[2] || 'public';
const html = fs.readFileSync(path.join(output, 'index.html'), 'utf8');
assert.match(html, /Powered by Hextra/);
assert.match(html, /© 2026–<span id="tesla-current-year">\d{4}<\/span> Roran60<br>Autorské práva patria pôvodným vlastníkom/);
assert.ok(html.indexOf('Powered by Hextra') < html.indexOf('tesla-current-year'));
assert.match(html, /<script defer src="\/js\/footer-year\.js"><\/script>/);

const code = fs.readFileSync(path.join(output, 'js/footer-year.js'), 'utf8');
const year = { textContent: '2026' };
let currentYear = 2026;
let interval;
let visibility;
vm.runInNewContext(code, {
  Date: class { getFullYear() { return currentYear; } },
  document: {
    getElementById: (id) => id === 'tesla-current-year' ? year : null,
    addEventListener: (event, callback) => { if (event === 'visibilitychange') visibility = callback; },
  },
  setInterval: (callback, delay) => { assert.equal(delay, 3600000); interval = callback; },
});
assert.equal(year.textContent, 2026);
currentYear = 2027;
interval();
assert.equal(year.textContent, 2027);
currentYear = 2028;
visibility();
assert.equal(year.textContent, 2028);
console.log('Pätička: text, poradie a zmena roka 2026 → 2027 → 2028 sú v poriadku.');
