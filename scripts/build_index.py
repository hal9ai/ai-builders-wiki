#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Rebuild the generated part of README.md from the front matter in pages/*.md.

Only the text between the INDEX:START and INDEX:END markers is replaced.
Also checks that every relative link in pages/ and README.md points to an
existing file (and, for #anchors, an existing heading). Exits 1 on a broken link.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "pages"
README = ROOT / "README.md"
START, END = "<!-- INDEX:START -->", "<!-- INDEX:END -->"


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            value = [v.strip().strip('"') for v in value[1:-1].split(",") if v.strip()]
        else:
            value = value.strip('"')
        meta[key.strip()] = value
    return meta


def slugify(heading):
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)
    return s.replace(" ", "-")


def anchors(path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return {slugify(h) for h in re.findall(r"^#{1,6} (.+)$", text, re.M)}


def check_links(files):
    broken = []
    for f in files:
        text = re.sub(r"```.*?```", "", f.read_text(encoding="utf-8"), flags=re.S)
        for target in re.findall(r"\]\(([^)\s]+)\)", text):
            if re.match(r"^[a-z]+:", target):
                continue
            path, _, anchor = target.partition("#")
            dest = (f.parent / path).resolve() if path else f
            if not dest.exists():
                broken.append(f"{f.relative_to(ROOT)} -> {target}")
            elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
                broken.append(f"{f.relative_to(ROOT)} -> {target} (no such heading)")
    return broken


def main():
    pages = []
    for p in sorted(PAGES.glob("*.md")):
        meta = front_matter(p.read_text(encoding="utf-8"))
        meta["path"] = f"pages/{p.name}"
        pages.append(meta)

    by_cat = defaultdict(list)
    by_tag = defaultdict(list)
    for meta in pages:
        by_cat[meta.get("category", "Uncategorized")].append(meta)
        for tag in meta.get("tags", []):
            by_tag[tag].append(meta)

    out = ["## Pages by category", ""]
    for cat in sorted(by_cat):
        out += [f"### {cat}", ""]
        for meta in by_cat[cat]:
            desc = f": {meta['description']}" if meta.get("description") else ""
            out.append(f"- [{meta['title']}]({meta['path']}){desc}")
        out.append("")
    out += ["## Tags", ""]
    for tag in sorted(by_tag):
        links = ", ".join(f"[{m['title']}]({m['path']})" for m in by_tag[tag])
        out.append(f"- **{tag}**: {links}")
    out.append("")
    generated = "\n".join(out)

    readme = README.read_text(encoding="utf-8")
    if START not in readme or END not in readme:
        sys.exit("README.md has no INDEX markers")
    head, rest = readme.split(START, 1)
    _, tail = rest.split(END, 1)
    README.write_text(f"{head}{START}\n\n{generated}\n{END}{tail}", encoding="utf-8")
    print(f"Indexed {len(pages)} pages, {len(by_cat)} categories, {len(by_tag)} tags.")

    broken = check_links([README, ROOT / "CONTRIBUTING.md", *sorted(PAGES.glob("*.md"))])
    if broken:
        print("Broken relative links:")
        print("\n".join(f"  {b}" for b in broken))
        sys.exit(1)
    print("All relative links resolve.")


if __name__ == "__main__":
    main()
