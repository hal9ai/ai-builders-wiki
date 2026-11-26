#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the static HTML site into _site/ for GitHub Pages.

Every page is written as <slug>/index.html (README.md becomes index.html), so
URLs carry no .html extension and are lowercase: /security-for-ai-apps.
Reuses build_wiki's front-matter parser and category constants so the sidebar
matches _Sidebar.md, converts every Markdown page with pandoc (GFM), rewrites
internal .md links to routes, and wraps each page in site/template.html with
the generated sidebar and site/style.css.

Links and the stylesheet are relative (../ for a page one directory down), so
the site works at the domain root and under a path prefix.
"""
import html
import re
import shutil
import subprocess
from pathlib import Path

from build_wiki import CATEGORY_ORDER, cat_file, front_matter

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
OUT = ROOT / "_site"
HOME = "README.md"
WIKI_TITLE = "AI Builders Wiki"


def pandoc(md: str) -> str:
    return subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout


def strip_front_matter(md: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", md, count=1, flags=re.S)


def page_slug(md_name: str) -> str:
    """X.md -> x; README.md -> "" (the site root). Routes are lowercase."""
    if md_name == HOME:
        return ""
    return md_name[:-3].lower()


def output_path(md_name: str) -> Path:
    """Where a page is written: index.html, or <slug>/index.html."""
    slug = page_slug(md_name)
    return Path(slug) / "index.html" if slug else Path("index.html")


def href(depth: int, md_name: str) -> str:
    """Relative link to a page from a page `depth` directories below the root."""
    up = "../" * depth
    slug = page_slug(md_name)
    if not slug:
        return up or "./"
    return f"{up}{slug}/"


def rewrite_links(h: str, depth: int) -> str:
    def repl(m):
        name, anchor = m.group(1), m.group(2) or ""
        # _Sidebar.md has no page of its own; "all pages" means the Home index.
        target = HOME if name.lower() in ("readme", "_sidebar") else f"{name}.md"
        return f'href="{href(depth, target)}{anchor}"'

    # Leave code samples alone: a URL written inside backticks is an example,
    # not a link the page should follow.
    parts = re.split(r"(<pre\b[^>]*>.*?</pre>|<code\b[^>]*>.*?</code>)", h, flags=re.S)
    for i, part in enumerate(parts):
        if i % 2 == 0:
            parts[i] = re.sub(r'href="([^":#]+)\.md(#[^"]*)?"', repl, part)
    return "".join(parts)


def title_of(md: str) -> str:
    m = re.search(r'^title:\s*"?([^"\n]+)"?\s*$', md, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else WIKI_TITLE


def content_pages():
    pages = []
    for p in sorted(ROOT.glob("*.md")):
        meta = front_matter(p.read_text(encoding="utf-8"))
        if meta.get("category"):
            meta["file"] = p.name
            pages.append(meta)
    pages.sort(key=lambda m: (int(m.get("order", 99)), m["title"]))
    return pages


def sidebar_html(pages, depth: int) -> str:
    by_cat = {}
    for m in pages:
        by_cat.setdefault(m["category"], []).append(m)
    cats = [c for c in CATEGORY_ORDER if c in by_cat]
    cats += sorted(c for c in by_cat if c not in CATEGORY_ORDER)

    parts = [
        f'<div class="brand"><a href="{href(depth, HOME)}">{html.escape(WIKI_TITLE)}</a></div>',
        '<nav class="sidenav">',
        '<div class="nav-top">'
        f'<a href="{href(depth, HOME)}">Home</a>'
        f'<a href="{href(depth, "Glossary.md")}">Glossary</a>'
        f'<a href="{href(depth, "Tags.md")}">Tags</a>'
        '</div>',
    ]
    for c in cats:
        parts.append(f'<a class="nav-cat" href="{href(depth, cat_file(c))}">{html.escape(c)}</a>')
        for m in by_cat[c]:
            parts.append(f'<a class="nav-page" href="{href(depth, m["file"])}">{html.escape(m["title"])}</a>')
    parts.append("</nav>")
    return "\n".join(parts)


def mark_breadcrumb(h: str) -> str:
    def repl(m):
        p = m.group(0)
        return p.replace("<p>", '<p class="breadcrumb">', 1) if "›" in p else p
    return re.sub(r"<p>.*?</p>", repl, h, count=1, flags=re.S)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(SITE / "style.css", OUT / "style.css")

    template = (SITE / "template.html").read_text(encoding="utf-8")
    pages = content_pages()
    sidebars = {}

    n = 0
    routes = {}
    for f in sorted(ROOT.glob("*.md")):
        if f.name == "_Sidebar.md":
            continue
        out = output_path(f.name)
        if out in routes:
            raise SystemExit(
                f"route collision: {f.name} and {routes[out]} both build /{page_slug(f.name)}/. "
                "Rename one of them: routes are lowercase, so names may differ only by case."
            )
        routes[out] = f.name

        depth = len(out.parts) - 1
        if depth not in sidebars:
            sidebars[depth] = sidebar_html(pages, depth)
        md = f.read_text(encoding="utf-8")
        title = title_of(md)
        body = mark_breadcrumb(rewrite_links(pandoc(strip_front_matter(md)), depth))
        full_title = title if title == WIKI_TITLE else f"{title} · {WIKI_TITLE}"
        page = (template
                .replace("{{TITLE}}", html.escape(full_title))
                .replace("{{PREFIX}}", "../" * depth)
                .replace("{{SIDEBAR}}", sidebars[depth])
                .replace("{{CONTENT}}", body))
        (OUT / out).parent.mkdir(parents=True, exist_ok=True)
        (OUT / out).write_text(page, encoding="utf-8")
        n += 1
    print(f"{n} pages in {OUT}")


if __name__ == "__main__":
    main()
