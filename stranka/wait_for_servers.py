#!/usr/bin/env python3
"""Wait for the four Hugo dev servers to finish their initial build and answer HTTP 200."""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORTS = {"relearn": 1411, "book": 1412, "hextra": 1413, "hudocs": 1414}
DEADLINE = time.time() + 1500  # 25 minutes


def probe(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as response:
            body = response.read(500_000).decode("utf-8", "replace")
            return response.status, body
    except Exception as error:
        return None, str(error)


ready = {}
while len(ready) < len(PORTS):
    if time.time() > DEADLINE:
        break
    for theme, port in PORTS.items():
        if theme in ready:
            continue
        status, body = probe(port)
        if status == 200 and "Tesla" in body:
            ready[theme] = {"port": port, "url": f"http://localhost:{port}/", "status": status}
            print(f"READY {theme} http://localhost:{port}/", flush=True)
    if len(ready) < len(PORTS):
        time.sleep(10)

result = {
    "ready": ready,
    "missing": [t for t in PORTS if t not in ready],
    "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
}
(ROOT / "reports" / "server-status.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
raise SystemExit(0 if not result["missing"] else 1)
