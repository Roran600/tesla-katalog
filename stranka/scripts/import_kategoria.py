#!/usr/bin/env python3
"""Import one category; the resulting site has no dependency on the archive.

Run from stranka/: python3 scripts/import_kategoria.py DATASET 'CATEGORY' SLUG COUNT ARCHIVE
The original placeholder must still exist; never rerun over authored content.
"""
import hashlib
from html.parser import HTMLParser
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

dataset, category, slug, expected, archive = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), Path(sys.argv[5]) / 'teslakatalog.cz'

class ContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('h1', 'script', 'style'):
            self.skip += 1
        if tag == 'img' and not self.skip:
            self.items.append(('img', dict(attrs).get('src', '')))
    def handle_endtag(self, tag):
        if tag in ('h1', 'script', 'style'):
            self.skip -= 1
    def handle_data(self, data):
        text = ' '.join(data.split())
        if text and not self.skip:
            self.items.append(('text', text))
source = Path(dataset) / category
root = Path('content/docs/katalog')
placeholder = root / (slug + '.md')
content = root / slug
assets = Path('static/katalog') / slug
if not placeholder.is_file() or content.exists() or assets.exists():
    raise SystemExit('Destination already exists or placeholder is missing')
entries = sorted(p for p in source.iterdir() if p.is_dir() and (p / 'index.md').is_file()
                 and 'type: "component"' in (p / 'index.md').read_text(encoding='utf-8'))
if len(entries) != expected:
    raise SystemExit(f'Expected {expected} entries, found {len(entries)}')
old = placeholder.read_text(encoding='utf-8')
front = old.split('---', 2)[1].strip().replace('outputs: [html, markdown]', 'outputs: [html, rss, markdown]')
content.mkdir(parents=True)
lines = []
for entry in entries:
    original = (entry / 'index.md').read_text(encoding='utf-8')
    metadata, body = original.removeprefix('---\n').split('\n---\n', 1)
    title = re.search(r'^title: "(.*)"$', metadata, re.M).group(1)
    if not re.fullmatch(r'[A-Za-z0-9-]+', entry.name):
        raise SystemExit(f'Unexpected identifier: {entry}')
    page_slug = entry.name.lower()
    body = re.sub(r'^# .*?\n', '', body, count=1).lstrip()
    body = body.replace(f'[{category}](<../index.md>)', f'[{category}]({{{{< relref "/docs/katalog/{slug}" >}}}})')
    for label in ('**Označenie:**', '**Popis:**', '**Kľúčové slová:**'):
        body = body.replace('\n' + label, '\n\n' + label, 1)
    # Restore scan-to-edition context, which the processed dataset lists
    # separately from its scans. Verify every mapping against source bytes.
    labels = [s.strip() for s in body.split('## Obsah', 1)[1].split('## Scany', 1)[0].splitlines()
              if s.strip() and s.strip() != '* * *']
    if len(labels) > 1:
        source_html = re.search(r'^source_html: "([^"]+)"$', metadata, re.M).group(1)
        raw = (archive / source_html).read_bytes().decode('cp1250', errors='replace')
        match = re.search(r'<td class="forContent"[^>]*>(.*?)</td>', raw, re.I | re.S)
        if not match:
            raise SystemExit(f'Missing original content: {source_html}')
        parser = ContentParser()
        parser.feed(match.group(1))
        normalized = {label.strip('*'): label for label in labels}
        current = None
        images = []
        seen = set()
        for kind, value in parser.items:
            if kind == 'text' and value in normalized:
                current = normalized[value]
            elif kind == 'img' and value not in seen:
                images.append((value, current))
                seen.add(value)
        scans = sorted(entry.glob('scan-*'))
        if len(images) != len(scans):
            raise SystemExit(f'Scan mapping count differs: {source_html}')
        for (source_image, label), scan in zip(images, scans):
            old_scan = archive / source_image
            if not old_scan.is_file() or hashlib.sha256(old_scan.read_bytes()).digest() != hashlib.sha256(scan.read_bytes()).digest():
                raise SystemExit(f'Scan mapping differs: {source_html} {source_image}')
            if label:
                body = body.replace(f'- [Sken {int(scan.name[5:7])} —', f'**{label}**\n\n- [Sken {int(scan.name[5:7])} —', 1)
    destination = assets / page_slug
    destination.mkdir(parents=True)
    for asset in entry.iterdir():
        if asset.name == 'index.md':
            continue
        if not asset.is_file():
            raise SystemExit(f'Unexpected asset: {asset}')
        shutil.copy2(asset, destination / asset.name)
        url = f'katalog/{slug}/{page_slug}/{quote(asset.name)}'
        body = re.sub(r'(!\[[^\]]*\]\()<' + re.escape(asset.name) + r'>(\))',
                      lambda match: match.group(1) + '/' + url + match.group(2), body)
        body = body.replace(f'<{asset.name}>', '{{< katalog-asset "' + url + '" >}}')
    metadata = re.sub(r'^type: "component"\n', '', metadata, flags=re.M)
    metadata += '\nsidebar:\n  exclude: true\noutputs: [html, markdown]\ncontextMenu: true'
    body = re.sub(r'(?m)^[ \t]+$', '', body)
    body = re.sub(r'(?m)^([^\n]*\S) {2,}$', lambda m: m.group(1) + '\\', body)
    body = body.replace('\\\n\n', '\n\n')
    (content / (page_slug + '.md')).write_text(f'---\n{metadata}\n---\n\n{body}', encoding='utf-8')
    lines.append(f'- [{title}]({{{{< relref "{page_slug}" >}}}})')
category_meta = (source / 'index.md').read_text(encoding='utf-8')
description = re.search(r'^description: "(.*)"$', category_meta, re.M).group(1)
category_front = category_meta.split('---', 2)[1].strip().splitlines()
front += '\n' + '\n'.join(line for line in category_front
                             if not line.startswith(('title:', 'type:')))
text = f'---\n{front}\n---\n\n{description}\n\n## Súčiastky\n\n' + '\n'.join(lines) + '\n'
(content / '_index.md').write_text(text, encoding='utf-8')
placeholder.unlink()
print(f'Imported {len(entries)} entries into {slug}')
