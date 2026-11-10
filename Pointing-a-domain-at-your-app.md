---
title: "How to point a domain at your app, with one record for every subdomain"
description: "Point one wildcard DNS record at your app's server so every app subdomain resolves without its own record, and one wildcard certificate covers them for HTTPS."
category: How-to
tags: [hosting, basics]
order: 5
checked: 2026-11-10
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md), [basics](Tag-basics.md)
<!-- NAV:END -->

# How to point a domain at your app, with one record for every subdomain

**Point one wildcard DNS record at the server that answers for your app, and every `{name}.example.com` resolves there without a record per app.** Add one wildcard certificate for HTTPS, and the same record covers every subdomain at that level.

This is worth writing down when the app hands out a name per user, per project, or per region. At that point the number of names is unbounded, and a DNS record per name is the wrong shape: it needs a write whenever an app appears, and another whenever one moves.

## The three records

For one server that answers `example.com` and every `{name}.example.com`:

```
example.com        A       203.0.113.10
www.example.com    CNAME   example.com
*.example.com      A       203.0.113.10
```

**An A record maps a name to an IP address, and a CNAME maps one name to another name** ([Cloudflare, DNS record types](https://developers.cloudflare.com/dns/manage-dns-records/reference/dns-record-types/), checked 2026-11-10). The `www` CNAME follows the apex if the server's address changes; the wildcard points at the address itself.

The `*` is the point: it is one record, and a new app subdomain needs no DNS change at all.

If the app also gives out names under a region, `{name}.sea.example.com`, create `*.sea.example.com` pointed at that region's server. On Cloudflare a wildcard record is multi-level and would answer the deeper name anyway ([Cloudflare, wildcard DNS records](https://developers.cloudflare.com/dns/manage-dns-records/reference/wildcard-dns-records/), checked 2026-11-10), but HTTPS needs a certificate for that level too, so plan one wildcard per level you actually serve.

## What the wildcard matches, and what wins over it

- **Specific records take precedence.** A wildcard "applies only when no exact record exists at the queried name", so `admin.example.com` can point elsewhere while everything else falls to the wildcard ([wildcard DNS records](https://developers.cloudflare.com/dns/manage-dns-records/reference/wildcard-dns-records/), checked 2026-11-10).
- **The `*` occupies one whole first label.** "Wildcards are only supported on the first label": `*.example.com` is a wildcard, while `sub.*.example.com` is not, and in `*.*.example.com` only the first asterisk is wild (same source).
- **Cloudflare's wildcards match several levels.** "Wildcards are multi-level by default", so `*.example.com` also answers `a.b.example.com` unless a more specific record exists (same source). A TLS wildcard certificate does not work that way, as the next section shows.

## DNS-only, or through the provider's proxy

**Choose DNS-only unless you want the DNS provider to handle the traffic as well.** Cloudflare offers two modes for a record: proxied, where a lookup "will be answered with Cloudflare anycast IP addresses" and Cloudflare "sits between your visitors and your server"; and DNS-only, where it "will be answered with the actual origin IP address" ([Cloudflare, proxy status](https://developers.cloudflare.com/dns/proxy-status/), checked 2026-11-10). Cloudflare says DNS-only is "only recommended for records that do not serve web traffic", because proxying is what adds its DDoS protection, caching and rules.

For an app host the choice is architectural, not cosmetic:

- **DNS-only** lets the browser's connection reach your server, which presents its own certificate and applies its own limits. That is what you want when the server is the thing you are testing, and it makes your wildcard certificate the one the browser sees.
- **Proxied** has the provider terminate HTTPS and cache, filter and limit requests before your server. That can be useful, but now two systems must agree on hostnames, certificates and request sizes for every app.

Either mode works for the names above. What matters is choosing one on purpose, because the two put different systems in charge of the certificate and the request.

## One certificate for every subdomain

**A certificate for `*.example.com` covers every single-label subdomain, but not `example.com` itself and not `a.b.example.com`.** RFC 6125's matching example is that `*.example.com` "would match foo.example.com but not bar.foo.example.com or example.com" ([RFC 6125, section 6.4.3](https://www.rfc-editor.org/rfc/rfc6125#section-6.4.3), checked 2026-11-10). If the app needs its bare domain or a two-level name, put those names on the certificate explicitly, or issue a second wildcard for the deeper level.

A wildcard certificate cannot be validated with the usual HTTP-01 challenge. Let's Encrypt says wildcard issuance "must use the DNS-01 challenge" ([Let's Encrypt FAQ](https://letsencrypt.org/docs/faq/), checked 2026-11-10); in its list of challenge types, HTTP-01 "cannot be used to issue wildcard certificates" and TLS-ALPN-01 "cannot be used to validate wildcard domains" ([Let's Encrypt, challenge types](https://letsencrypt.org/docs/challenge-types/), checked 2026-11-10). DNS-01 proves control by publishing a TXT record, so the certificate tool needs an API token for the DNS provider — often the same account and token that creates the records above.

The payoff is one certificate and one renewal path for every app name. Renewal repeats the same DNS-01 exchange, so after the first setup nothing is manual.

## A second server, or a region

1. Add `sea.example.com` A, `www.sea.example.com` CNAME `sea.example.com`, and `*.sea.example.com` A to the new server. Do it before its first deploy, so the names resolve when certificates are requested and when the first request arrives.
2. Leave the primary records alone. Each region's wildcard covers its own names, and a name outside a region still falls to the global wildcard.
3. To move the global apps with one edit later, point the global wildcard at an alias instead of an address: `*.example.com CNAME active.example.com`, with `active.example.com` an A record at the current server. One edit to `active` moves the fleet. Keep its TTL short, because resolvers keep the old answer until it expires; Cloudflare's Auto TTL is 300 seconds ([Cloudflare, TTL](https://developers.cloudflare.com/dns/manage-dns-records/reference/ttl/), checked 2026-11-10).

## Check it

```sh
for h in example.com www.example.com app.example.com; do
  printf '%-24s ' "$h"; dig +short "$h" A
done

# The alias behind www, if you used a CNAME
dig +short www.example.com CNAME
```

Each name should return the server's IP address, and `www` should show its CNAME target followed by that address. A name that returns nothing is missing or misspelled in the zone. A name that returns an old address is being answered from a cache until its TTL runs out.

## Related pages

- [The cloud, for AI apps](Cloud-for-AI-apps.md)
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Deploy](Glossary.md#deploy), [Host](Glossary.md#host), [Provider](Glossary.md#provider), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-10.

- Cloudflare, [Wildcard DNS records](https://developers.cloudflare.com/dns/manage-dns-records/reference/wildcard-dns-records/); [Proxy status](https://developers.cloudflare.com/dns/proxy-status/); [DNS record types](https://developers.cloudflare.com/dns/manage-dns-records/reference/dns-record-types/); [TTL](https://developers.cloudflare.com/dns/manage-dns-records/reference/ttl/)
- Let's Encrypt, [Challenge types](https://letsencrypt.org/docs/challenge-types/); [FAQ](https://letsencrypt.org/docs/faq/)
- IETF, RFC 6125, [Representing and Matching Domain-Identified Applications](https://www.rfc-editor.org/rfc/rfc6125#section-6.4.3)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-10. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
