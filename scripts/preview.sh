#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Local HTML preview of the wiki (sidebar + page), written to _preview/ (git-ignored). Needs pandoc.
#   scripts/preview.sh && open _preview/index.html
set -e
src=$(cd "$(dirname "$0")/.." && pwd); out="$src/_preview"
rm -rf "$out"; mkdir -p "$out"
side=$(pandoc -f gfm -t html "$src/_Sidebar.md" | sed -E 's/href="([^":#]+)\.md(#[^"]*)?"/href="\1.html\2"/g')
for f in "$src"/*.md; do
  b=$(basename "$f" .md); [ "$b" = _Sidebar ] && continue; [ "$b" = README ] && n=index || n=$b
  body=$(pandoc -f gfm -t html "$f" | sed -E 's/href="([^":#]+)\.md(#[^"]*)?"/href="\1.html\2"/g; s/href="README\.html/href="index.html/g')
  cat > "$out/$n.html" <<HTML
<!doctype html><meta charset=utf-8><title>$b · AI Builders Wiki</title>
<style>body{margin:0;font:16px/1.6 system-ui;background:#0d1117;color:#e6edf3;display:flex}
nav{width:260px;padding:1em 1.5em;border-right:1px solid #30363d;height:100vh;position:sticky;top:0;overflow:auto;font-size:14px}
main{max-width:860px;padding:1em 2.5em}a{color:#58a6ff}table{border-collapse:collapse}td,th{border:1px solid #30363d;padding:4px 8px;vertical-align:top}
code{background:#161b22;padding:1px 4px;border-radius:4px}pre{background:#161b22;padding:1em;overflow:auto}</style>
<nav>$(echo "$side" | sed 's/href="README\.html/href="index.html/g')</nav><main>$body</main>
HTML
done
echo "$(ls "$out" | wc -l) pages in $out"
