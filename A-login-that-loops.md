---
title: "A login that loops between your app and the sign-in provider"
description: "The address bar flashes a callback URL with a code in it, over and over: how a page that redirects before the code is exchanged turns a sign-in into an endless loop, and how to fix it."
category: Problems & solutions
tags: [auth]
order: 2
checked: 2026-11-06
---

<!-- NAV:START -->
[Home](README.md) › [Problems & solutions](Category-Problems-solutions.md) · Tags: [auth](Tag-auth.md)
<!-- NAV:END -->

# A login that loops between your app and the sign-in provider

**A login that bounces between your app and its sign-in provider, forever, almost always means the page the provider redirects back to navigates away before the app can exchange the one-time code for a session.** The fix is to leave the callback URL alone until the app has read it, and to stop the app from starting another login from that same page.

## What it looks like

- You click "Sign in" or a button that needs a signed-in user.
- The provider's page flashes, or never appears because you are already signed in there.
- Your own address bar flashes a URL ending in `?code=...&state=...`, often too fast to read.
- It never settles on a page, and you are still signed out when it stops.

That `code` is the whole point of the round trip: it is how the provider hands your app a session. If it is not used, the login did not happen.

## How the redirect is supposed to work

The common pattern for browser apps is the OAuth 2.0 authorization code flow:

1. Your app sends the browser to the provider, asking for a code. The request names a redirect URI, the address the provider may send the user back to.
2. The user signs in at the provider.
3. The provider redirects the browser to that redirect URI with a short-lived `code` and the `state` value your app sent. The code "MUST expire shortly after it is issued", and the client "MUST NOT use the authorization code more than once" ([RFC 6749, section 4.1.2](https://www.rfc-editor.org/rfc/rfc6749#section-4.1.2), checked 2026-11-06).
4. Your app POSTs that code to the provider's token endpoint, with the same redirect URI, and gets tokens back ([RFC 6749, section 4.1.3](https://www.rfc-editor.org/rfc/rfc6749#section-4.1.3), checked 2026-11-06). `state` exists to protect step 3 from cross-site request forgery ([RFC 6749, section 4.1.1](https://www.rfc-editor.org/rfc/rfc6749#section-4.1.1), checked 2026-11-06); browser apps also use PKCE to tie the code to the app that asked for it ([RFC 7636](https://www.rfc-editor.org/rfc/rfc7636), checked 2026-11-06).

Steps 3 and 4 are the fragile part. The code lives only in the URL of the page the provider lands on, and it is only good once.

## Why, precisely, the loop happens

Two ordinary pieces of app code collide:

1. **The callback route redirects.** In a single-page app the callback address is a route, and that route is often written to bounce visitors onward — to a dashboard, or to a "you are signed in now" page. That redirect rewrites the address, and the `code` and `state` go with it.
2. **The auth library reads the callback late.** The library parses the `code` from the page's URL when it finishes starting up, not at the instant the page paints. Auth0's browser library, for example, says `handleRedirectCallback` "must be called in order to complete the login flow" when "the browser is redirected from Auth0 back to your SPA" ([Auth0 SPA SDK](https://auth0.com/docs/libraries/auth0-single-page-app-sdk), checked 2026-11-06). If the URL has already been rewritten, there is no code left to read.

So the exchange never happens, the app believes nobody is signed in, and its "you must be signed in to see this page" guard sends the user back to the provider. Because the user still has a session at the provider, it answers instantly with a fresh code, and the same two steps fail again. Nothing in that cycle can break out on its own, which is why it is so fast.

## How to confirm it in a minute

Open the browser's developer console before clicking sign in, and look at the Network panel, filtered to the provider's domain:

- **A POST to the provider's token endpoint** (`/oauth/token` at Auth0) means the code was read and the exchange was attempted; the loop is then about the exchange failing, not about the code being lost.
- **No token request at all**, while the address bar shows `?code=...`, means the code was thrown away before the library looked for it. That is this bug.

The console panel usually shows the library's own complaint — often an error about an invalid state or a missing transaction — instead of anything that names your redirect.

## How to fix it

- **Keep the callback URL intact.** The route that receives `code` and `state` must not redirect while the callback is pending. Let the auth library finish, then navigate. In a single-page app, check for the callback parameters in the route's own guard before sending the visitor anywhere.
- **Never start a login from the callback page.** The "not signed in, so redirect to the provider" guard must skip the callback route. Without this, one failed exchange turns into an endless loop instead of one visible error.
- **Let both halves of the app share the session.** If the redirect URI belongs to one part of the site and the page you return to belongs to another, the second part has to find the tokens the first part stored. Auth0's SDK stores tokens in memory by default and only keeps them across page loads when `cacheLocation` is set to `localstorage` ([Auth0 SPA SDK](https://auth0.com/docs/libraries/auth0-single-page-app-sdk), checked 2026-11-06).
- **Use the `state` you were given.** After a successful exchange, send the user to the address recorded in it — for example the page whose button started the login — rather than to a generic home page.

## Check that it is fixed

- With the Network tab open, sign in once: a single token request appears, and the browser settles on the page the login started from.
- Sign out and repeat: same result.
- A stale or expired callback link now produces one clear error or a plain signed-out page, not a loop. That is the guard from the second bullet doing its job.

## Related pages

- [From idea to deployed AI app](Idea-to-deployed-AI-app.md#4-deploy): where sign-in and secrets sit in a deploy
- [Security for AI apps and agents](Security-for-AI-apps.md#secrets-and-api-keys): why the tokens this flow produces are secrets

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Provider](Glossary.md#provider), [Token](Glossary.md#token).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-06.

- IETF, [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749): sections 4.1.1 (state), 4.1.2 (authorization response) and 4.1.3 (token request)
- IETF, [RFC 7636: Proof Key for Code Exchange by OAuth Public Clients](https://www.rfc-editor.org/rfc/rfc7636)
- Auth0, [Auth0 Single Page App SDK](https://auth0.com/docs/libraries/auth0-single-page-app-sdk): `handleRedirectCallback` and `cacheLocation`

---

First version written with AI assistance, from a sign-in loop found while deploying a web app, and checked against the [sources](#sources) on 2026-11-06. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
