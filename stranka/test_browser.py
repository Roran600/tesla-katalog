#!/usr/bin/env python3
"""Exercise stock theme UI, scans, PDFs and full-text search on desktop/mobile."""
import json
import os
from pathlib import Path
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
os.environ["TMPDIR"] = str(ROOT / ".cache" / "tmp")
os.environ["XDG_CACHE_HOME"] = str(ROOT / ".cache" / "xdg")
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(ROOT / ".cache" / "playwright")
for name in ("tmp", "xdg"):
    (ROOT / ".cache" / name).mkdir(parents=True, exist_ok=True)

from playwright.sync_api import sync_playwright

THEMES = ("relearn", "book", "hextra", "hudocs")
PORTS = {"relearn": 1411, "book": 1412, "hextra": 1413, "hudocs": 1414}


def details(page):
    return page.evaluate("""() => ({
      width: innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      h1: [...document.querySelectorAll('h1')].map(x => x.textContent.trim()),
      images: [...document.querySelectorAll('main img, article img, .article img')].map(x => ({
        src: x.currentSrc || x.src, loaded: x.complete && x.naturalWidth > 0,
        width: x.naturalWidth, alt: x.alt
      })),
      css: [...document.styleSheets].filter(x => x.href).length
    })""")


def test_theme(browser, theme, base):
    failures, js_errors, http_errors = [], [], []
    port = urlsplit(base).port
    output = ROOT / "reports" / "browser"
    output.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(viewport={"width": 1440, "height": 1000}, reduced_motion="reduce")
    page = context.new_page()
    page.set_default_timeout(30000)
    page.on("pageerror", lambda error: js_errors.append(str(error)))
    page.on("response", lambda response: http_errors.append({"url": response.url, "status": response.status}) if response.status >= 400 and urlsplit(response.url).port == port else None)

    routes = {
        "home": "/", "catalog": "/docs/", "category": "/docs/integrovane-obvody/",
        "component": "/docs/integrovane-obvody/ma0403/",
        "package": "/docs/integrovane-obvody/puzdra/io-13-c1/",
        "downloads": "/docs/ke-stazeni/",
    }
    desktop = {}
    for name, route in routes.items():
        response = page.goto(base + route, wait_until="networkidle", timeout=90000)
        if not response or response.status != 200:
            failures.append(f"{name}: expected HTTP 200")
        state = details(page)
        desktop[name] = state
        if state["documentWidth"] > state["width"] + 1:
            failures.append(f"{name}: desktop horizontal overflow")
        if not state["css"]:
            failures.append(f"{name}: theme CSS missing")
        if name == "component":
            if not page.get_by_role("heading", name="MA0403", exact=True).count():
                failures.append("Component heading missing")
            if not state["images"] or any(not image["loaded"] for image in state["images"]):
                failures.append("Component scan did not load")
            page.screenshot(path=str(output / f"{theme}-desktop.png"))
        elif name == "package":
            if not state["images"] or any(not image["loaded"] for image in state["images"]):
                failures.append("Package sheet did not load")
        elif name == "downloads":
            pdf = page.locator('a[href$="fonox.pdf"]').first
            if not pdf.count():
                failures.append("FONOX PDF link missing")
            else:
                url = pdf.evaluate("a => a.href")
                pdf_response = context.request.get(url)
                if pdf_response.status != 200 or not pdf_response.body().startswith(b"%PDF-"):
                    failures.append("FONOX PDF download is not a PDF")

    # Follow an actual catalog link, not only direct address navigation.
    page.goto(base + routes["category"], wait_until="networkidle")
    component_link = page.locator('main a, article a, .article a').filter(has_text="MA0403").first
    if component_link.count():
        component_link.click()
        page.wait_for_url("**/ma0403/")
    else:
        failures.append("Cannot navigate from category to MA0403")

    # Built-in search: initialize each stock theme's own dialog/input.
    page.goto(base + routes["component"], wait_until="networkidle")
    search = {"passed": False}
    try:
        if theme == "book":
            field = page.locator("#book-search-input")
            results = page.locator("#book-search-results a")
        elif theme == "hextra":
            page.locator("[data-search-open]").filter(visible=True).first.click()
            field = page.locator(".hextra-search-input")
            results = page.locator("#hextra-search-results a")
        elif theme == "hudocs":
            page.locator(".search-toggle").filter(visible=True).first.click()
            field = page.locator("#search-input")
            results = page.locator("#search-results a")
        else:
            field = page.locator("[data-search-input]").filter(visible=True).first
            results = page.locator("#R-searchresults a, .autocomplete-suggestion, .autocomplete-suggestions a")
        field.fill("MA0403")
        field.press("Enter") if theme == "relearn" else None
        page.wait_for_function("""() => {
          const containers = document.querySelectorAll('#book-search-results, #hextra-search-results, #search-results, #R-searchresults, .autocomplete-suggestions');
          return [...containers].some(x => x.innerText.includes('MA0403'));
        }""", timeout=60000)
        search = {"passed": True, "query": "MA0403", "url": page.url, "results": results.count()}
        page.screenshot(path=str(output / f"{theme}-search.png"))
    except Exception as error:
        search = {"passed": False, "query": "MA0403", "error": str(error)}
        failures.append("Built-in search: " + str(error).splitlines()[0])
        page.screenshot(path=str(output / f"{theme}-search-failure.png"))

    # Mobile page and the theme's menu affordance; do not replace the stock styling.
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(base + routes["component"], wait_until="networkidle")
    mobile = details(page)
    if mobile["documentWidth"] > mobile["width"] + 1:
        failures.append("Component: mobile horizontal overflow")
    if not mobile["images"] or any(not image["loaded"] for image in mobile["images"]):
        failures.append("Component: mobile scan missing")
    page.screenshot(path=str(output / f"{theme}-mobile.png"))
    mobile["buttons"] = page.locator("button, label[for]").evaluate_all("items => items.filter(x=>x.getBoundingClientRect().width>0 && x.getBoundingClientRect().height>0).map(x=>({tag:x.tagName, text:x.innerText, label:x.getAttribute('aria-label'), target:x.getAttribute('for'), class:x.className}))")
    # Test reports capture upstream errors rather than hiding them.
    if js_errors:
        failures.extend("JavaScript: " + error for error in sorted(set(js_errors)))
    if http_errors:
        failures.extend(f"HTTP {item['status']}: {item['url']}" for item in http_errors)
    context.close()
    return {"passed": not failures, "desktop": desktop, "mobile": mobile, "search": search, "js_errors": js_errors, "http_errors": http_errors, "failures": failures}


if __name__ == "__main__":
    target = ROOT / "reports" / "browser-results.json"
    results = {}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for theme in THEMES:
                start = time.perf_counter()
                base = f"http://127.0.0.1:{PORTS[theme]}"
                result = test_theme(browser, theme, base)
                result["seconds"] = round(time.perf_counter() - start, 3)
                results[theme] = result
                target.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
                print(theme, "passed=" + str(result["passed"]), "failures=" + str(result["failures"]), flush=True)
        finally:
            browser.close()
    raise SystemExit(any(not item["passed"] for item in results.values()))
