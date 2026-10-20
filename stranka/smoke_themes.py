#!/usr/bin/env python3
"""Compare theme/configuration compatibility on a tiny disposable site."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
THEMES = ("relearn", "book", "hextra", "hudocs")


def run(theme):
    site = ROOT / "reports" / "diagnostics" / "smoke" / theme
    site.mkdir(parents=True, exist_ok=True)
    content = site / "content"
    docs = content / "docs"
    sample = docs / "sample"
    sample.mkdir(parents=True, exist_ok=True)
    (content / "_index.md").write_text('---\ntitle: Tesla test\n---\n\n[Catalog](/docs/)\n')
    (docs / "_index.md").write_text('---\ntitle: Catalog\ntype: docs\n---\n\n[Sample](/docs/sample/)\n')
    (sample / "index.md").write_text('---\ntitle: MA0403\ntype: docs\n---\n\nMA0403 test\n\n[Catalog](/docs/)\n')
    # Exactly the actual project configuration, with only the theme location changed.
    config = (ROOT / theme / "hugo.toml").read_text()
    config = f'themesDir = "{ROOT / theme / "themes"}"\n' + config
    (site / "hugo.toml").write_text(config)
    environment = os.environ.copy()
    for key, directory in {"TMPDIR":ROOT/".cache/tmp", "XDG_CACHE_HOME":ROOT/".cache/xdg", "GOCACHE":ROOT/".cache/go-build", "GOMODCACHE":ROOT/".cache/go-mod", "HUGO_RESOURCEDIR":site/"resources"}.items():
        directory.mkdir(parents=True, exist_ok=True)
        environment[key] = str(directory)
    environment["GOTELEMETRY"] = "off"
    command = [str(ROOT / ".bin/hugo"), "--source", str(site), "--cacheDir", str(ROOT / ".cache/hugo" / theme), "--templateMetrics", "--noBuildLock"]
    start = time.monotonic()
    try:
        result = subprocess.run(command, env=environment, capture_output=True, text=True, timeout=6)
        log = result.stdout + result.stderr
        info = {"exit_code":result.returncode, "seconds":round(time.monotonic()-start,3), "timed_out":False}
    except subprocess.TimeoutExpired as error:
        log = (error.stdout or b"").decode() + (error.stderr or b"").decode()
        info = {"exit_code":None, "seconds":round(time.monotonic()-start,3), "timed_out":True}
    (site / "build.log").write_text(log)
    return theme, info


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = dict(pool.map(run, THEMES))
    (ROOT / "reports/diagnostics/smoke-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
