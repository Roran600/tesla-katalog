#!/usr/bin/env python3
"""Wait only for the Hextra dev server to finish its initial build."""
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 1413
DEADLINE = time.time() + 2700  # 45 more minutes

while time.time() < DEADLINE:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=5) as response:
            body = response.read(500_000).decode("utf-8", "replace")
            if response.status == 200 and "Tesla" in body:
                result = {"ready": {"hextra": {"port": PORT, "url": f"http://localhost:{PORT}/", "status": 200}},
                          "missing": [], "finished_at": time.strftime("%Y-%m-%d %H:%M:%S")}
                (ROOT / "reports" / "server-status.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
                print(f"READY hextra http://localhost:{PORT}/", flush=True)
                raise SystemExit(0)
    except Exception:
        pass
    time.sleep(15)

result = {"ready": {}, "missing": ["hextra"], "finished_at": time.strftime("%Y-%m-%d %H:%M:%S")}
(ROOT / "reports" / "server-status.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
raise SystemExit(1)
