---
title: "How to tell whether a page overflows the screen"
description: "Compare scroll size with client size at the viewport sizes you care about: a larger scroll width or height means something does not fit."
category: How-to
tags: [coding-agents]
order: 3
checked: 2026-11-15
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [coding-agents](Tag-coding-agents.md)
<!-- NAV:END -->

# How to tell whether a page overflows the screen

**A page overflows when the document, or a container you care about, has a larger scroll width or scroll height than its client width or client height at the viewport you are testing; measure those numbers at each size instead of judging from one screenshot.** A page-wide horizontal scrollbar is one symptom, but a fixed-height panel or a presentation slide can hide its overflow inside its own scrolling box, where the page itself looks fine.

This page is about measuring the fit. For the wider headless-browser check — console errors, failed requests, clicks and screenshots — see [How to check a web app an AI built](Checking-an-AI-built-web-app.md).

## Pick the sizes you care about

**Test the viewport sizes your users actually get, and set them before the page loads.** A laptop, a meeting-room projector and a phone are different layouts, not the same layout at three zoom levels.

Useful starting sizes are 1440×900 for a laptop, 1024×768 for an older projector, and 390×844 for a phone. Those are viewport sizes: the space the page gets, not the physical screen, so browser toolbars and the operating system's window borders are already excluded.

In Playwright, set the viewport before navigating:

```js
import { chromium } from 'playwright';

const browser = await chromium.launch();
const page = await browser.newPage();
await page.setViewportSize({ width: 1024, height: 768 });
await page.goto('http://localhost:3000/');
```

Playwright's `page.setViewportSize(viewportSize)` "will resize the page", and the docs recommend calling it before navigating because some sites do not handle a viewport change well ([Playwright, Page](https://playwright.dev/docs/api/class-page#page-set-viewport-size), checked 2026-11-15).

## Measure the page for horizontal overflow

**Read the root element's `scrollWidth` and `clientWidth`: a scroll width larger than the client width means content extends past the visible width.** Use the root element rather than `window.innerWidth` because `clientWidth` leaves out the vertical scrollbar, so a normal vertical scrollbar does not look like horizontal overflow.

```js
const doc = await page.evaluate(() => {
  const root = document.documentElement;
  return {
    viewportWidth: innerWidth,
    scrollWidth: root.scrollWidth,
    clientWidth: root.clientWidth,
    horizontalOverflow: root.scrollWidth > root.clientWidth,
  };
});
```

`scrollWidth` is "a measurement of the width of an element's content, including content not visible on the screen due to overflow", while `clientWidth` is the element's inner width, including padding but excluding borders, margins and vertical scrollbars ([MDN, Element.scrollWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollWidth); [MDN, Element.clientWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientWidth), checked 2026-11-15).

A positive difference is the whole test. `0` means nothing sticks out horizontally at that width; anything larger is content the visitor must scroll sideways to reach.

## Measure a container for vertical overflow

**Vertical scrolling is normal for a long page, so measure the container that is supposed to fit: a slide, a dialog, a dashboard panel or a card with a fixed height.** The same comparison works in the other direction: `scrollHeight > clientHeight` means content continues below the visible area.

```js
const stage = await page.evaluate(() => {
  const el = document.querySelector('.slide');
  return {
    scrollHeight: el.scrollHeight,
    clientHeight: el.clientHeight,
    overflows: el.scrollHeight > el.clientHeight,
  };
});
```

`scrollHeight` measures "the height of an element's content, including content not visible on the screen due to overflow"; `clientHeight` is the inner height, again including padding but excluding borders, margins and horizontal scrollbars ([MDN, Element.scrollHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight); [MDN, Element.clientHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientHeight), checked 2026-11-15).

For a presentation, a nonzero difference usually means the slide does not fit and the bottom of the content is off-screen. For an ordinary page section, scrolling may be intentional: decide what "fits" means for that container before you treat the number as a failure.

## Walk every screen, not just the first

**Click through the whole app — every tab, slide, step and dialog — and measure after each one, because a layout that fits on the first screen can overflow on the third.** Open the menus and panels a visitor can open; hidden content is still content, and a dialog is often the tightest box in the app.

Two practical rules:

- Reset the container's scroll position to the top before measuring, so `scrollTop` does not hide the top of the content.
- Wait for entrance animations and data to finish. A card that is still sliding in has a different size from the settled one.

The same measurement works for both languages if the app is translated: a longer translation is exactly the kind of content that turns a fitting card into an overflowing one.

## Look at the screenshot too

**Numbers find overflow; a screenshot finds content that is clipped, overlapping or unreadable without increasing any scroll size.** Take one screenshot at each size after the measurements pass, and open it.

A panel with `overflow: hidden` can report no overflow while cutting off its own contents. Absolutely positioned badges, tooltips and long labels can overlap without making the page wider. Text can fit and still be too small to read from the back of a room. The [headless check page](Checking-an-AI-built-web-app.md#4-look-at-what-came-out) covers capturing and keeping screenshots.

## When the number is too big

**Find the element that is wider or taller than its container, then fix that element or its container — not the whole page.** Shrinking the root font or hiding the overflow moves the problem out of sight.

Common causes to look for:

- A fixed width or minimum width that is larger than the space left on a narrow screen.
- A horizontal row of cards or buttons whose children keep their content width instead of shrinking. In flexbox, a child's `min-width` defaults to `auto`, which prevents it shrinking below its content; setting `min-width: 0` on the child that holds the text is the usual fix ([MDN, min-width](https://developer.mozilla.org/en-US/docs/Web/CSS/min-width), checked 2026-11-15).
- A long URL, file name or unbroken word. `overflow-wrap` lets the browser break it ([MDN, overflow-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap), checked 2026-11-15).
- A grid whose columns have fixed minimums that add up to more than the container.
- Negative margins or an element positioned outside its container, which can widen the scroll area without changing the layout of the elements around it.

Re-run the measurement after the change at every size, not just the one that failed: a fix for 390px can break 1024px.

## What this does not catch

**Overflow numbers only compare content size with visible size; they say nothing about whether the content is usable.** Keep the screenshot and the click-through alongside them.

- Content clipped by `overflow: hidden` reports no overflow.
- Overlapping elements can fit inside the box and still cover each other.
- A tiny but complete layout passes every number.
- A page can be correct at the sizes you tested and wrong at the one you did not; there is no substitute for testing the sizes your users have.

## Related pages

- [How to check a web app an AI built](Checking-an-AI-built-web-app.md)
- [From idea to deployed AI app: a typical workflow](Idea-to-deployed-AI-app.md)
- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Container](Glossary.md#container).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-15.

- Playwright, [Page](https://playwright.dev/docs/api/class-page#page-set-viewport-size): `setViewportSize`.
- MDN, [Element.scrollWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollWidth); [Element.clientWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientWidth); [Element.scrollHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight); [Element.clientHeight](https://developer.mozilla.org/en-US/docs/Web/API/Element/clientHeight); [min-width](https://developer.mozilla.org/en-US/docs/Web/CSS/min-width); [overflow-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap).

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-15. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
