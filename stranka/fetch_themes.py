#!/usr/bin/env python3
"""Download pinned upstream theme snapshots, writing only below this directory."""
import concurrent.futures
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import urllib.request

ROOT = Path(__file__).resolve().parent
REPOS = {
    "relearn": "McShelby/hugo-theme-relearn",
    "book": "alex-shpak/hugo-book",
    "hextra": "imfing/hextra",
    "hudocs": "zkreations/hudocs",
}


def download(item):
    name, repo = item
    destination = ROOT / name / "themes" / name
    metadata = destination.parent / "upstream.json"
    incomplete = destination.parent / f".{name}-extracting"
    if metadata.exists():
        return name, json.loads(metadata.read_text())
    if destination.exists():
        # Resume only an extraction explicitly marked by this script.
        if not incomplete.exists() or incomplete.read_text() != str(destination):
            raise RuntimeError(f"Refusing to overwrite existing theme: {destination}")
        shutil.rmtree(destination)
    sha = subprocess.check_output(
        ["git", "ls-remote", f"https://github.com/{repo}.git", "HEAD"], text=True
    ).split()[0]
    archive_url = f"https://codeload.github.com/{repo}/tar.gz/{sha}"
    request = urllib.request.Request(archive_url, headers={"User-Agent": "Tesla-catalog-theme-test"})
    data = urllib.request.urlopen(request, timeout=120).read()
    cache = ROOT / ".cache" / "downloads"
    cache.mkdir(parents=True, exist_ok=True)
    (cache / f"{name}-{sha}.tar.gz").write_bytes(data)
    destination.parent.mkdir(parents=True, exist_ok=True)
    incomplete.write_text(str(destination))
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        for member in archive.getmembers():
            relative = Path(*Path(member.name).parts[1:])
            if not relative.parts:
                continue
            target = (destination / relative).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise RuntimeError("Unsafe archive member")
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())
            elif member.issym():
                link_target = Path(member.linkname)
                if link_target.is_absolute() or not (target.parent / link_target).resolve().is_relative_to(destination.resolve()):
                    raise RuntimeError(f"Unsafe archive symlink: {member.name} -> {member.linkname}")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(member.linkname)
            elif member.islnk():
                link_relative = Path(*Path(member.linkname).parts[1:])
                linked = (destination / link_relative).resolve()
                if not linked.is_relative_to(destination.resolve()) or not linked.is_file():
                    raise RuntimeError(f"Unsafe archive hardlink: {member.name} -> {member.linkname}")
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(linked, target)
            else:
                raise RuntimeError(f"Unsupported archive member: {member.name}")
    info = {"repository": f"https://github.com/{repo}", "commit": sha, "archive": archive_url}
    metadata.write_text(json.dumps(info, indent=2) + "\n")
    incomplete.unlink()
    return name, info


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for name, info in executor.map(download, REPOS.items()):
            print(name, info["commit"], flush=True)
