#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Build the static HTML site into _site/ for GitHub Pages.

Reuses build_wiki's front-matter parser and category constants so the sidebar
matches _Sidebar.md. Converts every Markdown page with pandoc (GFM), rewrites
internal .md links to .html, and wraps each page in site/template.html with the
generated sidebar and site/style.css.
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


def html_href(md_name: str) -> str:
    """X.md -> X.html (README.md -> index.html)."""
    if md_name == HOME:
        return "index.html"
    return md_name[:-3] + ".html"


def rewrite_links(h: str) -> str:
    h = re.sub(r'href="([^":#]+)\.md(#[^"]*)?"', r'href="\1.html\2"', h)
    return h.replace('href="README.html', 'href="index.html')


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


def sidebar_html(pages) -> str:
    by_cat = {}
    for m in pages:
        by_cat.setdefault(m["category"], []).append(m)
    cats = [c for c in CATEGORY_ORDER if c in by_cat]
    cats += sorted(c for c in by_cat if c not in CATEGORY_ORDER)

    parts = [
        f'<div class="brand"><a href="index.html">{html.escape(WIKI_TITLE)}</a></div>',
        '<nav class="sidenav">',
        '<div class="nav-top">'
        '<a href="index.html">Home</a>'
        '<a href="Glossary.html">Glossary</a>'
        '<a href="Tags.html">Tags</a>'
        '</div>',
    ]
    for c in cats:
        parts.append(f'<a class="nav-cat" href="{html_href(cat_file(c))}">{html.escape(c)}</a>')
        for m in by_cat[c]:
            parts.append(f'<a class="nav-page" href="{html_href(m["file"])}">{html.escape(m["title"])}</a>')
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
    sidebar = sidebar_html(content_pages())

    n = 0
    for f in sorted(ROOT.glob("*.md")):
        if f.name == "_Sidebar.md":
            continue
        md = f.read_text(encoding="utf-8")
        title = title_of(md)
        body = mark_breadcrumb(rewrite_links(pandoc(strip_front_matter(md))))
        full_title = title if title == WIKI_TITLE else f"{title} · {WIKI_TITLE}"
        page = (template
                .replace("{{TITLE}}", html.escape(full_title))
                .replace("{{SIDEBAR}}", sidebar)
                .replace("{{CONTENT}}", body))
        (OUT / html_href(f.name)).write_text(page, encoding="utf-8")
        n += 1
    print(f"{n} pages in {OUT}")


if __name__ == "__main__":
    main()
