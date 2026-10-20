#!/usr/bin/env python3
"""Time-box a disposable Hugo build and save goroutine stacks if it stalls."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parent


def run(theme, timeout, probe=False):
    target = ROOT / "reports" / "diagnostics" / (theme + ("-probe" if probe else ""))
    target.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    for key, relative in {
        "TMPDIR": ".cache/tmp", "XDG_CACHE_HOME": ".cache/xdg",
        "GOCACHE": ".cache/go-build", "GOMODCACHE": ".cache/go-mod",
    }.items():
        path = ROOT / relative
        path.mkdir(parents=True, exist_ok=True)
        environment[key] = str(path)
    environment.update(GOTELEMETRY="off", GOMEMLIMIT="3GiB", HUGO_RESOURCEDIR=str(target / "resources"))
    command = [str(ROOT / ".bin/hugo"), "--source", str(ROOT / theme),
               "--destination", str(target / "public"), "--cacheDir", str(target / "cache"),
               "--logLevel", "debug", "--noBuildLock"]
    if probe:
        overlay = target / "probe.toml"
        overlay.write_text('''[[segments.probe.includes]]
kind = "home"
[[segments.probe.includes]]
path = "/docs/integrovane-obvody/ma0403"
[params.search.index]
disable = true
[params.search.page]
disable = true
''')
        command += ["--config", str(ROOT / theme / "hugo.toml") + "," + str(overlay), "--renderSegments", "probe", "--templateMetrics"]
    started = time.monotonic()
    expired = False
    with (target / "build.log").open("w") as output:
        process = subprocess.Popen(command, env=environment, stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            expired = True
            # SIGQUIT targets only the disposable process created above, not a user's server.
            process.send_signal(signal.SIGQUIT)
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
    result = {"theme": theme, "timed_out": expired, "seconds": round(time.monotonic() - started, 3), "exit_code": process.returncode}
    (target / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)
    print("Log:", target / "build.log", flush=True)
    for line in (target / "build.log").read_text(errors="replace").splitlines()[:12]:
        print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("theme", choices=["relearn", "book", "hextra", "hudocs"])
    parser.add_argument("--timeout", type=float, default=8)
    parser.add_argument("--probe", action="store_true")
    arguments = parser.parse_args()
    run(arguments.theme, arguments.timeout, arguments.probe)
