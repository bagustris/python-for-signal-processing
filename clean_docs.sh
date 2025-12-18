#!/usr/bin/env bash
set -euo pipefail

# Remove all contents of docs/ (including dotfiles) but keep the docs/ directory.
# Usage:
#   ./clean_docs.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$ROOT_DIR/docs"

mkdir -p "$DOCS_DIR"

# Safety checks
if [[ "$DOCS_DIR" != "$ROOT_DIR/docs" ]]; then
  echo "Refusing to operate: unexpected docs dir '$DOCS_DIR'" >&2
  exit 1
fi

# Delete everything inside docs/, but not the directory itself
find "$DOCS_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +

echo "OK: cleaned contents of docs/"
