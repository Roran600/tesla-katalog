#!/usr/bin/env python3
"""Import the download list and its 21 PDFs; normal builds need no archive."""
import re
import shutil
import sys
from pathlib import Path

source = Path(sys.argv[1]) / 'Ke stažení'
target = Path('static/katalog/na-stiahnutie')
page = Path('content/docs/katalog/na-stiahnutie.md')
if target.exists():
    raise SystemExit('Destination already exists')
original = (source / 'index.md').read_text(encoding='utf-8')
rows = re.findall(r'^- \[(.*?)\]\(<([^>]+)>\) — (\d+) B$', original, re.M)
if len(rows) != 21:
    raise SystemExit(f'Expected 21 PDFs; found {len(rows)}')
old = page.read_text(encoding='utf-8')
front = old.split('---', 2)[1].strip()
target.mkdir(parents=True)
links = []
for title, name, size in rows:
    if Path(name).name != name or not name.endswith('.pdf'):
        raise SystemExit(f'Unexpected filename: {name}')
    src = source / name
    with src.open('rb') as pdf:
        magic = pdf.read(5)
    if src.stat().st_size != int(size) or magic != b'%PDF-':
        raise SystemExit(f'Invalid PDF or size: {src}')
    shutil.copy2(src, target / name)
    links.append(f'- [{title}]({{{{< katalog-asset "katalog/na-stiahnutie/{name}" >}}}}) — {size} B')
page.write_text('---\n' + front + '\n---\n\nKatalógy a ďalšie dokumenty zo zálohy stránky „Ke stažení“.\n\n## Súbory PDF\n\n' + '\n'.join(links) + '\n', encoding='utf-8')
print(f'Imported {len(rows)} PDF documents')
