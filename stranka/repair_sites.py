#!/usr/bin/env python3
"""Apply navigation and locale fixes to the four generated standalone sites."""
import json
from pathlib import Path
import re

import yaml

import build_sites

ROOT = Path(__file__).resolve().parent


def parts(text):
    if not text.startswith("---\n"):
        raise ValueError("Missing YAML frontmatter")
    _, front, body = text.split("---", 2)
    return yaml.safe_load(front), body.lstrip("\n")


def write(path, front, body):
    path.write_text(
        "---\n" + yaml.safe_dump(front, allow_unicode=True, sort_keys=False)
        + "---\n\n" + body.rstrip() + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    files = build_sites.source_inventory()
    pages, media = build_sites.build_mapping(files)
    for theme in build_sites.THEMES:
        site = ROOT / theme
        for original, page in pages.items():
            output = site / "content" / page["file"]
            front, _ = parts(output.read_text(encoding="utf-8"))
            front.pop("collapsibleMenu", None)
            body = build_sites.rewrite_body(page["body"], original, page["url"], pages, media)
            write(output, front, body)
        source_home = pages["O webu/index.md"]
        for filename, url, root_home in [("_index.md", "/", True), ("docs/_index.md", "/docs/", False)]:
            output = site / "content" / filename
            front, _ = parts(output.read_text(encoding="utf-8"))
            body = build_sites.rewrite_body(source_home["body"], "O webu/index.md", url, pages, media)
            body = re.sub(r"!\[[^\]]*\]\(<[^>]+>\)\s*", "", body)
            if root_home and theme == "hudocs":
                body = "# Tesla katalóg súčiastok\n\n" + body
            body += "\n\n## Dokumentácia datasetu\n\n"
            for label, original in [("Štruktúra datasetu", "STRUCTURE.md"), ("Audit pôvodu dát", "AUDIT_COMPARISON.md")]:
                body += f"- [{label}](<{pages[original]['url']}>)\n"
            write(output, front, body)
        (site / "hugo.toml").write_text(build_sites.config_for(theme), encoding="utf-8")
        mapping = {"pages": {k: {x: v[x] for x in ("file", "url", "section")} for k, v in pages.items()}, "media": media}
        (site / "page-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(theme, "links and configuration updated", flush=True)
