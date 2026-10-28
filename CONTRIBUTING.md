# Contributing

Thank you for helping. This wiki is only useful if it is correct, so corrections are the most valuable contribution.

## Report a mistake

Open an issue. Please include:

- the page and the sentence that is wrong
- what is correct instead
- a link to an official source (the vendor's own docs, policy page or announcement), if there is one

If you are not sure something is wrong, open the issue anyway and say so.

## Propose a change

Pull requests are welcome for small fixes. For a new page or a large rewrite, open an issue first so we can agree on scope.

## Rules for pages

- **Main point first.** The first sentence of a page or section answers its question. Context and caveats come after.
- **Plain words.** Short paragraphs, examples, and the English tech terms people actually use (token, API key, logs, deploy).
- **Sources for vendor facts.** Every claim about a vendor or product links to that vendor's own page, with the date it was checked (`checked YYYY-MM-DD`). No source, no claim.
- **No invented numbers.** If a number is not on a source page, leave it out.
- **Vendor-neutral.** Cloudish (run by Hal9, which makes this wiki) may appear as a disclosed example where relevant, never as a recommendation.
- **Nothing personal.** No names of individual people at Hal9 or elsewhere, except authors of cited work.

## Front matter

Each page in `pages/` starts with:

```yaml
---
title: "What an AI agent is"
category: Concepts
tags: [agents, tools]
checked: 2026-10-28
---
```

Categories and tags are descriptive and will change. Reuse an existing one when it fits; add a new one when it does not. After changing front matter, regenerate the index:

```sh
python3 scripts/build_index.py
```

## Licence

By contributing, you agree that your text is released under [CC BY 4.0](LICENSE). The index script is under the MIT licence (see its header).
