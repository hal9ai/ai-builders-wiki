---
title: "How to carry a prompt through sign-in into the first chat"
description: "Save the text a visitor typed before the sign-in redirect, read it back once when the app restarts, and use it as the first message: what survives the redirect, and how to keep the handoff safe."
category: How-to
tags: [auth, storage]
order: 15
checked: 2026-11-15
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [auth](Tag-auth.md), [storage](Tag-storage.md)
<!-- NAV:END -->

# How to carry a prompt through sign-in into the first chat

**A [prompt](Glossary.md#prompt) typed on a landing page survives the sign-in redirect only if the page saves it in the browser before the visitor leaves, and the app reads it back — once — after it restarts.** In-memory JavaScript is gone by then: the redirect loads new pages, so the natural home for a short, per-tab handoff is `sessionStorage`.

## What the redirect throws away

**A redirect sign-in is a series of page loads, and each one starts the app again with an empty memory.** OpenID Connect describes the successful response as an OAuth 2.0 Authorization Response "returned from the OP's Authorization Endpoint", whose parameters are returned "by adding them as query parameters to the `redirect_uri` specified in the Authorization Request" ([OpenID Connect Core 1.0, section 3.1.2.5](https://openid.net/specs/openid-connect-core-1_0.html#AuthResponse), checked 2026-11-15). The browser leaves your page for the provider, then comes back to the redirect URI — your single-page app boots from scratch.

A variable, a React state value or a module-level cache does not survive that trip. The visitor is still the same person, in the same tab, but your page is a new instance of the app.

## Store a small payload before leaving

**Save only what the first chat needs: the text, where to return, and when it was saved.** `sessionStorage` has the right lifetime — "a page session lasts as long as the tab or the browser is open, and survives over page reloads and restores"; closing the tab clears it ([MDN, `Window.sessionStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage), checked 2026-11-15). It is not shared with other tabs, which matches a draft the visitor is about to send, not a preference that should follow them around.

```js
const KEY = 'pending-prompt';

function savePrompt(text) {
  const payload = { text: text.slice(0, 4000), from: location.pathname, at: Date.now() };
  try {
    sessionStorage.setItem(KEY, JSON.stringify(payload));
  } catch {
    // Storage can be blocked; the visitor can still sign in without the handoff.
  }
}
```

- **Keep it short.** Trim the text and check its length again when you read it back; do not let whatever is in storage become an unbounded request.
- **Do not store secrets.** `sessionStorage` is readable by any script on the origin: "A single Cross Site Scripting can be used to steal all the data in these objects", and OWASP recommends "not to store sensitive information in local storage" ([OWASP HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html), checked 2026-11-15). A prompt is user text; access [tokens](Glossary.md#token) and API keys are not.
- **Expect it to fail.** Reading `sessionStorage` can throw a `SecurityError` when, for example, "the user has configured the browsers to prevent the page from persisting data" ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage), checked 2026-11-15). Wrap both read and write, and let the sign-in flow work without it.

## Read it once, after the app knows who the user is

**Consume the payload only when the app has a signed-in user, remove the key as part of reading it, and then pass the text to the first chat.** Reading before auth settles wastes the payload on a signed-out page; reading without removing it sends the same prompt again on the next reload.

```js
function takePrompt() {
  let raw;
  try {
    raw = sessionStorage.getItem(KEY);
  } catch {
    return null;
  }
  if (!raw) return null;
  try {
    sessionStorage.removeItem(KEY); // first read wins, even if the page boots twice
  } catch {
    return null;
  }

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch {
    return null;
  }
  if (typeof payload?.text !== 'string' || !payload.text.trim()) return null;
  if (!Number.isFinite(payload.at) || Date.now() - payload.at > 30 * 60 * 1000) return null;
  return payload;
}
```

Two details matter more than they look:

- **Remove before you validate.** If the page boots twice, both runs must not send the same prompt. React's Strict Mode runs "one extra setup+cleanup cycle in development for every Effect" ([React, StrictMode](https://react.dev/reference/react/StrictMode), checked 2026-11-15); the first read takes the payload and the second finds nothing. In production the extra cycle does not happen, but a reload or a second auth callback can still race the same way.
- **Let it expire.** A prompt saved on Monday should not appear in a chat on Friday. Thirty minutes is arbitrary but explicit; pick a window that matches how long a sign-in takes in your app.

If the visitor abandons sign-in, leave the payload in place: they may come back and finish. It disappears with the tab, or when the age check rejects it.

## Show the handoff on the sign-in page

**Echo the saved text on the sign-in page so the visitor sees that the prompt was kept, but do not consume it there.** The post-sign-in consumer owns the key; the sign-in page only reads and displays it.

```
Your first task
Plan a calm week in Kyoto, with two slow mornings.
```

Render it as text (React escapes it by default), cap the visible length, and read it inside a `try/catch` for the same storage exceptions. If the payload is stale or malformed, show nothing rather than an error.

## Check that it works

1. Signed out, type a prompt on the landing page and submit. You land on sign-in and see the prompt echoed.
2. Sign in through the real provider, including the full redirect. The first chat opens with that exact text as its first message.
3. Reload the app. The prompt is not sent a second time.
4. Save a payload with an old timestamp, then sign in: it is ignored and removed.
5. Block storage for the site and repeat: sign-in still completes, without the handoff.

## Notes

- **A new tab is a new page session.** "Opening a page in a new tab or window creates a new session" ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage), checked 2026-11-15), so a sign-in that finishes in another tab may not see the payload. A tab opened by your page starts with a copy of the opener's `sessionStorage`; after that the two are separate.
- **A URL parameter is the other option, and it leaks.** Passing the prompt through the redirect URI puts it in browser history and server logs, and long prompts can exceed URL limits. Browser storage avoids both; this is a design trade-off, not a rule.
- **A server-side draft needs an identity first.** Before sign-in there is no account to attach a draft to. After sign-in, storing the first message on the server is a reasonable alternative — in a database, not process memory ([Where an AI-built app keeps its data](Where-an-AI-built-app-keeps-its-data.md)).

## Related pages

- [A login that loops between your app and the sign-in provider](A-login-that-loops.md): keep the callback URL intact until the code is exchanged.
- [Where an AI-built app keeps its data](Where-an-AI-built-app-keeps-its-data.md): what belongs in the browser, and what belongs on the server.
- [Security for AI apps and agents](Security-for-AI-apps.md#secrets-and-api-keys): why tokens are secrets, not page state.

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [API key](Glossary.md#api-key), [Logs](Glossary.md#logs), [Prompt](Glossary.md#prompt), [Provider](Glossary.md#provider), [Secret](Glossary.md#secret), [Token](Glossary.md#token).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-15.

- MDN, [`Window.sessionStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/sessionStorage): page-session lifetime, new tabs, and the `SecurityError` when storage is blocked.
- OpenID Foundation, [OpenID Connect Core 1.0, section 3.1.2.5, Successful Authentication Response](https://openid.net/specs/openid-connect-core-1_0.html#AuthResponse)
- React, [StrictMode](https://react.dev/reference/react/StrictMode): the extra setup+cleanup cycle in development.
- OWASP, [HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html): keeping sensitive data out of Web Storage.

---

First version written with AI assistance, out of a session that implemented this handoff in a React app, and checked against the [sources](#sources) on 2026-11-15. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
