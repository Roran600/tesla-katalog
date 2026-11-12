#!/usr/bin/env python3
"""Check the generated subpath output and SHA-256 against one dataset category.

Usage: python3 scripts/test_import_kategoria.py DATASET CATEGORY SLUG OUTPUT
"""
import hashlib
import re
import sys
from pathlib import Path

source = Path(sys.argv[1]) / sys.argv[2]
slug = sys.argv[3]
output = Path(sys.argv[4])
assets = Path('static/katalog') / slug
index_html = (output / 'docs/katalog' / slug / 'index.html').read_text(encoding='utf-8')
items = scans = 0
for index in sorted(source.glob('*/index.md')):
    original = index.read_text(encoding='utf-8')
    if 'type: "component"' not in original:
        continue
    name = index.parent.name.lower()
    title = re.search(r'^title: "(.*)"$', original, re.M).group(1)
    page_url = f'/tesla/docs/katalog/{slug}/{name}/'
    assert page_url in index_html, page_url
    html = (output / 'docs/katalog' / slug / name / 'index.html').read_text(encoding='utf-8')
    assert title in html, title
    items += 1
    for f in index.parent.iterdir():
        if f.name == 'index.md':
            continue
        target = assets / name / f.name
        published = output / 'katalog' / slug / name / f.name
        digest = lambda p: hashlib.sha256(p.read_bytes()).digest()
        assert digest(f) == digest(target) == digest(published), f
        assert f'/tesla/katalog/{slug}/{name}/{f.name}' in html, f
        scans += 1
print(f'{items} entries, {scans} assets verified')
