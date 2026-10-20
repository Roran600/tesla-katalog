#!/usr/bin/env python3
"""Install a pinned Hugo Extended binary below stranka/, not system-wide."""
import hashlib
import io
from pathlib import Path
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parent
VERSION = "0.168.0"
NAME = f"hugo_extended_{VERSION}_linux-amd64.tar.gz"
BASE = f"https://github.com/gohugoio/hugo/releases/download/v{VERSION}"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Tesla-catalog-test"})
    return urllib.request.urlopen(req, timeout=120).read()


if __name__ == "__main__":
    binary = ROOT / ".bin" / "hugo"
    if binary.exists():
        print(binary)
        raise SystemExit(0)
    checksums = fetch(f"{BASE}/hugo_{VERSION}_checksums.txt").decode()
    expected = next(line.split()[0] for line in checksums.splitlines() if line.split()[-1] == NAME)
    archive = fetch(f"{BASE}/{NAME}")
    actual = hashlib.sha256(archive).hexdigest()
    if actual != expected:
        raise RuntimeError("Hugo archive checksum mismatch")
    cache = ROOT / ".cache" / "downloads"
    cache.mkdir(parents=True, exist_ok=True)
    (cache / NAME).write_bytes(archive)
    (cache / f"hugo_{VERSION}_checksums.txt").write_text(checksums)
    binary.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as source:
        binary.write_bytes(source.extractfile("hugo").read())
    binary.chmod(0o755)
    print(f"Installed {binary} (verified SHA-256 {actual})")
