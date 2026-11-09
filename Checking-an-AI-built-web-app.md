---
title: "How to check a web app an AI built"
description: "Run it in a headless browser: load each page, click the main actions, and keep the console errors, failed requests and screenshots as evidence."
category: How-to
tags: [coding-agents]
order: 2
checked: 2026-11-05
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [coding-agents](Tag-coding-agents.md)
<!-- NAV:END -->

# How to check a web app an AI built

**A web app an AI built is checked the way any web app is: run it, drive it in a headless browser, and keep the evidence — every page loaded, every main action clicked, and the console errors, failed requests and screenshots that came back.** The code compiling and its tests passing only say that the parts the tests cover work; they say nothing about the page a user opens.

The examples here use [Playwright](https://playwright.dev/), a browser automation library. Any headless-browser tool has the same pieces; the point is not the tool but looking at the running app before you share the link.

## 1. Start the app, and mock what is not running

**Run the app the way its README says, open the URL it prints, and if a page depends on a backend you have not started, mock that endpoint inside the check instead of changing the app.** If the front end asks for its session or config, gets a connection refused, and stops rendering, the page stays blank however good the code is.

Playwright can answer that request from inside the check without touching the app's code: it "provides APIs to mock and modify network traffic, both HTTP and HTTPS", and "any requests that a page does, including XHRs and fetch requests, can be tracked, modified and mocked" ([Playwright, Mock APIs](https://playwright.dev/docs/mock), checked 2026-11-05).

```js
// check.mjs
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();

await page.route('**/session/config', (route) =>
  route.fulfill({
    status: 200,
    contentType: 'application/json',
    body: JSON.stringify({ enabled: false }),
  }),
);
```

Keep the mock in the check script, not in the app: a mock shipped in the app makes the page pass a check it would fail in production, and the next [deploy](Glossary.md#deploy) carries it along.

## 2. Watch what the browser reports

**Before the page finishes loading, attach listeners for uncaught exceptions, console errors and failed responses, so the reason a blank page stayed blank is in the output rather than a guess; none of those three shows up in a screenshot.**

```js
page.on('pageerror', (err) => console.log('page error:', err.message));
page.on('console', (msg) => msg.type() === 'error' && console.log('console error:', msg.text()));
page.on('response', (res) => res.status() >= 400 && console.log('failed:', res.status(), res.url()));
```

The Page object emits these as they happen: `pageerror` is "emitted when an uncaught exception happens within the page"; `console` when JavaScript "calls one of console API methods"; `response` "when response status and headers are received for a request" ([Playwright, Page](https://playwright.dev/docs/api/class-page), checked 2026-11-05). A 404 on a favicon or a tracking pixel is noise; read the URL before you count a line as a failure. A 5xx from your own [API](Glossary.md#api) is not noise.

**Do not wait for the network to go quiet.** Playwright marks `networkidle` "**DISCOURAGED**" — "wait until there are no network connections for at least `500` ms" — and adds: "Don't use this method for testing, rely on web assertions to assess readiness instead" ([Playwright, Page](https://playwright.dev/docs/api/class-page), checked 2026-11-05). A client-rendered page can arrive, open no requests, and still be blank while a large view is built.

Wait for something that must exist instead — the heading, the first card, the button — and let the browser tell you when it is really there. Playwright "auto-waits for all the relevant checks to pass and only then performs the requested action", and an element is visible when it "has non-empty bounding box and does not have `visibility:hidden` computed style" ([Playwright, Actionability](https://playwright.dev/docs/actionability), checked 2026-11-05).

```js
await page.goto('http://localhost:3000/');
await page.getByRole('heading', { name: 'Dashboard' }).waitFor();
```

Locating by role and accessible name, as a person would, also keeps the check honest about which control you clicked.

## 3. Click the main actions

**List the few things the app is for and do them in the same run: submit the form, follow the flow, press the button that generates a file.** A page that renders is not an app that works, and the failures that matter appear after the click, not before it.

For a download, wait for the event before clicking, then save the file:

```js
const downloadPromise = page.waitForEvent('download');
await page.getByRole('button', { name: 'Download PNG' }).click();
const download = await downloadPromise;
await download.saveAs('/tmp/check.png');
```

The `download` event is "emitted when attachment download started", and the Download instance gives access to "basic file operations on downloaded content"; the docs' advice is to "wait for the download process to complete and save the downloaded file somewhere" ([Playwright, Page](https://playwright.dev/docs/api/class-page); [Playwright, Downloads](https://playwright.dev/docs/downloads), checked 2026-11-05).

## 4. Look at what came out

**Take a screenshot of each page and each generated file, and look at them; a screenshot is the only part of the check that shows what a user sees.**

```js
await page.screenshot({ path: '/tmp/page.png' });
await page.locator('.card').first().screenshot({ path: '/tmp/card.png' });
```

`page.screenshot({ path: 'screenshot.png' })` saves the viewport, and "sometimes it is useful to take a screenshot of a single element" ([Playwright, Screenshots](https://playwright.dev/docs/screenshots), checked 2026-11-05). On a page of repeated cards, capture one of each shape rather than every card; the layout is what you are checking.

Set the viewport to the size you care about before the run. A default viewport is one fixed size, not your user's screen, and a layout can be right at one width and broken at the next.

Open the images. This is where the check earns its keep: the failures that survive a green build are visual — a line that wraps to two rows, a label that pushes a number out of its card, an image that never loaded and left its alt text in a gray box. None of them throw, and none of them appear in the console.

If the file's size is part of the job — a launch image, a favicon, an Open Graph card — check the bytes, not the preview. `file /tmp/check.png` prints the format and the pixel size. A page can show a sharp, correctly cropped preview of an image that exported at the wrong dimensions.

## 5. Keep the check

**Put the whole run in one script and run it again after every deploy and before every link you share; the second run is nearly free and catches the change that broke what the first run proved.**

A short checklist for the end of a run:

- Every route returned HTML, and its main element had content.
- No uncaught exceptions, and no 4xx or 5xx from the app's own API.
- Each main action completed: the form answered, the list grew, the file arrived.
- The screenshots match the design at the viewport you care about.
- Generated files have the format and size you promised.

## What this catches, and what it does not

A headless run catches a page that does not render, a request that fails, a button wired to nothing, an image that 404s and a file that exports at the wrong size. It does not catch a slow page on a phone, a layout that only breaks at one width, a flow that needs a real login or a third-party service, or a logic error the page never shows. Check a phone and a narrow window by hand before a launch, and read the [logs](Glossary.md#logs) for the requests the browser never made.

Screenshots, console messages and downloaded files can contain tokens, personal data and private content. Look before you paste one into an issue or a pull request, and keep the check's output out of public build logs — see [security](Security-for-AI-apps.md) and [data protection](Data-protection.md).

## Related pages

- [From idea to deployed AI app: a typical workflow](Idea-to-deployed-AI-app.md)
- [Security for AI apps and agents](Security-for-AI-apps.md)
- [Data protection when you use AI](Data-protection.md)
- [Ways to use AI](Ways-to-use-AI.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Deploy](Glossary.md#deploy), [Logs](Glossary.md#logs), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-05.

- Playwright, [Mock APIs](https://playwright.dev/docs/mock); [Downloads](https://playwright.dev/docs/downloads); [Screenshots](https://playwright.dev/docs/screenshots); [Page](https://playwright.dev/docs/api/class-page); [Actionability](https://playwright.dev/docs/actionability)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-05. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
