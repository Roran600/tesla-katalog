#!/usr/bin/env python3
"""Compare each detail's main HTML with HTTrack; TLS authentication is disabled.

Usage: python3 scripts/audit_kategoria.py DATASET ARCHIVE CATEGORY
This does not verify the image bytes or the TLS identity of the server.
"""
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

source = Path(sys.argv[1]) / sys.argv[3]
mirror = Path(sys.argv[2]) / 'teslakatalog.cz'
context = ssl._create_unverified_context()
for item in sorted(source.iterdir()):
    index = item / 'index.md'
    if not index.is_file():
        continue
    metadata = index.read_text(encoding='utf-8')
    if 'type: "component"' not in metadata:
        continue
    url = re.search(r'^source_url: "([^"]+)"$', metadata, re.M).group(1)
    filename = re.search(r'^source_html: "([^"]+)"$', metadata, re.M).group(1)
    try:
        with urllib.request.urlopen(url, context=context, timeout=20) as response:
            live = response.read()
        archived = (mirror / filename).read_bytes()
        def content(data):
            match = re.search(rb'<td class="forContent"[^>]*>(.*?)</td>', data, re.S | re.I)
            if not match:
                raise ValueError('forContent not found')
            return re.sub(rb'\s+', b' ', match.group(1)).strip()
        result = 'ZHODA' if content(live) == content(archived) else 'ROZDIEL'
    except (OSError, ValueError, urllib.error.URLError) as error:
        result = f'NEOVERENÉ: {error}'
    print(f'{item.name}\t{result}\t{url}', flush=True)
