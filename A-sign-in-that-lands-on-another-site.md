---
title: "A sign-in that lands on another site"
description: "Clicking sign in takes the browser to a page with no login form on it, and your app never hears about the attempt: the sign-in provider's fallback route points at the wrong place, and the fix is to own that route."
category: Problems & solutions
tags: [auth]
order: 4
checked: 2026-11-14
---

<!-- NAV:START -->
[Home](README.md) › [Problems & solutions](Category-Problems-solutions.md) · Tags: [auth](Tag-auth.md)
<!-- NAV:END -->

# A sign-in that lands on another site

**If clicking "Sign in" ends on a page that has no login form on it, the sign-in provider could not resume the login and redirected the browser to a fallback route configured on the provider — so your app was never reached, and nothing in your app is wrong.** The fix is to point that fallback at a route you own, which starts the sign-in again.

## What it looks like

- You click "Sign in". The browser visits the provider, then lands somewhere unexpected: the company's marketing site, a blank page, a dashboard that is not signed in.
- The address has a query string you did not write, usually ending in `?iss=https%3A%2F%2Flogin.example.com%2F` — the provider's own address, encoded.
- No login form ever appears, and no error is shown. The page looks like a normal page of the wrong site.
- Your app's logs show no sign-in attempt at all: no request to the callback address.
- It may happen to some people and not others, or on some browsers and not others.

## First, rule out your app

The absence in your logs is the useful signal. If the provider had sent the browser back with a `code`, your callback route would have seen a request — even a failing one. If the browser never arrives, the break is between the provider and your app, and no change to your app's code will fix it:

```sh
# Follow the provider's authorize request without cookies and print where it lands.
curl -sL -o /dev/null -w '%{url_effective}\n' 'https://login.example.com/authorize?client_id=...&redirect_uri=https%3A%2F%2Fapp.example.com%2Fauth%2Fcallback&response_type=code&scope=openid&state=test'
```

If the last URL is a host that is not the provider and not your app, the provider itself sent the browser away. A `403` saying "redirect URI mismatch" instead is a different problem: see [A sign-in that breaks behind a proxy: the redirect URI](A-sign-in-that-breaks-behind-a-proxy.md).

Running the same request twice — once with a cookie jar, once without — tells you whether the fallback is what users hit. Auth0, for example, renders its normal login form when the request carries its login-transaction cookie, and falls back when it does not.

## Why the provider sends the browser elsewhere

OpenID Connect has a section for this, "Initiating Login from a Third Party": an initiating party sends the browser to the application's login-initiation URL with an `iss` parameter, "Issuer Identifier for the OP that the RP is to send the Authentication Request to" ([OpenID Connect Core 1.0, Initiating Login from a Third Party](https://openid.net/specs/openid-connect-core-1_0.html#ThirdPartyInitiatedLogin), checked 2026-11-14). The application's job is then to send that Authentication Request to the provider named.

Auth0 points at the same specification for its own fallback: "As per the OIDC Third Party Initiated Login specification, the `iss` parameter containing Issuer Identifier … will be added as a query string parameter to `login_url` before redirecting." It calls that configured address the default login route, and lists what triggers it: **cookies disabled** — "Auth0 redirects the user to the application login URI", and "If the application login URI is not set, the redirect is sent to the tenant login URI instead" — a bookmarked login page whose saved state has expired ("Auth0 will redirect to the default client URL if configured, or the tenant level URL if not"; with neither, "Auth0 will render an error page"), and returning from a password reset, an email verification or an organization invitation. It warns that "Sending the user back to the login page can potentially cause a redirect loop", and suggests a landing page that checks for cookies ([Auth0: Configure Default Login Routes](https://auth0.com/docs/authenticate/login/auth0-universal-login/configure-default-login-routes), checked 2026-11-14).

The same shape exists in other providers: one URL is configured to receive a browser the provider cannot help, and if that URL is not a page that starts a login, the user is stranded.

## Why it becomes a dead end

The fallback URL is meant to be one where "`login_url` should point to a route in the application that ends up redirecting to Auth0's `/authorize` endpoint" (same Auth0 page, checked 2026-11-14). A marketing page or a different product's site ignores `iss` entirely — it has no code to read it, and no login to offer — so nothing happens.

The usual cause is age: the tenant's login route was set when the company had one login portal, then the product moved and the setting stayed. Because it is tenant- or application-level configuration, it is invisible in your repository, your deploy and your app's logs.

## How to fix it

1. **Point the fallback at a route you own.** If several applications share the tenant, set it **per application**, not just tenant-wide, so one product's fix does not move the other's fallback.
2. **Make that route restart the login** — read any `returnTo` the configured URL carries (providers preserve query parameters on it) and send the browser back to the provider's authorize endpoint.
3. **Break the loop before it starts.** A browser blocking cookies comes straight back to the same route. Park a marker in `sessionStorage` before redirecting, and on a second arrival show "your browser is blocking the sign-in cookies; allow them or open this in a normal browser" instead of redirecting again.
4. **Keep the value on your own domain.** The fallback is part of the sign-in surface; pointing it at another site is the failure this page is about.

## Check that it is fixed

- Request the authorize URL with no cookies: the redirect chain should now end on your own route, not on another site.
- With cookies allowed in a browser, sign-in completes and the callback appears in the app's logs.
- With cookies blocked, the second arrival shows the explanation, not an endless bounce.

## Related pages

- [A login that loops between your app and the sign-in provider](A-login-that-loops.md): the loop happens after the callback arrives; this page is about it never arriving
- [A sign-in that breaks behind a proxy: the redirect URI](A-sign-in-that-breaks-behind-a-proxy.md): the provider refuses the callback address instead
- [Checking whether a deploy worked](Checking-whether-a-deploy-worked.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Deploy](Glossary.md#deploy), [Host](Glossary.md#host), [Logs](Glossary.md#logs), [Provider](Glossary.md#provider).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-14.

- Auth0, [Configure Default Login Routes](https://auth0.com/docs/authenticate/login/auth0-universal-login/configure-default-login-routes): the `iss` parameter, application versus tenant URI, the scenarios that trigger the redirect, the cookies-disabled loop warning, and the requirement that the login URL route back to `/authorize`
- OpenID Foundation, [OpenID Connect Core 1.0, Initiating Login from a Third Party](https://openid.net/specs/openid-connect-core-1_0.html#ThirdPartyInitiatedLogin): the `iss` parameter and its definition ("Issuer Identifier for the OP that the RP is to send the Authentication Request to")

---

First version written with AI assistance, from a sign-in that dead-ended on a marketing page while debugging a deployed app, and checked against the [sources](#sources) on 2026-11-14. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
