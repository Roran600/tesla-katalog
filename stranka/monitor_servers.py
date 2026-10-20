#!/usr/bin/env python3
"""Monitor the four Hugo dev servers: HTTP readiness plus on-disk build progress."""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTS = {"relearn": 1411, "book": 1412, "hextra": 1413, "hudocs": 1414}
DEADLINE = time.time() + 2700  # 45 minutes
reports = ROOT / "reports"
reports.mkdir(exist_ok=True)
progress_log = reports / "server-progress.log"
status_file = reports / "server-status.json"


def probe(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=3) as response:
            body = response.read(500_000).decode("utf-8", "replace")
            return response.status, body
    except Exception as error:
        return None, type(error).__name__


def html_count(theme):
    public = ROOT / theme / "public"
    if not public.is_dir():
        return 0
    return sum(1 for _ in public.rglob("*.html"))


ready = {}
started = time.time()
last_snapshot = 0
with progress_log.open("w", encoding="utf-8") as log:
    while len(ready) < len(PORTS):
        if time.time() > DEADLINE:
            break
        snapshot = {"elapsed_seconds": round(time.time() - started), "html_files": {}, "http": {}}
        for theme, port in PORTS.items():
            status, body = probe(port)
            snapshot["http"][theme] = status
            snapshot["html_files"][theme] = html_count(theme)
            if theme not in ready and status == 200 and "Tesla" in body:
                ready[theme] = {"port": port, "url": f"http://localhost:{port}/", "status": status,
                                "after_seconds": round(time.time() - started)}
                print(f"READY {theme} http://localhost:{port}/ after {ready[theme]['after_seconds']}s", flush=True)
        log.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
        log.flush()
        last_snapshot = time.time()
        if len(ready) < len(PORTS):
            time.sleep(15)

result = {
    "ready": ready,
    "missing": [t for t in PORTS if t not in ready],
    "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "links": {t: f"http://localhost:{p}/" for t, p in PORTS.items()},
}
status_file.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
raise SystemExit(0 if not result["missing"] else 1)
