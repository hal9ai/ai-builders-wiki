---
title: "A sign-in that breaks behind a proxy: the redirect URI"
description: "The provider says the redirect URI does not match, or the callback address comes out as 'https,http://example.com': why a forwarded header can carry a list of values, and how to build the address safely."
category: Problems & solutions
tags: [auth, hosting]
order: 3
checked: 2026-11-09
---

<!-- NAV:START -->
[Home](README.md) › [Guides](Category-Guides.md) · Tags: [auth](Tag-auth.md), [hosting](Tag-hosting.md)
<!-- NAV:END -->

# A sign-in that breaks behind a proxy: the redirect URI

**If your app sits behind a proxy and sign-in fails with a redirect-URI error, the app is probably computing its public address from a forwarded header that can carry more than one value, so the callback address comes out as `https,http://app.example.com/auth/callback`.** Build the redirect URI from a configured public address instead, or parse the header as a comma-separated list and take the first value.

## What it looks like

- The sign-in provider shows an error such as "redirect_uri mismatch", "Invalid redirect_uri" or "Callback URL mismatch".
- The provider's error page shows the address your app sent, with a comma in the scheme: `https,http://app.example.com/auth/callback`. In the URL it is encoded as `https%2Chttp%3A%2F%2Fapp.example.com%2Fauth%2Fcallback`.
- Sign-in works when you open the app at its local address and fails at the public one, or the reverse.
- If the app ignores the provider's error, the sign-in looks like an endless bounce: see [A login that loops between your app and the sign-in provider](A-login-that-loops.md).

## Why the address has to be exactly right

