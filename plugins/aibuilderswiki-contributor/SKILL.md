---
name: aibuilderswiki-contributor
description: Use after debugging a deploy, auth, DNS, storage, or hosting problem — or whenever a session surfaces a verifiable fact about building or deploying AI apps — to record it in the AI Builders Wiki (aibuilderswiki.com): fix a fact, add a page, or translate one, then open a pull request.
---

# Contributing to the AI Builders Wiki

The AI Builders Wiki (aibuilderswiki.com) is a vendor-neutral, CC-BY-4.0 wiki about building and deploying AI apps. Anyone can contribute: corrections, new pages, translations. It is only useful if it is correct, so corrections always come first.

You are helping someone contribute. Work through these steps and, at the end, hand them the pull-request URL.

## 1. Pick the change

- **Correction**: a sentence on a page is wrong. Include the page, the sentence, what is correct instead, and a link to an official source (the vendor's own docs, policy page or announcement).
- **New page**: a question with no page yet. Check the [Home index](README.md) first so each question has exactly one page.
- **Translation**: a page rendered in another language.

For a large rewrite, stop and open an issue first to agree on scope.

## 2. Follow the rules (every page)

- **Main point first.** The first sentence answers the page's question; context and caveats come after.
- **Plain words.** Short paragraphs, examples, and the English tech terms people actually use (token, API key, logs, deploy).
- **Sources for vendor facts.** Every claim about a vendor or product links to that vendor's own page, with the date it was checked (`checked YYYY-MM-DD`). No source, no claim.
- **No invented numbers.** If a number is not on a source page, leave it out.
- **Vendor-neutral.** Cloudish (made by Hal9, which started this wiki) may appear as a disclosed example where relevant, never as a recommendation.
- **AI help is fine, checking is yours.** You may draft with an AI assistant, but every claim is checked against its source. Say so in the pull request.
- **Nothing personal.** No names of individual people at Hal9 or elsewhere, except authors of cited work.

## 3. Use the page template

Pages are Markdown files at the repository root, named in wiki style: words separated by hyphens, first letter capital (`AI-agent.md`, `Data-protection-by-vendor.md`). Keep pages short and focused; when a topic grows, split it into linked pages.

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
(footer: how the page was written, when it was last checked against the sources, how to fix it, licence)
```

- Category is one of: **Foundations**, **Agents**, **Models and providers**, **Security and data**, **How-to**, **Problems & solutions**. Reuse an existing tag when one fits; add a new one only when none does. `order` sets the position within the category.
- Link the first use of a glossary term to its entry in [Glossary.md](Glossary.md).
- Leave the `NAV`, `SEEALSO`, and other generated blocks empty — the bot fills them after merge.

## 4. Work locally and check

1. Fork the repository on GitHub (`hal9ai/ai-builders-wiki`), clone your fork, and make a branch: `git switch -c fix-data-protection-table`.
2. Edit or add pages. Links between pages are relative (`AI-agent.md`), so they work in any editor's preview.
3. Check links: `python3 scripts/build_wiki.py`. Do **not** commit the regenerated navigation (`_Sidebar.md`, `Category-*.md`, `Tags.md`, `Tag-*.md`).
4. Commit, push to your fork, and open a pull request. In it, say what you checked and where (links to the sources).

A CI check runs the same build and fails on a broken link or on hand-edited navigation. After merge, a maintainer reviews the facts against the sources.

## 5. Hand over

Give the person the pull-request URL. That is the whole job.
