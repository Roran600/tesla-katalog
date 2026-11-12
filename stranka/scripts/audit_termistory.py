#!/usr/bin/env python3
"""Compare Pramet detail content with the HTTrack HTML (TLS unverified).

Run from stranka/: python3 scripts/audit_termistory.py ../zaloha-dataset-clean ../zaloha-data
This does not modify either archive or verify image/PDF bytes.
"""
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

dataset = Path(sys.argv[1]) / 'Termistory Pramet'
mirror = Path(sys.argv[2]) / 'teslakatalog.cz'
context = ssl._create_unverified_context()  # The original site's certificate has expired.
entries = sorted(p.name for p in dataset.iterdir() if (p / 'index.md').is_file())
if len(entries) != 24:
    raise SystemExit(f'Unexpected count: {len(entries)}')

for name in entries:
    url = f'https://teslakatalog.cz/{name}.html'
    try:
        with urllib.request.urlopen(url, context=context, timeout=20) as response:
            live = response.read()
        archived = (mirror / f'{name}.html').read_bytes()
        def content(data):
            match = re.search(rb'<td class="forContent"[^>]*>(.*?)</td>', data, re.S | re.I)
            if not match:
                raise ValueError('forContent not found')
            return re.sub(rb'\s+', b' ', match.group(1)).strip()
        result = 'ZHODA' if content(live) == content(archived) else 'ROZDIEL'
    except (OSError, ValueError, urllib.error.URLError) as error:
        result = f'NEOVERENÉ: {error}'
    print(f'{name}\t{result}\t{url}', flush=True)
