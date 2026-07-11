#!/usr/bin/env bash
set -euo pipefail

package="${ARIA_PACKAGE:-aria-cli}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

if ! command -v pipx >/dev/null 2>&1; then
  python3 -m pip install --user pipx
  python3 -m pipx ensurepath
fi

pipx install "$package"
echo "ARIA installed. Restart your shell if 'aria' is not on PATH yet."
