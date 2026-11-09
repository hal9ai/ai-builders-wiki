---
title: "Where an AI app's terms of service and privacy policy should live"
description: "One canonical copy of each legal document, rendered as it is served: HTML for people and search, Markdown for agents, a last-known-good copy for outages."
category: Security and data
tags: [privacy, hosting]
order: 4
checked: 2026-11-06
---

<!-- NAV:START -->
[Home](README.md) › [Security and data](Category-Security-and-data.md) · Tags: [privacy](Tag-privacy.md), [hosting](Tag-hosting.md)
<!-- NAV:END -->

# Where an AI app's terms of service and privacy policy should live

**Keep one canonical copy of each legal document — the terms of service and the privacy policy — in the service that owns the facts they describe, and have every site that shows them render them from that copy.** Two copies always drift: the price changes in the code, the terms page still quotes the old one, and nobody notices until a customer quotes the page back at you.

**This is not legal advice.** This page covers where the documents live and how they are served, not what they should say. That question belongs to a lawyer.

## One copy, in the place that knows the facts

The terms describe the product: what it does, what it costs, what data it holds, who is responsible for what. The system that knows those facts is usually the backend — the [API](Glossary.md#api) server, the billing ledger, the database — and not the marketing site, which is normally a separate repository, deployed separately and edited by different people.

When the same document exists in both places, one of them is stale, and it is usually the one a lawyer is reading.

Put the document where the code it describes lives, in Markdown, at a predictable path (`terms.md`, `privacy.md`), in the same repository as that code. It can then change in the same pull request as the behavior it describes, and the record of who changed what is the repository's own [logs](Glossary.md#logs).

## Serve it two ways: a page for people, Markdown for agents

**The same source becomes an HTML page for people and search engines, and stays Markdown for programs.** Both are the same text; neither is a copy of the other.

- `GET /terms` — the page: title, "Last updated" date and the document's body, rendered from the Markdown as the page is served.
- `GET /terms.md` — the Markdown itself, as `text/markdown`, which is what an [agent](Glossary.md#agent) should fetch.
- In the page's `<head>`, a `<link rel="alternate" type="text/markdown" href="…/terms.md">` names the machine copy, so a tool that reads the HTML knows where it is.

Markdown matters for agents because it is plain text: an agent answering "how much do credits cost" reads it faster, and for fewer [tokens](Glossary.md#token), than it parses a styled page.

HTML matters because search engines index it. Google's list of the file types it can index names plain text (`.txt`) but not Markdown, so a legal page that should be findable needs an HTML version ([Google Search Central, file types indexable by Google](https://developers.google.com/search/docs/crawling-indexing/indexable-file-types), checked 2026-11-06).

If the site is served from more than one place — several datacenters, or a language mirror — give every copy the same canonical URL, on the one host you want in search results. Google calls `rel="canonical"` "a strong signal that the specified URL should become canonical" ([Google Search Central, consolidate duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls), checked 2026-11-06).

## Render at request time, without losing search or speed

The pattern that keeps one source and still serves a fast, indexable page has three parts:

1. **Prerender the page around the document.** At build time, render the site's own layout — header, footer, styles, navigation — with placeholders where the document's title, date and body go, plus an empty `<article>`. The shell is static, so every request shares its assets and layout.
2. **Fill it in as it is served.** The server fetches the canonical Markdown, renders it to HTML, and substitutes the title, date and body. The page cannot then show text that the canonical document no longer contains.
3. **Hand the same data to the browser.** Put the rendered document in a global (`window.__LEGAL_DOC__`) and have the page pick it up during hydration, so the browser-rendered page matches the HTML the server sent. For navigation inside the app, a small JSON endpoint (`/legal-docs/terms.json`) returns the same fields.

Cache the Markdown — an hour in memory is plenty — and keep the last good version on disk. When the source can't be reached, serve the copy and retry after a few minutes instead of holding the failure for the full hour. A deployment that has never fetched the document has nothing to fall back on; that is what a 502 and a message naming the document are for.

## Stand on its own

**The legal pages should be the last thing to break, not the first.** If they live inside the app whose data handling they describe, an outage, a bad [deploy](Glossary.md#deploy) or a billing problem takes them down with it — and `/terms` is exactly what a customer, a payment processor or a crawler looks for when something is wrong.

Serve them from whatever stays up: a static site, the account site, a CDN. Where the page has to fetch from a service that can fail, the last-known-good copy above is what makes that acceptable.

## Say when it changed

Every legal page shows a "Last updated" date, and the date belongs in the document itself — not only in the page's chrome — so the Markdown carries it too. Keep a short changelog of substantive changes: pricing, what data is collected, who it goes to, what rights a user has. "We may change these terms at any time" gives you the flexibility to change a price quietly, and costs you the trust that saying "we will tell you" earns.

## Write what the code actually does

The most common defect on a legal page is not a missing clause. It is a sentence copied from a template that the product does not do. "Credits expire after one year" — because the generator's template said so — is a promise, whether or not anyone could enforce it, and the ledger has never had an expiry.

When you find one, pick one:

- **Implement it**, if it is worth implementing.
- **State what happens, and promise notice.** That is accurate, so it stops being a promise you are breaking. Cloudish's terms, for example, now say credits do not currently expire, and that introducing expiry would come with at least 30 days' notice, applying only to credits added after the policy takes effect ([Cloudish, terms.md](https://cloudish.ai/terms.md?ref=cc-wiki), checked 2026-11-06).

Do not leave the unenforced claim in. It is the one sentence on the page a user can catch you on.

## Clauses an AI app needs that a plain website does not

Templates are written for websites selling subscriptions. An app that runs [models](Glossary.md#model) on users' [API keys](Glossary.md#api-key), and lets agents use them, describes a different relationship:

- **Who acts with a key.** Keys are handed to agents and applications, so "you are responsible for activity under your keys" has to continue "including actions taken by your agents and applications", or a user can reasonably say the agent did it, not them.
- **What the output is worth.** Say that model output can be wrong — [hallucinated](Glossary.md#hallucination) — that the user must check it, and who owns it.
- **Abuse.** AI apps get used to generate spam at scale and to attack other systems. A clause saying you may not host or distribute malware or attack other systems, and that you may suspend an account for it, is worth having before you need it.
- **Age.** Templates usually say 13, the US children's-privacy threshold, while a product sold with prepaid credits is meant for adults. Cloudish's terms and its privacy policy now both say 18, and say what happens if it learns otherwise. Whatever number you pick, the two documents should give the same one.
- **Money.** Prepaid credits need a price, what happens to unused ones, whether they are refundable, and what happens to them on termination.
- **Changes and termination.** What gets an account removed from the service, and how much notice a change to pricing, data handling or users' rights gets. Name the jurisdiction whose law governs the agreement.

## Check that it works

Four commands, against the deployed site:

```sh
# The page, as a browser and a crawler see it
curl -s https://www.example.com/terms | grep -o '<h1[^>]*>[^<]*</h1>'
curl -s https://www.example.com/terms | grep -c '%'   # no placeholders left behind

# The Markdown, as an agent sees it
curl -s https://www.example.com/terms.md | head -3

# The link to it, in the page head
curl -sI https://www.example.com/terms | grep -i '^link:'
```

Then break the source on purpose — stop the service, or point the fetch at a dead [host](Glossary.md#host) — and load `/terms` again. The last-known-good copy should still be served, and a document that was never fetched should fail with a message naming what could not be loaded, not a blank page.

## Checklist

- one canonical Markdown file per document, in the repository that owns the behavior
- `/{name}` as HTML and `/{name}.md` as Markdown, both served from that file
- a canonical URL and a `rel="alternate"` link to the Markdown in the page head
- the "Last updated" date in the document itself
- every promise in the document matching what the code does
- keys, agents, model output and abuse covered
- the legal pages still served when the service behind them is down

## Related pages

- [Data protection when you use AI](Data-protection.md): the questions a privacy policy answers
- [Data protection by vendor](Data-protection-by-vendor.md)
- [Security for AI apps and agents](Security-for-AI-apps.md)
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md#4-deploy): where the legal pages fit in a deploy
- [The cloud, for AI apps](Cloud-for-AI-apps.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [API key](Glossary.md#api-key), [Deploy](Glossary.md#deploy), [Host](Glossary.md#host), [Logs](Glossary.md#logs), [Model](Glossary.md#model), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-06.

- Google Search Central, [File types indexable by Google](https://developers.google.com/search/docs/crawling-indexing/indexable-file-types)
- Google Search Central, [Consolidate duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
- Cloudish, [terms.md](https://cloudish.ai/terms.md?ref=cc-wiki) and [privacy.md](https://cloudish.ai/privacy.md?ref=cc-wiki), the disclosed example's canonical copies

---

First version written with AI assistance, from a change made while building the Cloudish site, and checked against the [sources](#sources) on 2026-11-06. Not legal advice. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
