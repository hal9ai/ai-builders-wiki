---
title: "Why a deployed app is blank inside an iframe"
description: "A framed page can refuse to load and the parent page cannot see why: check X-Frame-Options and frame-ancestors, then keep an open-in-a-new-tab fallback."
category: Problems & solutions
tags: [hosting, security]
order: 6
checked: 2026-11-15
---

<!-- NAV:START -->
[Home](README.md) › [Problems & solutions](Category-Problems-solutions.md) · Tags: [hosting](Tag-hosting.md), [security](Tag-security.md)
<!-- NAV:END -->

# Why a deployed app is blank inside an iframe

**A deployed app appears as an empty or error-filled frame when the app refuses to be framed, usually with an `X-Frame-Options` header or a CSP `frame-ancestors` policy; the parent page cannot inspect the refusal, so check the headers on your server and keep an open-in-a-new-tab fallback.**

## The two headers that block a frame

`X-Frame-Options` is a response header that "can be used to indicate whether a browser should be allowed to render the document in a `<frame>`, `<iframe>`, `<embed>` or `<object>`" ([MDN, X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options), checked 2026-11-15). `DENY` means "The document cannot be loaded in any frame, regardless of origin"; `SAMEORIGIN` means "The document can only be embedded if all ancestor frames have the same origin as the page itself" ([MDN, X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options), checked 2026-11-15).

A Content Security Policy can say the same thing with more detail. `frame-ancestors` "specifies valid parents that may embed a page using `<frame>`, `<iframe>`, `<object>`, or `<embed>`", and `'none'` means "This resource may not be embedded" ([MDN, frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors), checked 2026-11-15). Setting it to `'none'` is "similar to `X-Frame-Options: deny`", and MDN points to this directive for "more comprehensive options than offered by this header" ([MDN, X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options), checked 2026-11-15).

A deployed app that sets `X-Frame-Options: SAMEORIGIN` — a common default for an app with its own sign-in — will not render in your product, because your page is a different origin. The same is true for a policy whose `frame-ancestors` list does not include your origin.

## The browser does not tell the parent

The browser blocks the frame; the parent page gets a box, not an error it can catch. The same-origin policy "restricts how a document or script loaded by one origin can interact with a resource from another origin" ([MDN, Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy), checked 2026-11-15), and cross-origin documents get "very limited access" to each other. Do not treat the frame's `load` event as proof that your app rendered: it cannot distinguish a loaded app from a blocked one.

## Check before you build the preview

Ask the deployed app for its headers from your server, not from the browser, and store the result with the deployment. A plain `GET` is enough; read `X-Frame-Options` and `Content-Security-Policy`, and treat a positive block as a reason to show the fallback instead of an iframe.

- `X-Frame-Options: DENY` or `SAMEORIGIN` → not embeddable.
- `frame-ancestors 'none'` → not embeddable.
- A `frame-ancestors` list that does not include your origin → not embeddable.
- No rule, or a rule that includes your origin → the browser will try, but still keep the fallback.

Do not follow redirects blindly while probing. A deployed app can redirect, and following it server-side lets the app steer that request at other hosts; check the first response, or validate every redirect target against the same allowlist.

## Build the frame safely

Only embed a URL your own backend recorded from the deploy API, never a URL supplied by a model or a user. Check the scheme and host before putting it in `src`; an `https` URL on the host you expect is the minimum.

The `sandbox` attribute "controls the restrictions applied to the content embedded in the `<iframe>`" ([MDN, `<iframe>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe#sandbox), checked 2026-11-15). For a cross-origin app, a starting point is `allow-scripts allow-forms allow-modals allow-popups allow-downloads allow-same-origin`: the app keeps its own origin, so it can use its own cookies and storage (subject to the browser's third-party rules), but it cannot reach your page. MDN warns against using `allow-scripts` together with `allow-same-origin` when the framed document has the same origin as the parent, "as that lets the embedded document remove the `sandbox` attribute"; a deployed app on another origin does not have that problem.

Set `referrerpolicy="no-referrer"` on the frame so the app does not receive your product's URL as a referrer; the attribute "indicates which referrer to send when fetching the frame's resource" ([MDN, `<iframe>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe#referrerpolicy), checked 2026-11-15).

## Keep a way out

The frame is a convenience, not the only path to the app. Always show **Open in a new tab** next to the preview, and say why the inline preview is unavailable when the headers block it. That covers blocked framing, a slow cold start, and a browser that blocks third-party storage.

A screenshot is not a substitute. It is a still image from one moment, it cannot be clicked, and it needs a headless browser to take it. If you want a thumbnail in a list, take it deliberately and label it as a picture. For checking what the app actually does, use a headless browser and keep the console and screenshots as evidence ([How to check a web app an AI built](Checking-an-AI-built-web-app.md)).

## What an embedded app may still fail to do

Browsers may block third-party cookies, and "if the domain and scheme are different, the cookie is not considered to be from the same site, and is referred to as a third-party cookie" ([MDN, Third-party cookies](https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Third-party_cookies), checked 2026-11-15). An app that signs users in may work in a tab and fail inside your frame even when the framing headers allow it. Test the sign-in path inside the frame, not only the public page.

## Related pages

- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md): a successful deploy response is not an app that answers
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md): headless-browser checks and screenshots
- [Previewing a signed-in page on localhost](Previewing-a-signed-in-page-on-localhost.md): a local preview of a signed-in page, for development

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Deploy](Glossary.md#deploy), [Host](Glossary.md#host), [Model](Glossary.md#model).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-15.

- MDN, [X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options): `DENY`, `SAMEORIGIN`, and the link to `frame-ancestors`
- MDN, [Content-Security-Policy: frame-ancestors](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors): valid parents, `'none'`, and the comparison with `X-Frame-Options`
- MDN, [Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy): cross-origin documents get very limited access to each other
- MDN, [`<iframe>`](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe): the `sandbox` and `referrerpolicy` attributes
- MDN, [Third-party cookies](https://developer.mozilla.org/en-US/docs/Web/Privacy/Guides/Third-party_cookies): cookies set under another domain, and browser blocking

---

First version written with AI assistance, from building a split-view preview for deployed apps and checking the framing headers and fallback against the [sources](#sources) on 2026-11-15. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
