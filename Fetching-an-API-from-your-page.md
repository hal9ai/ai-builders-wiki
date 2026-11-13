---
title: "Why a page can't read another site's API, and how to serve it from your own"
description: "A browser only lets a page read another origin's JSON when that server allows it with Access-Control-Allow-Origin; otherwise fetch the data on your own server and serve it from your own domain."
category: Problems & solutions
tags: [security, hosting]
order: 4
checked: 2026-11-12
---

<!-- NAV:START -->
[Home](README.md) › [Problems & solutions](Category-Problems-solutions.md) · Tags: [security](Tag-security.md), [hosting](Tag-hosting.md)
<!-- NAV:END -->

# Why a page can't read another site's API, and how to serve it from your own

**A browser only lets a page read a response from another origin when that server allows it with an `Access-Control-Allow-Origin` header; without the header, the page's code gets an error instead of the data, even when the request reached the server and it answered.** The fix is a small endpoint on your own server that fetches the data and returns it from your own domain, because a server is not bound by that rule.

This is the usual reason a page that shows live numbers — usage, prices, a dashboard — works in a tool like `curl` and shows nothing in the browser.

## How the block looks

- A `fetch()` call goes to `catch` with a `TypeError` ("Failed to fetch" in Chrome), and the console says something like *"blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource"*.
- The Network panel still shows the request, often with status 200: it was sent, and the browser threw the answer away instead of handing it to the page.
- `curl` on the very same URL returns the JSON, which makes the API look broken to nobody except the browser.
- Calling the same API from a page on the API's own domain works. The difference is not the page's code; it is where the page was loaded from.

## Why the browser does this

Code loaded from one origin may only read responses from other origins when those responses say so. As the CORS guide puts it: a web application "can only request resources from the same origin the application was loaded from unless the response from other origins includes the right CORS headers" ([MDN, CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS), checked 2026-11-12). An origin is the scheme, host and port together, so `https://app.example.com` and `https://api.example.com` are two origins even though the domain is the same.

The server opts in per response with one header:

- `Access-Control-Allow-Origin: https://app.example.com` — that one page may read it.
- `Access-Control-Allow-Origin: *` — any page may, but only for requests without credentials: a request that carries a cookie is refused against the wildcard, and the server must name the origin instead ([MDN, Access-Control-Allow-Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin), checked 2026-11-12).

Some requests are sent directly: a `GET`, `HEAD` or `POST` with only the safelisted headers and a content type of `application/x-www-form-urlencoded`, `multipart/form-data` or `text/plain`. Everything else — notably a `POST` with `Content-Type: application/json` — is preflighted: the browser sends an `OPTIONS` request first and only sends the real one if the server approves it ([MDN, CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS), checked 2026-11-12). An API that was never written for browser pages usually answers neither.

## Check the endpoint from the shell

Ask for the JSON the way a page from another origin would, by sending an `Origin` header and reading the response headers:

```sh
curl -sD - -o /dev/null -H "Origin: https://app.example.com" https://api.example.com/stats.json
```

- No `access-control-allow-origin` in the response: a page on another domain cannot read it. This is where the question ends.
- `access-control-allow-origin: *`: any page can read it, as long as the request sends no cookies.
- `access-control-allow-origin: https://app.example.com`: your page can read it, cookies included.

## The fix: fetch it on your own server

Your server can make any request it likes; only browsers apply the rule. One route that fetches the upstream and answers from your own domain is enough, and the page then talks to its own origin, where no check happens at all:

```js
// GET /api/stats: the upstream JSON, served from your own domain
app.get("/api/stats", async (req, res) => {
  const r = await fetch("https://api.example.com/stats.json", { signal: AbortSignal.timeout(6000) });
  const body = await r.json();
  res.set("cache-control", "public, max-age=300");
  res.json(body);
});
```

```js
// In the page: same origin, so nothing to allow
fetch("/api/stats").then((r) => r.json()).then(render);
```

Two things make the route hold up:

- **Cache it.** A five-minute copy in the server (and `max-age` for the browser) means a busy page doesn't forward every visitor to the upstream, and the upstream's rate limits stay out of the way.
- **Keep the last good copy.** If the upstream is down or slow, answer with the numbers fetched last time, so the page still shows something instead of an error. The page can then say how old they are.

If you also own the API, adding the header there is one line, and often simpler than a proxy: `Access-Control-Allow-Origin: https://app.example.com`, or `*` for data that needs no cookies.

The investor site that explains how Cloudish works reads Cloudish's usage numbers this way: the stats come from a registry that doesn't send the header, so the site's server fetches them every five minutes and its page reads `/api/stats` from its own domain. (Cloudish is made by Hal9, which started this wiki; the example is the reason the page exists, not a recommendation.)

## What not to do

- **Don't proxy secrets.** Whatever your route returns is public to anyone who can load the page. The upstream's API key stays on the server, but treat the numbers as published.
- **Don't leave CORS disabled in your browser** — a flag or an extension that turns the check off — and call it fixed. It works on your machine only; the header check above tells you what every visitor will get.
- **Don't expect a third-party API without the header to work from the page at all.** A server route or a copy made at build time are the only options. A build-time copy is fine for numbers that can be a day old, and useless for a live chart.

## Related pages

- [Checking an AI-built web app](Checking-an-AI-built-web-app.md): what to look at when a page loads but its data doesn't
- [Stale cache after a deploy](Stale-cache-after-a-deploy.md): the other reason new numbers don't show up
- [The cloud, for AI apps](Cloud-for-AI-apps.md): the container that runs your server route

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [API key](Glossary.md#api-key), [Host](Glossary.md#host), [Rate limit](Glossary.md#rate-limit), [Secret](Glossary.md#secret), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-12.

- MDN, [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS): the same-origin policy for `fetch()` and `XMLHttpRequest`, `Access-Control-Allow-Origin`, and which requests are "simple" rather than preflighted
- MDN, [Access-Control-Allow-Origin](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin): one origin or the `*` wildcard, and the wildcard's exclusion for requests that carry credentials

---

First version written with AI assistance, from a site that needed another domain's live usage numbers and found the endpoint sent no CORS header, and checked against the [sources](#sources) on 2026-11-12. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
