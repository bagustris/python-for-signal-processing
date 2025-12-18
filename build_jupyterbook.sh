#!/usr/bin/env bash
set -euo pipefail

# Build the root Jupyter Book and stage HTML into docs/.
# Usage:
#   ./build_jupyterbook.sh
#   ./build_jupyterbook.sh [extra jupyter-book build args]

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

JB_BIN=""
if [[ -x "$ROOT_DIR/.venv/bin/jupyter-book" ]]; then
  JB_BIN="$ROOT_DIR/.venv/bin/jupyter-book"
elif command -v jupyter-book >/dev/null 2>&1; then
  JB_BIN="jupyter-book"
else
  echo "Error: jupyter-book not found. Install deps into .venv first (e.g. 'uv venv .venv && uv pip install -r requirements.txt')." >&2
  exit 1
fi

EXTRA_ARGS=("$@")
if [[ ${1:-} == "--" ]]; then
  shift
  EXTRA_ARGS=("$@")
fi

"$JB_BIN" build . --path-output _build-jupyterbook "${EXTRA_ARGS[@]}"

rm -rf docs/*
mkdir -p docs
cp -a _build-jupyterbook/_build/html/. docs/
touch docs/.nojekyll

echo "OK: built site staged in docs/ (open docs/index.html)"
