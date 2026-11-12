#!/usr/bin/env python3
"""Import the 58 separate IO-package records, without classifying them as types.

Run from stranka/: python3 scripts/import_puzdra.py DATASET
"""
import re
import shutil
import sys
from pathlib import Path

source = Path(sys.argv[1]) / 'Integrované obvody/Púzdra'
base = Path('content/docs/katalog/integrovane-obvody')
content = base / 'puzdra'
assets = Path('static/katalog/integrovane-obvody/puzdra')
if content.exists() or assets.exists():
    raise SystemExit('Destination already exists')
entries = sorted(p for p in source.iterdir() if p.is_dir() and (p / 'index.md').is_file())
if len(entries) != 58:
    raise SystemExit(f'Expected 58 packages, found {len(entries)}')
content.mkdir()
links = []
for entry in entries:
    original = (entry / 'index.md').read_text(encoding='utf-8')
    metadata, body = original.removeprefix('---\n').split('\n---\n', 1)
    title = re.search(r'^title: "(.*)"$', metadata, re.M).group(1)
    page = re.search(r'^source_page: (\d+)$', metadata, re.M).group(1)
    slug = entry.name.lower().replace('_', '-')
    if not re.fullmatch(r'[a-z0-9-]+', slug):
        raise SystemExit(f'Unexpected package name {entry}')
    body = re.sub(r'^# .*?\n', '', body, count=1).lstrip()
    body = body.replace('[Integrované obvody](<../../index.md>)', '[Integrované obvody]({{< relref "/docs/katalog/integrovane-obvody" >}})')
    destination = assets / slug
    destination.mkdir(parents=True)
    for asset in entry.iterdir():
        if asset.name == 'index.md':
            continue
        shutil.copy2(asset, destination / asset.name)
        url = f'katalog/integrovane-obvody/puzdra/{slug}/{asset.name}'
        body = re.sub(r'(!\[[^\]]*\]\()<' + re.escape(asset.name) + r'>(\))',
                      lambda m: m.group(1) + '/' + url + m.group(2), body)
        body = body.replace(f'<{asset.name}>', '{{< katalog-asset "' + url + '" >}}')
    metadata = re.sub(r'^type: "package"\n', '', metadata, flags=re.M)
    metadata += '\nsidebar:\n  exclude: true\noutputs: [html, markdown]\ncontextMenu: true'
    body = re.sub(r'(?m)^[ \t]+$', '', body)
    body = re.sub(r'(?m)^([^\n]*\S) {2,}$', lambda m: m.group(1) + '\\', body)
    body = body.replace('\\\n\n', '\n\n')
    (content / (slug + '.md')).write_text(f'---\n{metadata}\n---\n\n{body}', encoding='utf-8')
    links.append(f'- [{title}]({{{{< relref "/docs/katalog/integrovane-obvody/puzdra/{slug}" >}}}}) — strana {page}')
(content / '_index.md').write_text('---\ntitle: "Puzdrá IO"\nsidebar:\n  exclude: true\noutputs: [html, rss, markdown]\ncontextMenu: true\n---\n\nPuzdrá sú samostatné záznamy, nie typy súčiastok.\n\n## Puzdrá\n\n' + '\n'.join(links) + '\n', encoding='utf-8')
with (base / '_index.md').open('a', encoding='utf-8') as f:
    f.write('\n## Puzdrá IO\n\nPuzdrá sú samostatné záznamy, nie typy súčiastok.\n\n' + '\n'.join(links) + '\n')
print(f'Imported {len(entries)} IO package records')
