#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SITE="${1:-}"
ACTION="${2:-build}"
case "$SITE" in relearn|book|hextra|hudocs) ;; *) echo 'Použitie: ./hugo.sh {relearn|book|hextra|hudocs} {build|serve} [Hugo argumenty]' >&2; exit 2 ;; esac
case "$ACTION" in build|serve) ;; *) echo 'Akcia musí byť build alebo serve.' >&2; exit 2 ;; esac
if [[ $# -ge 2 ]]; then shift 2; else shift "$#"; fi
mkdir -p "$ROOT/.cache/tmp" "$ROOT/.cache/xdg" "$ROOT/.cache/go-build" "$ROOT/.cache/go-mod" "$ROOT/.cache/hugo/$SITE"
export TMPDIR="$ROOT/.cache/tmp"
export XDG_CACHE_HOME="$ROOT/.cache/xdg"
export GOCACHE="$ROOT/.cache/go-build"
export GOMODCACHE="$ROOT/.cache/go-mod"
export GOTELEMETRY=off
if [[ ! -x "$ROOT/.bin/hugo" ]]; then python3 "$ROOT/setup_hugo.py"; fi
cd "$ROOT/$SITE"
if [[ "$ACTION" == serve ]]; then
  exec "$ROOT/.bin/hugo" server --cacheDir "$ROOT/.cache/hugo/$SITE" --disableFastRender "$@"
else
  exec "$ROOT/.bin/hugo" --cacheDir "$ROOT/.cache/hugo/$SITE" --printPathWarnings "$@"
fi
