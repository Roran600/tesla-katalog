#!/usr/bin/env python3
"""Start and health-check four persistent Hugo development servers."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
PORTS = {"relearn": 1411, "book": 1412, "hextra": 1413, "hudocs": 1414}


def request(port):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2) as response:
            return response.status, response.read(500_000).decode("utf-8", "replace")
    except Exception:
        return None, ""


def existing_hugo_server(theme):
    expected = (ROOT / theme).resolve()
    proc = Path("/proc")
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        try:
            cwd = (entry / "cwd").resolve()
            args = shlex.split((entry / "cmdline").read_bytes().replace(b"\0", b" ").decode("utf-8", "replace"))
        except (OSError, ValueError):
            continue
        if cwd == expected and "server" in args:
            return int(entry.name)
    return None


def start():
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    pids = {}
    for theme, port in PORTS.items():
        status, body = request(port)
        if status == 200 and "Tesla" in body:
            pids[theme] = "already running"
            print(theme, "already serving", f"http://localhost:{port}/", flush=True)
            continue
        if status is not None:
            # The earlier Hugo startup may still be rendering its first full site.
            # Reuse it and wait for a catalog response; never kill another process.
            pids[theme] = "waiting for existing server"
            print(theme, "port already responds; waiting without replacing its process", flush=True)
            continue
        old_server = existing_hugo_server(theme)
        if old_server:
            pids[theme] = old_server
            print(theme, "existing Hugo server is still building", f"pid={old_server}", flush=True)
            continue
        log = (reports / f"serve-{theme}.log").open("a", encoding="utf-8")
        command = ["bash", str(ROOT / "hugo.sh"), theme, "serve", "--port", str(port), "--bind", "127.0.0.1", "--liveReloadPort", str(port + 1000)]
        environment = os.environ.copy()
        process = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, start_new_session=True, env=environment)
        (reports / f"serve-{theme}.pid").write_text(str(process.pid) + "\n")
        pids[theme] = process.pid
        print(theme, "starting", f"pid={process.pid}", f"http://localhost:{port}/", flush=True)
    (reports / "server-pids.json").write_text(json.dumps(pids, indent=2) + "\n")
    deadline = time.time() + 600
    ready, last = set(), {}
    while len(ready) < len(PORTS):
        if time.time() > deadline:
            raise TimeoutError(f"Hugo servers did not become ready: {last}")
        for theme, port in PORTS.items():
            if theme in ready:
                continue
            status, body = request(port)
            if status == 200 and "Tesla" in body:
                ready.add(theme)
                print(theme, "ready", f"http://localhost:{port}/", flush=True)
            else:
                log_path = reports / f"serve-{theme}.log"
                last[theme] = log_path.read_text(encoding="utf-8", errors="replace")[-1500:] if log_path.exists() else f"HTTP {status}"
        if len(ready) < len(PORTS):
            time.sleep(3)
    print("All four Hugo development servers are returning HTTP 200.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "start":
        raise SystemExit("Usage: python3 servers.py start")
    start()
