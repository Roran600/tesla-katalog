#!/usr/bin/env python3
"""Expose copied source assets that are not linked from Markdown page bundles."""
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
DATASET = ROOT.parent / "zaloha-dataset-clean"
STATIC_MEDIA = ("O webu/stylcss.css", "O webu/Odkazy/bcsmb.gif")

if __name__ == "__main__":
    for theme in ("relearn", "book", "hextra", "hudocs"):
        site = ROOT / theme
        mapfile = site / "page-map.json"
        mapping = json.loads(mapfile.read_text(encoding="utf-8"))
        for original in STATIC_MEDIA:
            if original not in mapping["media"]:
                continue
            filename = Path(original).name
            target = Path("dataset-media") / Path(*[part.lower().replace(" ", "-") for part in Path(original).parts[:-1]]) / filename
            output = site / "static" / target
            output.parent.mkdir(parents=True, exist_ok=True)
            source = DATASET / original
            if not output.exists():
                output.write_bytes(source.read_bytes())
            mapping["media"][original] = {
                "file": target.as_posix(),
                "url": "/" + quote(target.as_posix(), safe="/._~-"),
                "static": True,
            }
        mapfile.write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(theme, "orphan media staged")
