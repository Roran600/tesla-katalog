#!/usr/bin/env python3
"""Check every migrated page, media byte and rendered local link in all four sites."""
import argparse
from collections import Counter
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent
THEMES = ("relearn", "book", "hextra", "hudocs")


class PageMarkup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        for name in ("href", "src", "poster", "action"):
            if values.get(name):
                self.references.append(values[name])
        for candidate in (values.get("srcset") or "").split(","):
            candidate = candidate.strip()
            if candidate:
                self.references.append(candidate.split()[0])
        if values.get("id"):
            self.ids.add(values["id"])


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def verify_source(baseline):
    source = ROOT.parent / "zaloha-dataset-clean"
    actual_paths = {p.relative_to(source).as_posix() for p in source.rglob("*") if p.is_file()}
    assert actual_paths == set(baseline), "Source dataset inventory changed"
    for relative, expected in baseline.items():
        assert digest(source / relative) == expected, f"Source bytes changed: {relative}"
    return len(baseline)


def test_site(theme, baseline):
    start = time.perf_counter()
    site = ROOT / theme
    built = ROOT / "reports" / "builds" / theme
    public = built if built.is_dir() else site / "public"
    mapping = json.loads((site / "page-map.json").read_text())
    failures = []
    missing_pages = []
    for original, page in mapping["pages"].items():
        output = public / page["url"].lstrip("/") / "index.html"
        if not output.is_file():
            missing_pages.append(original)
        migrated = site / "content" / page["file"]
        if not migrated.is_file():
            failures.append(f"Missing migrated content: {original}")

    media_checked = 0
    output_media_checked = 0
    for original, resource in mapping["media"].items():
        migrated = site / ("static" if resource["static"] else "content") / resource["file"]
        if not migrated.is_file() or digest(migrated) != baseline[original]:
            failures.append(f"Migrated resource differs: {original}")
        else:
            media_checked += 1
        rendered = public / unquote(resource["url"]).lstrip("/")
        if not rendered.is_file() or digest(rendered) != baseline[original]:
            failures.append(f"Published resource missing/differs: {original}")
        else:
            output_media_checked += 1

    html_files = sorted(public.rglob("*.html"))
    missing_links, bad_fragments = {}, {}
    file_cache, fragment_cache = {}, {}
    local_references = 0
    seen_refs = set()

    def check(raw, current_url, current_file):
        nonlocal local_references
        raw = html.unescape(raw).strip()
        parsed = urlsplit(raw)
        if parsed.scheme and parsed.scheme not in {"http", "https"}:
            return
        if parsed.netloc and parsed.hostname not in {"localhost", "127.0.0.1"}:
            return
        if not raw or raw == "#":
            return
        absolute = urlsplit(urljoin("http://localhost" + current_url, raw))
        destination = unquote(absolute.path)
        local_references += 1
        key = (destination, absolute.fragment)
        if key in seen_refs:
            return
        seen_refs.add(key)
        if destination not in file_cache:
            target = public / destination.lstrip("/")
            if target.is_dir():
                target /= "index.html"
            file_cache[destination] = target if target.is_file() else None
        target = file_cache[destination]
        if target is None:
            missing_links.setdefault(destination, {"from": current_file.relative_to(public).as_posix(), "href": raw})
            return
        fragment = unquote(absolute.fragment)
        if not fragment or fragment.startswith(":~:text=") or target.suffix != ".html":
            return
        if target not in fragment_cache:
            parser = PageMarkup()
            parser.feed(target.read_text(encoding="utf-8"))
            fragment_cache[target] = parser.ids
        if fragment not in fragment_cache[target]:
            bad_fragments.setdefault(destination + "#" + fragment, {"from": current_file.relative_to(public).as_posix(), "href": raw})

    for page in html_files:
        relative = page.relative_to(public).as_posix()
        current_url = "/" + relative
        if relative.endswith("index.html"):
            current_url = current_url[:-len("index.html")]
        parser = PageMarkup()
        parser.feed(page.read_text(encoding="utf-8"))
        for raw in parser.references:
            check(raw, current_url, page)

    source_types = Counter()
    for relative in mapping["pages"]:
        original = ROOT.parent / "zaloha-dataset-clean" / relative
        text = original.read_text(encoding="utf-8")
        match = re.search(r'^type: ["\']?([^"\'\n]+)', text, re.M)
        if match:
            source_types[match.group(1)] += 1
    result = {
        "passed": not (failures or missing_pages or missing_links or bad_fragments),
        "source_pages": len(mapping["pages"]), "source_types": dict(source_types),
        "content_pages": sum(1 for _ in (site / "content").rglob("*.md")),
        "rendered_html_files": len(html_files), "missing_pages": missing_pages,
        "media_bytes_verified": media_checked, "published_media_bytes_verified": output_media_checked,
        "local_references": local_references, "unique_local_targets": len(seen_refs),
        "broken_links": missing_links, "broken_fragments": bad_fragments,
        "failures": failures, "seconds": round(time.perf_counter() - start, 3),
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("themes", nargs="*", choices=THEMES)
    parser.add_argument("--skip-source", action="store_true")
    args = parser.parse_args()
    baseline = json.loads((ROOT / "reports" / "source-sha256.json").read_text())
    if not args.skip_source:
        print("Original source files hash-verified:", verify_source(baseline), flush=True)
    target = ROOT / "reports" / "content-results.json"
    results = json.loads(target.read_text()) if target.exists() else {}
    for theme in args.themes or THEMES:
        result = test_site(theme, baseline)
        results[theme] = result
        target.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
        print(theme, json.dumps({k: result[k] for k in ["passed", "source_pages", "media_bytes_verified", "published_media_bytes_verified", "local_references", "seconds"]}), flush=True)
        print("broken links:", len(result["broken_links"]), "broken fragments:", len(result["broken_fragments"]), "other failures:", len(result["failures"]), flush=True)
    raise SystemExit(any(not results[t]["passed"] for t in args.themes or THEMES))
