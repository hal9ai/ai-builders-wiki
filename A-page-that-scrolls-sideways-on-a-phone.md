---
title: "A page that scrolls sideways on a phone"
description: "A phone page wider than the screen is usually one flex or grid item that cannot shrink: find the item, let it shrink with min-width: 0, and keep sideways scrolling for the rows that should have it."
category: Problems & solutions
tags: [basics]
order: 6
checked: 2026-11-15
---

<!-- NAV:START -->
[Home](README.md) › [Problems & solutions](Category-Problems-solutions.md) · Tags: [basics](Tag-basics.md)
<!-- NAV:END -->

# A page that scrolls sideways on a phone

**A phone page that scrolls sideways is usually one flex or grid item that cannot shrink: its content's minimum width is wider than the screen, so it pushes every ancestor wider with it.** On a laptop there is room and nothing looks wrong; on a phone the whole page slides left and right. The fix is to let that item shrink, and to give a sideways scroll only to the rows that should have one.

## What it looks like

- The page slides sideways under your finger.
- Full-width things — the header, section backgrounds, the footer — run past the right edge or end early.
- Text or a button is cut off at the right, or there is a blank band on one side.
- Rotating the phone changes how bad it is, but does not fix it.

## 1. Confirm the page is wider than the screen

Open the browser console with the phone connected, or with device emulation set to a phone width such as 390px, and run:

```js
document.documentElement.scrollWidth - document.documentElement.clientWidth
```

`scrollWidth` is the width of the content, including the part not visible because of overflow; `clientWidth` is the width you can see ([MDN: Element.scrollWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollWidth), checked 2026-11-15). A result of `0` means the page is not wider than the screen, so the sideways movement is coming from something else.

## 2. Find the element that sticks out

This lists the elements whose right edge is past the visible width:

```js
const viewport = document.documentElement.clientWidth;
const insideScroller = (el) => {
  for (let p = el.parentElement; p; p = p.parentElement) {
    const x = getComputedStyle(p).overflowX;
    if (x === 'auto' || x === 'scroll') return true;
  }
  return false;
};
[...document.querySelectorAll('body *')]
  .filter(
    (el) =>
      !insideScroller(el) &&
      el.getBoundingClientRect().right > viewport + 1
  )
  .map((el) => {
    const cls = typeof el.className === 'string' ? el.className.trim().replace(/\s+/g, '.') : '';
    return el.tagName.toLowerCase() + (cls ? '.' + cls : '');
  });
```

The deepest element in the list is usually the real cause; everything above it is wide only because it contains that element. The `insideScroller` filter leaves out the cards inside a row you meant to scroll — those sit outside the screen on purpose.

## 3. Why the width is there

A flex or grid item's minimum width defaults to the minimum width of its content: the size the content needs when every line is as short as it can be without breaking ([MDN: min-width](https://developer.mozilla.org/en-US/docs/Web/CSS/min-width), checked 2026-11-15). Put a row of chips that must stay on one line inside a plain wrapper, put that wrapper in a one-column grid, and the column's minimum becomes the width of all chips side by side. The grid, and then the page, grows to that width.

The row can have `overflow-x: auto` and still cause this. Its own box scrolls, but the minimum width of its content still reaches the wrapper; the wrapper has to be allowed to shrink. (A flex or grid item that is *itself* the scroll container gets an automatic minimum of `0`, so the usual cause is a plain wrapper around the scrolling row.)

A small reproduction:

```html
<div class="page">
  <div class="copy">
    <div class="chips">
      <button>Plan a trip</button>
      <button>Analyze a spreadsheet</button>
      <button>Build a landing page</button>
    </div>
  </div>
</div>
```

```css
.page {
  display: grid;
  grid-template-columns: 1fr;
}
.chips {
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
}
```

The fix is one line on the item that contains the row:

```css
.copy {
  min-width: 0;
}
```

At the track level, the same thing is written `grid-template-columns: minmax(0, 1fr)`: the track's minimum is explicitly zero instead of the items' content width ([MDN: minmax()](https://developer.mozilla.org/en-US/docs/Web/CSS/minmax), checked 2026-11-15). If there are several nested flex or grid items between the row and the page, each one needs `min-width: 0` on the path up.

## 4. Keep the sideways scroll, on the row

Once the page fits, give the row its own scrolling and snapping:

```css
.chips {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-padding-inline: 18px;
  padding-inline: 18px;
}
.chips > * {
  flex: 0 0 auto;
  scroll-snap-align: start;
}
```

- `overflow-x: auto` makes this box the scroll container, so it scrolls instead of widening the page.
- `scroll-snap-type: x mandatory` opts the container into horizontal scroll snapping ([MDN: scroll-snap-type](https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-type), checked 2026-11-15); each child sets `scroll-snap-align: start`.
- `scroll-padding-inline` insets the region the browser snaps into, so the first card lands at the page gutter instead of flush against the screen edge ([MDN: scroll-padding-inline](https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-padding-inline), checked 2026-11-15).
- `flex: 0 0 auto` stops the cards from shrinking to fit the row.

On a wide screen, turn the row back into a normal grid so it does not look like a carousel with nothing to scroll to.

## 5. If the culprit is one element, not a row

- **A long URL, token or code line.** Let it break with `overflow-wrap: anywhere`, or give the code block its own `overflow-x: auto` ([MDN: overflow-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap), checked 2026-11-15).
- **A wide table.** Wrap it in a `div` with `overflow-x: auto`, and make sure that wrapper is allowed to shrink like any other item.
- **A decorative glow, shape or illustration positioned outside its section.** Clipping it at the section that owns it is the right use of hidden overflow: `overflow: hidden` on that section (or `overflow: clip`, which clips without creating a scroll container) ([MDN: overflow](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow), checked 2026-11-15).

## 6. Check it at phone widths

- Load the page at 320px and 390px wide; the difference from step 1 should be `0` at both.
- Scroll to the bottom and check again. A section lower down can be the only one that is too wide.
- Run the list from step 2 on a few sections, not just the top of the page.
- Swipe each sideways row: it should stop at its ends, with the first and last card fully visible.

## Do not hide it on `body`

`body { overflow-x: hidden }` hides the scrollbar but not the layout: the page is still wider than the screen, so content can be clipped, and an element that receives keyboard focus can still scroll the page sideways. Use hidden overflow only on the section that owns a deliberately clipped decoration, and fix the width where it is created.

## Related pages

- [How to check a web app an AI built](Checking-an-AI-built-web-app.md): run each page in a headless browser, keep screenshots and console errors, and catch a layout that only breaks at phone width
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md): where the build, deploy and checks fit

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Container](Glossary.md#container), [Token](Glossary.md#token).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-15.

- MDN, [min-width](https://developer.mozilla.org/en-US/docs/Web/CSS/min-width): the automatic minimum of a flex or grid item, and when it is `0`
- MDN, [minmax()](https://developer.mozilla.org/en-US/docs/Web/CSS/minmax): the track minimum and the `<flex>` value
- MDN, [Element.scrollWidth](https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollWidth): content width including overflow
- MDN, [scroll-snap-type](https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-snap-type): opting a scroll container into snapping
- MDN, [scroll-padding-inline](https://developer.mozilla.org/en-US/docs/Web/CSS/scroll-padding-inline): insets for the region used to place things in view
- MDN, [overflow-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-wrap): breaking an otherwise unbreakable string
- MDN, [overflow](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow): clipping and scrolling

---

First version written with AI assistance, from a landing page whose suggestion chips made the page wider than a 390px phone screen, and checked against the [sources](#sources) on 2026-11-15. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
