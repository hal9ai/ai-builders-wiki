---
title: "A signed-in user with no account on another region"
description: "The user is signed in, yet the account is empty: their identity follows them across regions, the account row does not, so create it on first use instead of only reading it."
category: Problems & solutions
tags: [auth, hosting]
order: 5
checked: 2026-11-11
---

<!-- NAV:START -->
<!-- NAV:END -->

# A signed-in user with no account on another region

**A user can be signed in and still land with no account on the copy of your app they just reached, because their sign-in identity carries across regions while their account is a row in that copy's own database.** The page then shows an empty account — zero balance, no keys, no projects — and "sign in again" sends the user in a circle, because they already are.

## What it looks like

- The user switches to another region, deployment or address of the same app, or follows a link there, and still appears signed in: name or avatar present, no password prompt.
- Their account page is empty: a balance of zero, and no keys, projects or history.
- Signing in again, or reloading, changes nothing.
- An action on the page fails with a message like "no account — sign in again", which is the misleading part.

## Two different things called "signed in"

The sign-in session and the account are kept in different places, and only one of them travels.

**The sign-in identity belongs to the [provider](Glossary.md#provider).** Single sign-on is what lets one login carry across applications: Auth0 defines it as occurring "when a user logs in to one application and is then signed in to other applications automatically" ([Auth0: Single Sign-On](https://auth0.com/docs/authenticate/single-sign-on), checked 2026-11-11). For the second address to take part, the provider must allow it — Auth0's allowed callback URLs are the "set of URLs to which Auth0 is allowed to redirect users after they authenticate" ([Auth0: Application Settings](https://auth0.com/docs/get-started/applications/application-settings), checked 2026-11-11).

**The account belongs to your app's database.** It is a row keyed by the provider's user identifier. OpenID Connect defines that identifier as a "locally unique and never reassigned identifier within the Issuer for the End-User" ([OpenID Connect Core 1.0, section 8](https://openid.net/specs/openid-connect-core-1_0.html#SubjectIDTypes), checked 2026-11-11). It is the same user on every region, but signing in does not write a row into a database that has never seen them.

**The browser's own storage does not cross either.** "Access to data stored in the browser such as Web Storage and IndexedDB are separated by origin", and "each origin gets its own separate storage" ([MDN: Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy), checked 2026-11-11). Two addresses are two origins unless protocol, host and port all match, so a token or cached profile saved at the first address is not visible at the second.

If each copy of the app has its own database, the account row exists only where it was written. A shared database or replication can move rows; neither can invent a row that was never written anywhere.

## Why the account is missing instead of created

Apps usually create the account at one of two moments: a signup form, or the first authenticated request. A user sent to another region did not go through signup there, so it falls to the first authenticated request — which is often a read.

**A read endpoint should not create anything.** RFC 9110 defines a method as safe when "the client does not request, and does not expect, any state change on the origin server" ([RFC 9110, section 9.2.1](https://www.rfc-editor.org/rfc/rfc9110#section-9.2.1), checked 2026-11-11). A dashboard's `GET /account` belongs in that group, and it is also what the page refreshes to stay current: if it created rows, every refresh would be a write.

So the request answers truthfully with nothing — `account: null`, an empty list — and the page renders an empty account. Signing in again produces the same session and the same missing row.

## How to fix it: create on first touch

Add an operation whose job is "make sure this identity has an account", and call it once when a signed-in page first loads:

- **Give it its own endpoint**, such as `POST /account/ensure`, next to the read. Return the same shape as the read, so the page can use either response.
- **Call it on the first authenticated load, not every load.** After it succeeds, use the read-only endpoint for refreshes and polls.
- **Make it idempotent in the app, not just named POST.** RFC 9110 says a method is idempotent when "the intended effect on the server of multiple identical requests with that method is the same as the effect for a single such request" ([RFC 9110, section 9.2.2](https://www.rfc-editor.org/rfc/rfc9110#section-9.2.2), checked 2026-11-11), and POST is not in its idempotent set. Enforce one account per user identifier with a uniqueness constraint, and have the endpoint return the existing row when there is one — not a second account.
- **Keep any starting grant inside the create path.** A free credit or trial that comes with a new account should be applied when the row is inserted, so a double click, two tabs or an automatic retry cannot grant it twice.
- **Writing the row at sign-in is not enough on its own.** A callback can be missed, retried, or never reached when single sign-on signs the user in silently. The first-touch call covers those cases.

Two tabs arriving at once are what catches a read-then-insert without a constraint: both reads find nothing and both insert. Either hold a lock around the insert, or let the database reject the second and return the existing row.

## Check that it is fixed

- Sign in on the second address, or in a private window that has no session there, and load the first authenticated page: the account exists, with the starting balance it should have.
- Send the "ensure" request twice, or reload a page that calls it: one account, one grant.
- Open two tabs of the same page at once on a fresh identity: still one account.
- Watch the ordinary read during a refresh: it should perform no writes.
- Repeat on each region you run, not only the one you develop against.

## Related pages

- [A login that loops between your app and the sign-in provider](A-login-that-loops.md)
- [Where an AI-built app keeps its data](Where-an-AI-built-app-keeps-its-data.md)
- [Serve one custom domain from more than one datacenter](Serve-one-domain-from-more-than-one-datacenter.md)
- [The cloud, for AI apps](Cloud-for-AI-apps.md)
- [Security for AI apps and agents](Security-for-AI-apps.md)

## See also

<!-- SEEALSO:START -->
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-11.

- MDN, [Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy): storage separated by origin
- OpenID Connect Core 1.0, [section 8, Subject Identifier Types](https://openid.net/specs/openid-connect-core-1_0.html#SubjectIDTypes): the subject identifier
- IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): sections 9.2.1 (safe methods) and 9.2.2 (idempotent methods)
- Auth0, [Single Sign-On](https://auth0.com/docs/authenticate/single-sign-on)
- Auth0, [Application Settings](https://auth0.com/docs/get-started/applications/application-settings): allowed callback URLs

---

First version written with AI assistance from a datacenter switch that left a signed-in user with an empty account, and checked against the [sources](#sources) on 2026-11-11. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