In the OAuth authorization code flow the app sends the user to the provider and names a redirect URI: where the provider may send the user back. The provider only accepts an address it knows. RFC 6749 says "the redirection endpoint URI MUST be an absolute URI", and the authorization server "MUST compare and match the value received against at least one of the registered redirection URIs" ([RFC 6749, section 3.1.2](https://www.rfc-editor.org/rfc/rfc6749#section-3.1.2), checked 2026-11-09). When a full URI is registered, the comparison is "using simple string comparison as defined in [RFC3986] Section 6.2.1" ([RFC 6749, section 3.1.2.3](https://www.rfc-editor.org/rfc/rfc6749#section-3.1.2.3), checked 2026-11-09).

Simple string comparison means small differences count. `https://app.example.com/auth/callback` and `https://app.example.com/auth/callback/` are two different strings. So is `https,http://app.example.com/auth/callback`.

## Where the wrong scheme comes from

Your app usually listens on plain HTTP on a private address, such as `http://localhost:3000`. The proxy in front accepts HTTPS from the public and forwards the request over HTTP. If the app builds links from the request it receives, it sees `http` and an internal host, neither of which is the address the user is on.

Proxies add headers for exactly this. `X-Forwarded-Proto` carries the original scheme, `X-Forwarded-Host` the original host, and `X-Forwarded-For` the original address. MDN calls `X-Forwarded-Proto` "a de-facto standard header for identifying the protocol (HTTP or HTTPS) that a client used to connect to a proxy or load balancer", with the syntax `X-Forwarded-Proto: <protocol>` — a single value ([MDN, X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto), checked 2026-11-09).

It is "de-facto" because the header was never standardised. RFC 7239 instead defines a standard header called `Forwarded`, "an HTTP extension header field that allows proxy components to disclose information lost in the proxying process", written like `Forwarded: for=192.0.2.60;proto=http;by=203.0.113.43` ([RFC 7239](https://www.rfc-editor.org/rfc/rfc7239), checked 2026-11-09). Most proxies still add the `X-Forwarded-*` headers, and many apps read only those.

## Why the header can hold a list

A request can pass through more than one proxy: a CDN, then a load balancer, then the app's own reverse proxy. Each may append its own value to the same header. Microsoft's documentation for ASP.NET Core says of `X-Forwarded-Proto`: "The value might also be a list of schemes if the request has traversed multiple proxies" ([Microsoft Learn, proxy servers and load balancers](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer), checked 2026-11-09). Django's documentation says the same from the other side: the proxy should strip `X-Forwarded-Proto` from incoming requests "even when it contains a comma-separated list of protocols" ([Django settings, `SECURE_PROXY_SSL_HEADER`](https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header), checked 2026-11-09).

So a header like this is not corruption; it is two hops reporting:

```
X-Forwarded-Proto: https,http
```

Values are conventionally appended in the order the request travelled, so the first describes the connection nearest the user. The standardised `Forwarded` header says this outright: "The first element in this list holds information added by the first proxy that implements and uses this header field", and "each subsequent element holds information added by each subsequent proxy" ([RFC 7239, section 4](https://www.rfc-editor.org/rfc/rfc7239#section-4), checked 2026-11-09).

An app that treats the whole header as one string gets the scheme `https,http`, builds `https,http://app.example.com/auth/callback`, and sends that as `redirect_uri`. The provider sees a URI that is not absolute and does not match the registered one, so it refuses. The one-time code and PKCE never come into it: the request is rejected before the user signs in.

## How to confirm it in a minute

- Log the redirect URI your app builds, and the full URL it sends the browser to. In the query string, `%2C` is a comma.
- Ask the app what it sees. Send a request to your own development server with a made-up two-value header and see what address comes back: `curl -H 'X-Forwarded-Proto: https,http' http://localhost:3000/`.
- Compare the address sent with the one registered at the provider: scheme, host, port, path and trailing slash.

If the provider's error page names a `redirect_uri` that looks correct, the problem is elsewhere — see [A login that loops between your app and the sign-in provider](A-login-that-loops.md).

## How to fix it

1. **Do not derive the redirect URI from the request.** Set the public address once, as an [environment variable](Glossary.md#environment-variable) such as `PUBLIC_URL=https://app.example.com`, and build the callback address from it. The same string goes out on every request, so it can be registered once and checked once. It also keeps working when the proxy configuration changes or when several proxies disagree.
2. **If you do read the header, read it as a list.** Split on commas, take the first value and trim it, for the scheme and for the host. Accept only `http` or `https` and reject anything else rather than passing it into a URL.
3. **Trust the header only from your own proxy.** A client can send `X-Forwarded-Proto: https` itself. If the app believes it, that client influences the redirect URI and every link the app generates. Have your proxy overwrite or strip incoming copies. Django's documentation is explicit: "You should only set this setting if you control your proxy or have some other guarantee that it sets/strips this header appropriately" ([Django settings, `SECURE_PROXY_SSL_HEADER`](https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header), checked 2026-11-09).
4. **Keep the registered redirect URI exact.** After all of the above, the string sent and the string registered must be identical. If the provider supports several registered URIs or wildcards, prefer exact ones and use one per environment (local, staging, production).

## Check that it is fixed

- Sign in from the public HTTPS address: the provider request carries `redirect_uri=https%3A%2F%2Fapp.example.com%2Fauth%2Fcallback`, with no `%2C`.
- The callback reaches the app, the code is exchanged, and you land signed in.
- Send the app a header with two values again: the address it builds is the same as before.

## Related pages

- [A login that loops between your app and the sign-in provider](A-login-that-loops.md): the same redirect, when the app throws the code away
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md#4-deploy): where sign-in and environment settings sit in a deploy
- [The cloud, for AI apps](Cloud-for-AI-apps.md#1-hosting-the-app): what a host puts in front of your app

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Environment variable](Glossary.md#environment-variable), [Host](Glossary.md#host), [Provider](Glossary.md#provider).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-09.

- IETF, [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749): section 3.1.2 (redirection endpoint) and 3.1.2.3 (registration requirements)
- IETF, [RFC 3986: Uniform Resource Identifier (URI): Generic Syntax](https://www.rfc-editor.org/rfc/rfc3986): section 6.2.1, simple string comparison
- IETF, [RFC 7239: Forwarded HTTP Extension](https://www.rfc-editor.org/rfc/rfc7239): the `Forwarded` header field, the `proto=` parameter, and the order of elements in section 4
- MDN, [`X-Forwarded-Proto`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-Proto): description and syntax
- Microsoft Learn, [Configure ASP.NET Core to work with proxy servers and load balancers](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer): the forwarded-headers table, including the list-of-schemes sentence
- Django, [Settings: `SECURE_PROXY_SSL_HEADER`](https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header): why the header is trusted, and the comma-separated case

---

First version written with AI assistance, from a sign-in that failed behind a proxy while deploying a web app, and checked against the [sources](#sources) on 2026-11-09. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
