---
title: "An app that looks fine but its buttons do nothing"
description: "The page painted but no JavaScript ran: how to spot a script request that the server answered with an HTML page, and how to fix the rule that caused it."
category: Guides
tags: [hosting]
order: 3
checked: 2026-11-06
---

<!-- NAV:START -->
[Home](README.md) › [Guides](Category-Guides.md) · Tags: [hosting](Tag-hosting.md)
<!-- NAV:END -->

# An app that looks fine but its buttons do nothing

**A page that renders but whose buttons, sliders and links do nothing is usually a page whose JavaScript never ran.** The HTML was already on the page — pre-rendered at build time or server-rendered — so it looks complete. The script that makes it interactive was not loaded, or was loaded as the wrong kind of file.

## What it looks like

- The layout, text and images are all there.
- Clicking a button does nothing: no navigation, no spinner, no error dialog.
- Controls that the browser itself draws, like a slider, may still move — but nothing else on the page reacts.
- The browser console shows a syntax error, and the token it complains about is `<`.
- The Network tab shows the main script request answered with an HTML page instead of a script.

## 1. Read the console first

Open the browser's developer tools and look at the console. "Unexpected token" is the parser saying it met something it cannot read at that position ([MDN: SyntaxError: Unexpected token](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Unexpected_token), checked 2026-11-06). When the first character of the file is `<`, the browser was handed an HTML document where it expected JavaScript — for example the site's 404 page or the home page.

**The error names the script, not the bug.** The bug is on the server, in whatever answered that request.

## 2. Ask the server what it returned for the script

Take the script's URL from the error or from the Network tab, then request it directly:

```sh
curl -I https://example.com/assets/app-abc123.js
```

Read two things in the response:

- **Status.** A `200` is what you want. A `301`, `302` or `307` means some rule is sending the file request somewhere else.
- **Content-Type.** For a `.js` file it should be a JavaScript type; the common types table on MDN lists `text/javascript` ([MDN: Common MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types), checked 2026-11-06). A Content-Type of `text/html` confirms the server answered with a page.

If the response has `X-Content-Type-Options: nosniff`, a script served with an HTML type is blocked before it is even parsed; without that header the browser tries to parse the HTML as JavaScript and fails at the first character ([MDN: X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options), checked 2026-11-06).

## 3. Find the rule that did it

The usual causes, in order of how often they turn up:

1. **A single-page-app fallback.** Every path the static server cannot find is answered with `index.html`. That is right for page URLs such as `/plans` and wrong for `/assets/app-abc123.js`.
2. **A redirect for old or moved pages.** A rule written for a page path that no longer exists can match a folder of the same name. A rule for `/assets` or `/static` then catches every file under it.
3. **The file is simply missing from the host,** and the fallback from point 1 hides the miss behind a `200` page.

Match rules against the whole path, not just the first segment: `/assets/app.js` is both "under `/assets`" and "a file", and the second fact must win.

## 4. Fix it at the server, not in the app

- **Serve real files before any fallback.** Check the disk (or object storage) first, and only rewrite to `index.html` when nothing was found.
- **Only rewrite page URLs.** Skip any request whose last path segment contains a dot, since that is a file request, not a page.
- **Never redirect a file request to an HTML page.** If a redirect list is meant for retired pages, apply it only to requests that look like pages.

The same rule applies in reverse proxies, CDN rules and serverless rewrites: the asset path has to be excluded from the catch-all before it is excluded from anything else.

## 5. Check that it is fixed

- `curl -I` on the script returns `200` and a JavaScript Content-Type.
- The console is clean on a hard reload (bypass the cache).
- The buttons, forms and other controls respond.

## Why the page looked fine all along

Pre-rendering — turning each page into static HTML at build time — is there for speed and for search engines, and it does its job even when the JavaScript is broken. The markup arrives complete, so the page paints. Only interaction shows the difference.

Pre-rendered markup can also show browser defaults where an app value belongs. A range input with no `value` attribute shows the halfway point between its minimum and maximum ([MDN: `<input type="range">`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/range), checked 2026-11-06); a slider parked in the middle while the page around it says something else is a second clue that no script has run.

## Related pages

- [From idea to deployed AI app](Idea-to-deployed-AI-app.md#4-deploy): where the deploy and its checks fit
- [The cloud, for AI apps](Cloud-for-AI-apps.md): what the [host](Glossary.md#host) does with static files
- [Security for AI apps and agents](Security-for-AI-apps.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Host](Glossary.md#host), [Serverless](Glossary.md#serverless), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-06.

- MDN, [SyntaxError: Unexpected token](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Unexpected_token)
- MDN, [Common MIME types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types)
- MDN, [X-Content-Type-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options)
- MDN, [&lt;input type="range"&gt;](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/range)

---

First version written with AI assistance, from a deployment bug where a redirect rule for retired pages also matched the folder that holds the site's JavaScript, and checked against the [sources](#sources) on 2026-11-06. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
