#!/usr/bin/env python3
"""Generate four independent catalog sites; never modify the source dataset."""
import hashlib
import json
import os
from pathlib import Path
import posixpath
import re
import shutil
import unicodedata
from urllib.parse import quote, unquote, urlsplit, urlunsplit

import yaml

ROOT = Path(__file__).resolve().parent
DATASET = ROOT.parent / "zaloha-dataset-clean"
THEMES = ("relearn", "book", "hextra", "hudocs")
PORTS = {"relearn": 1411, "book": 1412, "hextra": 1413, "hudocs": 1414}
CATEGORIES = [
    "Integrované obvody", "Tranzistory", "Tyristory, triaky", "Diody, varikapy",
    "Displeje, LED", "Kondenzátory", "Rezistory", "Tlumivky, filtry",
    "Krystaly, oscilátory", "Termistory Pramet",
]
LINK = re.compile(r"(\]\()(<[^>]+>|[^\s)]+)(\))")


def slug(text):
    plain = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_markdown(text):
    if not text.startswith("---\n"):
        raise ValueError("Missing YAML front matter")
    _, head, body = text.split("---", 2)
    return yaml.safe_load(head), body.lstrip("\n")


def write_markdown(path, frontmatter, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n" + yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False)
        + "---\n\n" + body.rstrip() + "\n", encoding="utf-8"
    )


def source_inventory():
    """Hash original bytes before generation, and verify them again during tests."""
    report = ROOT / "reports" / "source-sha256.json"
    files = sorted(p for p in DATASET.rglob("*") if p.is_file())
    actual = {p.relative_to(DATASET).as_posix(): sha256(p) for p in files}
    if report.exists():
        if json.loads(report.read_text()) != actual:
            raise RuntimeError("Source dataset differs from the recorded baseline")
    else:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(actual, ensure_ascii=False, indent=2) + "\n")
    return files


def build_mapping(files):
    pages, media, used = {}, {}, {}
    for path in files:
        relative = path.relative_to(DATASET)
        if relative.suffix == ".md":
            meta, body = split_markdown(path.read_text(encoding="utf-8"))
            directory = Path("docs", *(slug(p) for p in relative.parent.parts))
            if relative.name != "index.md":
                directory /= slug(relative.stem)
            section = meta["type"] in {"home", "category", "package-index"}
            # About owns two subsections and their logo/media; make it a branch bundle.
            if relative.as_posix() == "O webu/index.md":
                section = True
            target = directory / ("_index.md" if section else "index.md")
            url = "/" + directory.as_posix() + "/"
            if url in used:
                raise RuntimeError(f"Page URL collision: {relative} and {used[url]}")
            used[url] = relative.as_posix()
            pages[relative.as_posix()] = {
                "file": target.as_posix(), "url": url, "meta": meta, "body": body,
                "section": section,
            }
        elif relative.name == "MANIFEST.tsv":
            media[relative.as_posix()] = {"file": "dataset-manifest.tsv", "url": "/dataset-manifest.tsv", "static": True}
        elif relative.suffix.lower() == ".css" or relative.as_posix() == "O webu/Odkazy/bcsmb.gif":
            target = Path("dataset-media", *(slug(p) for p in relative.parts[:-1]), relative.name)
            media[relative.as_posix()] = {"file": target.as_posix(), "url": "/" + quote(target.as_posix(), safe="/._~-"), "static": True}
        else:
            directory = Path("docs", *(slug(p) for p in relative.parent.parts))
            target = directory / relative.name
            media[relative.as_posix()] = {"file": target.as_posix(), "url": "/" + quote(target.as_posix(), safe="/._~-"), "static": False}
    return pages, media


def rewrite_body(body, source_relative, output_url, pages, media):
    def replace(match):
        raw = match.group(2).strip("<>")
        parsed = urlsplit(raw)
        if parsed.scheme or parsed.netloc or raw.startswith("#"):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source_relative), unquote(parsed.path)))
        if resolved in pages:
            destination = pages[resolved]["url"]
        elif resolved in media:
            destination = media[resolved]["url"]
        else:
            raise RuntimeError(f"Unresolved dataset link in {source_relative}: {raw}")
        # Absolute page URLs resolve consistently in all four themes and through their custom hooks.
        # They remain portable when hosted at a domain root (the intended deployment mode).
        if resolved in pages or media[resolved]["static"]:
            encoded = destination
            return match.group(1) + "<" + encoded + ">" + match.group(3)
        # Page-bundle resources (scans and PDFs) stay relative to their own bundle.
        destination = posixpath.relpath(destination, output_url)
        encoded = urlunsplit(("", "", destination, parsed.query, parsed.fragment))
        return match.group(1) + "<" + encoded + ">" + match.group(3)

    body = LINK.sub(replace, body)
    # Themes render the page title; avoid duplicate H1s except on the home template
    # (Hudocs' stock home expects an H1 in Markdown).
    body = re.sub(r"\A# [^\n]+\n+", "", body)
    return body


