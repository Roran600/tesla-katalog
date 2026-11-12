#!/usr/bin/env python3
"""One-time import of the Pramet category from the processed archive.

Run from stranka/ with the dataset path as the sole argument. The site build
does not depend on the archive or this script.
"""
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

source = Path(sys.argv[1]) / "Termistory Pramet"
content = Path("content/docs/katalog/termistory-pramet")
assets = Path("static/katalog/termistory-pramet")
entries = sorted(p for p in source.iterdir() if p.is_dir() and (p / "index.md").exists())
if len(entries) != 24:
    raise SystemExit(f"Expected 24 entries, found {len(entries)}")
for entry in entries:
    original = (entry / "index.md").read_text(encoding="utf-8")
    front, body = original.removeprefix("---\n").split("\n---\n", 1)
    title = re.search(r'^title: "(.*)"$', front, re.M).group(1)
    if not re.fullmatch(r"[A-Za-z0-9-]+", title) or title != entry.name:
        raise SystemExit(f"Unexpected identifier: {entry}")
    body = re.sub(r"^# .*?\n", "", body, count=1).lstrip()
    body = body.replace("[Termistory Pramet](<../index.md>)", '[Termistory Pramet]({{< relref "/docs/katalog/termistory-pramet" >}})')
    for label in ('**Označenie:**', '**Popis:**', '**Kľúčové slová:**'):
        body = body.replace('\n' + label, '\n\n' + label, 1)
    destination = assets / title.lower()
    destination.mkdir(parents=True, exist_ok=True)
    for asset in entry.iterdir():
        if asset.name == "index.md":
            continue
        if not asset.is_file():
            raise SystemExit(f"Unexpected asset: {asset}")
        shutil.copy2(asset, destination / asset.name)
        url = f"katalog/termistory-pramet/{title.lower()}/{quote(asset.name)}"
        body = re.sub(r'(!\[[^\]]*\]\()<' + re.escape(asset.name) + r'>(\))',
                      lambda match: match.group(1) + '/' + url + match.group(2), body)
        body = body.replace(f"<{asset.name}>", '{{< katalog-asset "' + url + '" >}}')
    front = re.sub(r'^type: "component"\n', '', front, flags=re.M)
    front += '\nsidebar:\n  exclude: true\noutputs: [html, markdown]\ncontextMenu: true'
    body = re.sub(r'(?m)^[ \t]+$', '', body)
    body = re.sub(r'(?m)^([^\n]*\S) {2,}$', lambda m: m.group(1) + '\\', body)
    body = body.replace('\\\n\n', '\n\n')
    (content / f"{title.lower()}.md").write_text(f"---\n{front}\n---\n\n{body}", encoding="utf-8")
print(f"Imported {len(entries)} termistors")
