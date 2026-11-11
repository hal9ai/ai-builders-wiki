---
title: "Serve one custom domain from more than one datacenter"
description: "One hostname for an app that runs in several datacenters: point the domain at one entry point that looks up which datacenter holds each name, and forward the rest with the Host header kept."
category: How-to
tags: [hosting]
order: 5
checked: 2026-11-10
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md)
<!-- NAV:END -->

# Serve one custom domain from more than one datacenter

**Use one public entry point: it looks up which datacenter holds each name and forwards every request it does not hold itself, keeping the original `Host` header.**

An app can run in several datacenters and still be reached at one name, `app.example.com`. DNS sends a connection to one address, so give that address to a single entry point and let it decide where each request goes. Pointing a hostname at several datacenters with DNS round-robin does not work on its own: a request can land on a datacenter that does not hold that app. HTTP keeps the name in a header instead, so a router can use it.

## Why the `Host` header is the key

An HTTP request carries the hostname the client asked for in the `Host` header (in HTTP/2 and HTTP/3, sometimes the `:authority` pseudo-header). RFC 9110 describes it as the way a server tells requests for different names apart:

> "The "Host" header field in a request provides the host and port information from the target URI, enabling the origin server to distinguish among resources while servicing requests for multiple host names."

That is why an entry point can receive a request for `app.example.com`, notice that this datacenter does not hold that name, open a connection to the datacenter that does, and repeat the request **with the same `Host` header**. To the app, the request still arrived at `app.example.com`. Cookies, sign-in callbacks and absolute redirects keep working because the app only ever sees one origin.

## What the entry point does

1. Read the hostname from the request.
2. Look it up in a small name service that records which datacenter holds it.
3. If this datacenter holds it, serve it locally.
4. Otherwise, forward the request to the datacenter that does, keeping `Host`.
5. If the lookup finds nothing, answer 404 rather than guessing.

The name service can be tiny: a table of name to datacenter, written when an app is created and read on each request (cached briefly). It does not need to be in the request path for the app itself, only for picking the datacenter.

## One wildcard per ingress controller

Routers choose a backend by matching the request's host. In Kubernetes, an Ingress rule can name a precise host or a wildcard, and a wildcard covers exactly one DNS label:

> "Hosts can be precise matches (for example "`foo.bar.com`") or a wildcard (for example "`*.foo.com`"). Precise matches require that the HTTP `host` header matches the `host` field. Wildcard matches require the HTTP `host` header is equal to the suffix of the wildcard rule."
>
> "`*.foo.com` ... `baz.bar.foo.com` ... No match, wildcard only covers a single DNS label"

Traefik's `Host` matcher follows the same idea, and its default priority is the length of the rule:

> "The `Host` and `HostRegexp` matchers allow matching requests that are targeted to a given host."
>
> "To avoid path overlap, routes are sorted, by default, in descending order using rules length."

Two datacenters in **separate clusters** can each run their own ingress controller and each own a `*.example.com` rule. Two datacenters in the **same cluster** share one ingress controller: two identical wildcard rules match the same requests, and Traefik says to set a priority when overlapping routes need a fixed winner. The simpler rule is to let one datacenter own the wildcard and reach the other over the cluster's private network, using its internal service address instead of a public hostname.

## Where a forwarded request connects

- **Another cluster:** forward to a per-datacenter hostname, such as `app.dc2.example.net`. That hostname needs its own DNS record and a certificate that covers it. A wildcard certificate is the usual way to cover every app, and Let's Encrypt issues wildcard certificates only through the DNS-01 challenge: "It also allows you to issue wildcard certificates," while HTTP-01 "cannot be used to issue wildcard certificates."
- **The same cluster:** connect to the other datacenter's internal service address, which needs no public DNS record and no extra certificate.

## Tell the app the original scheme

Forwarding over a private network is often plain HTTP even though the visitor used HTTPS. Proxies report the original protocol in `X-Forwarded-Proto`, which is a de facto header rather than a standard one:

> "The HTTP `X-Forwarded-Proto` (XFP) request header is a de-facto standard header for identifying the protocol (HTTP or HTTPS) that a client used to connect to a proxy or load balancer."
>
> "Not part of any current specification. The standardized version of this header is `Forwarded`."

The app has to trust that header (usually a "trust proxy" setting in the web framework), or it will build `http://` redirects and think secure cookies are not secure. The standardized `Forwarded` header carries the same information: "The "Forwarded" HTTP header field is an OPTIONAL header field that, when used, contains a list of parameter-identifier pairs that disclose information that is altered or lost when a proxy is involved in the path of the request."

## Stop forwarding loops

Mark each forwarded request with a value only your datacenters know, and count the hops. Allow the small number of hops your topology needs (for example, a chain of two datacenters) and refuse anything beyond it. Without the count, two datacenters whose name tables briefly disagree can send the same request back and forth until it times out. Strip the marker and the count before the request reaches the app, so an app cannot set them.

## Checklist

- One public entry point owns `*.example.com`.
- A name service answers "which datacenter holds this name?".
- Forwarded requests keep `Host`; the app is told the original scheme.
- A co-located datacenter is reached over the private network, not back through the public wildcard.
- A separate-cluster datacenter has DNS and a certificate for its forward hostname.
- Forwarded requests carry a shared marker and a hop count, and the count is enforced.

## Related pages

- [From idea to deployed AI app: a typical workflow](Idea-to-deployed-AI-app.md)
- [How to shrink a container image](Container-image-size.md)
- [A login that loops between your app and the sign-in provider](A-login-that-loops.md)

## Sources

All checked on 2026-11-10.

- IETF, [RFC 9110: HTTP Semantics, section 7.2 "Host and :authority"](https://www.rfc-editor.org/rfc/rfc9110.html#section-7.2)
- IETF, [RFC 7239: Forwarded HTTP Extension](https://www.rfc-editor.org/rfc/rfc7239.html)
- Kubernetes, [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/)
- Traefik, [Rules & Priority](https://doc.traefik.io/traefik/v3.8/reference/routing-configuration/http/routing/rules-and-priority/)
- Let's Encrypt, [Challenge Types](https://letsencrypt.org/docs/challenge-types/)
- MDN, [`X-Forwarded-Proto`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-Proto)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-10. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
