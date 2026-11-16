---
title: "A product demo that pretends to be live"
description: "A scripted demo on a landing page is useful when it says it is scripted, follows the request the visitor can see, and carries their prompt into sign-up."
category: Problems & solutions
tags: [demos, product]
order: 7
checked: 2026-11-15
---

<!-- NAV:START -->
[Home](README.md) › [Problems & solutions](Category-Problems-solutions.md) · Tags: [demos](Tag-demos.md), [product](Tag-product.md)
<!-- NAV:END -->

# A product demo that pretends to be live

**A scripted product demo should be labelled as a sample and should carry the visitor's own prompt into the real product; presenting canned output as a live model response costs trust the first time the real result differs.** A landing page often has no session, no API spend and no latency budget, so a local timeline is a reasonable way to show the shape of the experience. The problem is the frame around it: the label, the controls, and what happens when the demo ends.

## What goes wrong

- A green "LIVE" badge sits above a transcript that never called a model.
- The visitor can type, but the reply ignores what they typed.
- The demo shows a file or page the product cannot make yet.
- The final button starts a generic sign-up and drops the request, so the first real conversation starts from zero.
- The animation has no reduced-motion path, and the artifact is the only proof of what happened.

Each of those turns a preview into a small broken promise. The fix is not to remove the demo; it is to make the boundary visible and make the handoff real.

## 1. Say "sample", not "live"

Use a plain badge such as `SAMPLE` or a line such as "Scripted previews. Pick one, then send the prompt to make your own." Reserve a live badge for output that a model or tool actually produced. The same rule applies to a "generating" spinner: if no work is running, do not show one.

## 2. Let the visitor choose the story, and keep the prompt in sync

Treat each scenario as data: a label, the prompt, the reply, the tool steps, the artifact and the files. Put the prompt in an editable field on the page. When the visitor picks a story, replace the field's text with that story's prompt and restart the preview. When the visitor presses send, use the text in the field, not a hidden copy, and let a matching word pick the closest story.

That gives the visitor two honest paths: watch a scenario, or edit the prompt and see the same shape with their words in the conversation.

## 3. Run a local, cancelable timeline

A small state machine is enough:

1. type the visitor's prompt;
2. show the working state;
3. type the reply;
4. reveal the tool steps;
5. reveal the artifact;
6. reveal the files;
7. show the call to action.

Set every delay with a timer you can clear when the component unmounts or the story changes. If the visitor changes the story mid-animation, cancel the old run instead of letting two timelines type into the same panel. If `prefers-reduced-motion` is set, jump to the final state; do not type or pulse.

## 4. Hand the prompt to the real product

The call to action should carry the exact text the visitor can see into sign-up and then into the first real conversation. A label such as "Run this prompt — start free" is clearer than "Get started". Store the pending prompt before navigation and consume it after authentication. Then the demo is a true preview, not a detour.

## 5. Only show what ships today

Choose scenarios from the product's current abilities. If a capability is planned, put it behind a separate, clearly marked preview and do not make it look like the demo's output. The test is simple: could a new account reproduce this result today, even if slower or messier? If not, leave it out.

## 6. Check the demo like a product

- Reload several times: the random starting story is different, and the selected card is visible when it should be.
- Pick every story: the prompt, title, artifact and files change together.
- Type a free-form prompt and send it: the closest story is chosen, but the visitor's words remain in the transcript and in the handoff.
- Finish the animation and press the call to action: the pending prompt reaches sign-up unchanged.
- Turn on reduced motion: the final state appears without typing.
- Try 1440, 768, 390 and 360 px: no horizontal page scroll; the story rail scrolls to the active card on a phone.
- Read the console: no errors and no failed requests.

## Why the label matters

A scripted demo is a promise about the shape of the product. When it is labelled and the prompt is carried through, it sets an expectation the real product can meet. When it is called live and the result is canned, the first real run has to overcome a small lie. The extra sentence and the extra state are cheaper than that.

## Related pages

- [Checking an AI-built web app](Checking-an-AI-built-web-app.md): the browser checks that catch a demo which only looks finished
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md): where a preview sits on the way to a real app

## Sources

No vendor claims on this page. The pattern was checked against a working landing-page implementation on 2026-11-15.

---
Written from a landing-page implementation reviewed on 2026-11-15. No vendor claims to check. To fix something, open an issue or a pull request. Text under [CC BY 4.0](LICENSE).
