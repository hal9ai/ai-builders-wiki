#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Fail if the built site has a route that is not lowercase.

The site is published to GitHub Pages as <slug>/index.html directories, so
routes look like /security-for-ai-apps (GitHub Pages redirects /slug to
/slug/). Page routes come from the Markdown filenames, which are Title-Case on
the wiki, so build_site.py lowercases them. This check runs on the output,
after the build, and fails the deploy if any route is not lowercase, if two
pages collide once case is ignored, or if a page links to a route that is
missing.

    python3 scripts/build_site.py && python3 scripts/check_routes.py
"""
import posixpath
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
HREF = re.compile(r'href="([^":#?]+)')


def route_of(page: Path, target: str):
    """The route a relative href points at, or None if it is not a route."""
    if not target.endswith("/"):
        return None
    path = posixpath.normpath(posixpath.join(page.parent.as_posix(), target))
    return "" if path in (".", "") else path


def main():
    if not OUT.is_dir():
        print(f"{OUT} not found; run scripts/build_site.py first", file=sys.stderr)
        return 1

    files = sorted(p.relative_to(OUT) for p in OUT.rglob("*") if p.is_file())
    problems = []

    seen = {}
    for rel in files:
        route = str(rel)
        if route != route.lower():
            problems.append(f"route is not lowercase: {route}")
        key = route.lower()
        if key in seen:
            problems.append(f"routes collide when case is ignored: {seen[key]} and {route}")
        else:
            seen[key] = route

    for rel in files:
        if rel.name != "index.html":
            continue
        targets = set(HREF.findall((OUT / rel).read_text(encoding="utf-8")))
        for target in sorted(targets):
            path = route_of(rel, target)
            if path is None:
                continue
            if target != target.lower():
                problems.append(f"{rel} links to a route that is not lowercase: {target}")
            if path.startswith(".."):
                problems.append(f"{rel} links outside the site: {target}")
                continue
            dest = OUT / "index.html" if path == "" else OUT / path / "index.html"
            if not dest.is_file():
                problems.append(f"{rel} links to a missing route: {target}")

    if problems:
        print("Route check failed:", file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    pages = sum(1 for rel in files if rel.name == "index.html")
    print(f"{len(files)} files, {pages} routes, all lowercase.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
