#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Build the static site into _site/ for local preview (needs pandoc).
# Routes are directories, so serve the folder rather than opening a file:
#   scripts/preview.sh
#   python3 -m http.server 8000 -d _site
#   open http://localhost:8000/
set -e
cd "$(dirname "$0")/.."
python3 scripts/build_site.py
python3 scripts/check_routes.py
echo "serve: python3 -m http.server 8000 -d _site"
echo "open:  http://localhost:8000/"