def config_for(theme):
    common = f'''baseURL = "http://localhost:{PORTS[theme]}/"
title = "Tesla katalóg súčiastok"
theme = "{theme}"
locale = "cs-CZ"
defaultContentLanguage = "cs"
disablePathToLower = true
disableKinds = ["taxonomy", "term", "RSS"]
enableRobotsTXT = true
timeout = "300s"

[markup.goldmark.renderer]
unsafe = true
[markup.highlight]
noClasses = false
[markup.tableOfContents]
startLevel = 2
endLevel = 3

[outputs]
home = ["HTML"]
section = ["HTML"]
page = ["HTML"]
'''
    options = {
        "relearn": '''
[params]
disableLandingPageButton = true
disableInlineCopyToClipboard = true
collapsibleMenu = false
urlExternalCheck = false
[params.search.adapter]
identifier = "orama"
''',
        "book": '''
[params]
BookSection = "docs"
BookSearch = true
BookToC = true
BookBreadcrumbs = true
BookPortableLinks = "warning"
''',
        "hextra": '''
[params]
description = "Archív historických elektronických súčiastok Tesla"
[params.search]
enable = true
[params.page.contextMenu]
enable = false

[[menu.main]]
name = "Katalóg"
pageRef = "/docs"
weight = 1
[[menu.main]]
name = "Vyhľadávanie"
weight = 2
[menu.main.params]
type = "search"
''',
        "hudocs": '''
[params]
description = "Archív historických elektronických súčiastok Tesla"
docs_section = "docs"
docs_versions = false
docs_ai = false
docs_chatgpt = false
docs_claude = false
footer_copyright = "Tesla katalóg súčiastok"

[[menus.main]]
name = "Katalóg"
pageRef = "/docs"
weight = 1
''',
    }
    return common + options[theme]


def prepare(theme, files, pages, media):
    site = ROOT / theme
    if not (site / "themes" / theme).is_dir():
        raise RuntimeError(f"Missing theme snapshot: {theme}")
    if (site / "content").exists():
        raise RuntimeError(f"Refusing to overwrite existing content: {site / 'content'}")
    for i, (relative, item) in enumerate(media.items(), 1):
        dest = site / ("static" if item["static"] else "content") / item["file"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Copies, never source symlinks or hardlinks: sites remain self-contained.
        shutil.copy2(DATASET / relative, dest)
    for relative, page in pages.items():
        metadata = dict(page["meta"])
        metadata["dataset_type"] = metadata.pop("type")
        metadata["type"] = "docs"
        metadata["url"] = page["url"]
        metadata["source_dataset"] = relative
        # Keep the built-in sidebar manageable for a catalog of nearly 3,000 notes.
        if page["section"]:
            metadata["bookCollapseSection"] = True
            top = relative.split("/", 1)[0]
            metadata["weight"] = (CATEGORIES.index(top) + 1) * 10 if top in CATEGORIES else 120
        body = rewrite_body(page["body"], relative, page["url"], pages, media)
        write_markdown(site / "content" / page["file"], metadata, body)

    # Each site has its own home and catalog landing page, not a multi-theme switcher.
    home_page = pages["O webu/index.md"]
    front = {"title": "Tesla katalóg súčiastok", "description": "Katalóg historických súčiastok Tesla", "weight": 1}
    for output_file, url, home in [("_index.md", "/", True), ("docs/_index.md", "/docs/", False)]:
        metadata = dict(front)
        if not home:
            metadata.update({"type": "docs", "cascade": {"type": "docs"}})
        body = rewrite_body(home_page["body"], "O webu/index.md", url, pages, media)
        body = re.sub(r"!\[[^\]]*\]\(<[^>]+>\)\s*", "", body)
        if home and theme == "hudocs":
            body = "# Tesla katalóg súčiastok\n\n" + body
        body += "\n\n## Dokumentácia datasetu\n\n"
        for label, original in [("Štruktúra datasetu", "STRUCTURE.md"), ("Audit pôvodu dát", "AUDIT_COMPARISON.md")]:
            target = posixpath.relpath(pages[original]["url"], url) + "/"
            body += f"- [{label}](<{target}>)\n"
        write_markdown(site / "content" / output_file, metadata, body)

    site.joinpath("hugo.toml").write_text(config_for(theme), encoding="utf-8")
    upstream = json.loads((site / "themes" / "upstream.json").read_text())
    site.joinpath("README.md").write_text(f'''# Tesla katalóg — {theme}

Samostatný kompletný Hugo web: vlastná téma, konfigurácia, obsah aj skeny. Všetko potrebné je v tomto priečinku; ostatné tri weby ani pôvodný dataset nie sú potrebné na jeho zostavenie.

Upstream: {upstream['repository']}  
Commit témy: `{upstream['commit']}`

Zo zložky `stranka/`:

```sh
./hugo.sh {theme} build
./hugo.sh {theme} serve
```

Alebo priamo v tomto priečinku (Hugo Extended >= 0.166):

```sh
../.bin/hugo --cacheDir ../.cache/hugo/{theme}
../.bin/hugo server --cacheDir ../.cache/hugo/{theme} --disableFastRender
```

`content/docs/`: všetkých 2 928 Markdown stránok zdrojového datasetu; pridaná je iba domovská stránka a vstup do katalógu. Sekcie majú `_index.md`, súčiastky a púzdra `index.md` s kópiami skenov. Odkazy sú prevedené na webové URL bez `.md`. Súbor `page-map.json` mapuje každý pôvodný záznam na nový súbor a URL. Upstream šablóny a štýly nie sú upravené.
''', encoding="utf-8")
    mapping = {
        "pages": {k: {x: v[x] for x in ("file", "url", "section")} for k, v in pages.items()},
        "media": media,
    }
    (site / "page-map.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n")
    print(f"{theme}: {len(pages)} source pages + 2 landing pages, {len(media)} copied resources", flush=True)


if __name__ == "__main__":
    files = source_inventory()
    pages, media = build_mapping(files)
    for theme in THEMES:
        prepare(theme, files, pages, media)
