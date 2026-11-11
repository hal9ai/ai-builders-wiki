#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Build the static site into _site/ for local preview (needs pandoc).
#   scripts/preview.sh && open _site/index.html
set -e
cd "$(dirname "$0")/.."
python3 scripts/build_site.py
echo "open _site/index.html"
