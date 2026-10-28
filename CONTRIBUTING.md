# Contributing

Thank you for helping. Anyone can contribute: corrections, updates, new pages and translations. The wiki was started by the team behind Cloudish, at Hal9, who review pull requests; it gets better the more people write in it. Because it is only useful if it is correct, corrections always come first.

## Report a mistake

Open an issue. Please include:

- the page and the sentence that is wrong
- what is correct instead
- a link to an official source (the vendor's own docs, policy page or announcement), if there is one

If you are not sure something is wrong, open the issue anyway and say so.

## Propose a change

Pull requests are welcome: fixes, updated facts, new pages and translations. For a new page, check the index first so each question has one page; for a large rewrite, open an issue first so we can agree on scope.

## Work locally

1. Fork the repository on GitHub, clone your fork, and make a branch: `git switch -c fix-data-protection-table`.
2. Edit or add pages. Any Markdown editor works; links between pages are relative (`AI-agent.md`), so they also work in your editor's preview.
3. Rebuild the navigation and check every link: `python3 scripts/build_wiki.py` (Python 3, nothing to install).
4. Optional: see the wiki as a site, with the sidebar: `scripts/preview.sh`, then open `_preview/index.html` in a browser (needs [pandoc](https://pandoc.org/installing.html)).
5. Commit, push to your fork, and open a pull request. Say in it what you checked and where (links to the sources).

On every pull request, a check runs `scripts/build_wiki.py` and fails if a link is broken or the navigation wasn't rebuilt. A maintainer then reviews the facts against the sources and merges.

## Rules for pages

- **Main point first.** The first sentence of a page or section answers its question. Context and caveats come after.
- **Plain words.** Short paragraphs, examples, and the English tech terms people actually use (token, API key, logs, deploy).
- **Sources for vendor facts.** Every claim about a vendor or product links to that vendor's own page, with the date it was checked (`checked YYYY-MM-DD`). No source, no claim.
- **No invented numbers.** If a number is not on a source page, leave it out.
- **Vendor-neutral.** Cloudish (made by Hal9, which started this wiki) may appear as a disclosed example where relevant, never as a recommendation.
- **Nothing personal.** No names of individual people at Hal9 or elsewhere, except authors of cited work.

## Page template

Pages are Markdown files at the top level, named in wiki style: words separated by hyphens, first letter capital (`AI-agent.md`, `Data-protection-by-vendor.md`). Keep pages short and focused; when a topic grows, split it into linked pages.

Every page follows the same template:

```markdown
---
title: "What an AI agent is"
description: "One line for the index."
category: Agents
tags: [agents, basics]
order: 1
checked: 2026-10-28
---

<!-- NAV:START -->
<!-- NAV:END -->

# What an AI agent is

**One sentence that answers the question.** Context and caveats after.

(body)

## Related pages
## See also
<!-- SEEALSO:START -->
<!-- SEEALSO:END -->
## Sources
---
(footer: AI help and date with the sources link, how to report a mistake, licence)
```

Categories and tags are descriptive and will change. Reuse an existing one when it fits; add a new one when it does not. `order` sets the position within the category.

Link the first use of a glossary term to its entry in [Glossary.md](Glossary.md). After adding a page or changing front matter, rebuild the navigation (Home index, `_Sidebar.md`, category and tag pages, breadcrumbs, *See also*) and check links:

```sh
python3 scripts/build_wiki.py
```

`python3 scripts/build_wiki.py --link-terms` also links the first plain use of each glossary term; review its diff before committing.

## Licence

By contributing, you agree that your text is released under [CC BY 4.0](LICENSE). The build script is under the MIT licence (see its header).
