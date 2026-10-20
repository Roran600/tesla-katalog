#!/usr/bin/env python3
"""Build each complete website independently and retain commands, logs and timings."""
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent
THEMES = ("relearn", "book", "hextra", "hudocs")


if __name__ == "__main__":
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    results = {}
    for theme in THEMES:
        started = time.perf_counter()
        destination = ROOT / "reports" / "builds" / theme
        command = ["bash", str(ROOT / "hugo.sh"), theme, "build", "--destination", str(destination)]
        environment = os.environ.copy()
        environment["GOMEMLIMIT"] = "3GiB"
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True)
        elapsed = time.perf_counter() - started
        log = result.stdout + result.stderr
        (reports / f"build-{theme}.log").write_text(log, encoding="utf-8")
        results[theme] = {
            "exit_code": result.returncode,
            "seconds": round(elapsed, 3),
            "command": f"bash ./hugo.sh {theme} build --destination reports/builds/{theme}",
            "hugo": subprocess.check_output([str(ROOT / ".bin" / "hugo"), "version"], text=True).strip(),
            "warnings": [line for line in log.splitlines() if line.startswith("WARN")],
            "errors": [line for line in log.splitlines() if line.startswith("ERROR")],
            "html_files": sum(1 for _ in destination.rglob("*.html")),
            "upstream": json.loads((ROOT / theme / "themes" / "upstream.json").read_text()),
        }
        (reports / "build-results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
        print(theme, f"exit={result.returncode}", f"seconds={elapsed:.2f}", flush=True)
        print("\n".join(log.splitlines()[-18:]), flush=True)
    raise SystemExit(any(item["exit_code"] for item in results.values()))
