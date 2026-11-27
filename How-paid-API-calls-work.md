---
title: "How paid API calls work"
description: "A paid API names its price before the work with HTTP 402, the caller accepts under a cap, one settlement charges the ledger, and a receipt lets the app check it was paid."
category: Foundations
tags: [costs, security]
order: 5
checked: 2026-11-26
---

<!-- NAV:START -->
[Home](README.md) › [Foundations](Category-Foundations.md) · Tags: [costs](Tag-costs.md), [security](Tag-security.md)
<!-- NAV:END -->

# How paid API calls work

**A paid [API](Glossary.md#api) call names its price before it does the work: the server answers an unpaid request with HTTP 402 Payment Required and a price, the caller retries accepting that price or under a maximum, and the platform settles one charge — from prepaid credit or on a later invoice — with a receipt the app can use to check it was paid.**

The opposite arrangement is to trust the caller, record usage, and bill later: Stripe describes its usage-based billing as a way to "Charge customers based on how much they use your product or service" ([Stripe, Basic usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based), checked 2026-11-26). A paid call moves the agreement into the request itself. A caller that will not or cannot pay does not get the work done, and neither side has to guess what was agreed.

## HTTP reserves 402 but defines no payment format

The 402 status code is part of HTTP, and HTTP says almost nothing about it. RFC 9110 (June 2022) defines it in one sentence: "The 402 (Payment Required) status code is reserved for future use." ([RFC 9110, §15.5.3](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.3), checked 2026-11-26).

The code is standard; the payment scheme is not. Each paid API defines what a price looks like on the wire — a header, a JSON body, or both — so two APIs can both answer 402 and share no header names.

That is also why 402 is not 401. RFC 9110 says 401 means the request "lacks valid authentication credentials for the target resource" ([RFC 9110, §15.5.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.2), checked 2026-11-26). A caller with a valid key and no money should not be told its key is wrong; it should be told the price.

## The first 402 is a quote, not a bill

An unpaid request is the question. The 402 is the answer that states the price, and nothing is charged until the caller comes back accepting it.

Cloudflare's pay per crawl works this way. A protected page answers an AI crawler with `HTTP/2 402 Payment Required` and a `crawler-price` header that "specifies the cost to access the content"; their example shows:

```
HTTP/2 402
crawler-price: USD 0.01
```

The price there is Cloudflare's illustration, not a rate. The feature was "currently in closed beta" when checked, and Cloudflare describes it as a way for site owners to "control and monetize AI crawler access" ([Cloudflare, What is Pay Per Crawl?](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/), and [Crawl pages](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/use-pay-per-crawl-as-ai-owner/crawl-pages/), checked 2026-11-26).

x402 uses the same code with more machinery. It describes itself as "an open, neutral standard for internet-native payments" ([x402.org](https://x402.org), checked 2026-11-26) and, in its README, as "A payments protocol for the internet. Built on HTTP." ([x402 README](https://github.com/coinbase/x402), checked 2026-11-26). The server answers 402 with a base64 `PaymentRequired` object in a `PAYMENT-REQUIRED` header, carrying `PaymentRequirements` the client can choose from by `scheme` and `network`. The client retries with a `PAYMENT-SIGNATURE`, which the server verifies itself or through a facilitator — "A server that facilitates verification and execution of payments for one or many networks." A paid request ends `200 OK` with a `PAYMENT-RESPONSE` header. The project says "Stablecoin payments are the primary use case" ([x402.org](https://x402.org), checked 2026-11-26).

In both designs the price comes from the server, where the price list lives, and travels to the caller before the work starts. A server that accepts the caller's idea of the price is asking to be lied to about the amount owed.

## The caller sets the ceiling

A price list is only safe if the caller can refuse it, so these designs let the caller say no to a price it did not agree to.

Cloudflare lets a crawler answer with one of two headers: `crawler-exact-price` agrees to the exact quoted price and should match the `crawler-price` header, while `crawler-max-price` states "the maximum price the AI crawler is configured to pay for access on any content." If the page costs more than that maximum, the crawler gets another 402 ([Cloudflare, Crawl pages](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/use-pay-per-crawl-as-ai-owner/crawl-pages/), checked 2026-11-26).

x402 puts acceptance in the protocol: the 402 lists several `PaymentRequirements`, and the client picks one it is willing to meet ([x402 README](https://github.com/coinbase/x402), checked 2026-11-26).

A cap turns a pricing mistake or a hostile page into one refused call instead of an empty account. With a maximum, the worst a server can charge for that call is a number the caller set without trusting the server.

## One settlement, once

After acceptance, someone has to move money. There are two common arrangements, and a per-call meter can use either.

**Prepaid credit.** The caller keeps a balance, and each call draws it down. Stripe offers billing credits for this: "prepaid or promotional usage credit allocated through credit grants," which it applies when an invoice finalizes ([Stripe, Billing credits](https://docs.stripe.com/billing/subscriptions/usage-based/billing-credits), checked 2026-11-26). Cloudish (the hosting product made by Hal9, which started this wiki) is a disclosed example of a prepaid platform, not a recommendation: it says its "credits are prepaid and metered per second" and "spend never exceeds the key's balance," and a request to a project with no credit "returns 402 (JSON) instead of starting the container" ([Cloudish, skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), checked 2026-11-26). That last 402 is a refusal, not a quote — the same code doing a different job.

**Invoice after usage.** The caller is trusted, usage is recorded, and a bill follows. Stripe's usage-based billing, which Stripe now points at Metronome as its primary platform, records usage and charges for it after the fact ([Stripe, Basic usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based), checked 2026-11-26).

Cloudflare sits between the two sides as "the Merchant of Record for pay per crawl," and its successful response carries a `crawler-charged` header that "indicates the exact amount that will be billed" ([Cloudflare, What is Pay Per Crawl?](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/) and [Crawl pages](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/use-pay-per-crawl-as-ai-owner/crawl-pages/), checked 2026-11-26).

Whichever arrangement, the ledger has one rule: one call, one charge. A retry carries a reference the platform has already seen, so a repeat is a no-op rather than a second sale; a call whose work failed is not charged at all, or both sides of its settlement are reversed. Those are the two failures to design against.

## The app at the end checks a receipt

When a gateway forwards paid calls to a service, the charge and the work happen in two places. The service must know the call was paid, because a caller that can reach the service directly would otherwise skip the meter.

The gateway can sign a short receipt. A compact JWS, defined by RFC 7515 (May 2015), is three base64url parts — protected header, payload, signature — and the signature covers the first two ([RFC 7515, §3.1](https://www.rfc-editor.org/rfc/rfc7515.html#section-3.1), checked 2026-11-26). The claims should answer four questions: who called, which request, how much was charged, and when the proof stops being valid.

```js
// Verify a compact JWS receipt (HS256) before serving a paid call.
import crypto from "node:crypto";

const [header, payload, signature] = receipt.split(".");
const expected = crypto
  .createHmac("sha256", process.env.METERING_SECRET)
  .update(`${header}.${payload}`)
  .digest();
const given = Buffer.from(signature, "base64url");

if (given.length !== expected.length || !crypto.timingSafeEqual(given, expected)) {
  res.writeHead(402).end(); // no valid receipt: not a paid call
  return;
}

const claims = JSON.parse(Buffer.from(payload, "base64url"));
if (claims.exp * 1000 <= Date.now()) {
  res.writeHead(402).end(); // the proof has expired
  return;
}
```

Use the verified claims — not a header the caller controls — to identify the caller. Compare the claims' method and path with the request in front of you, so a receipt for one cheap call cannot authorize an expensive one. And note the trade-off in the example: with a shared HS256 [secret](Glossary.md#secret), the service can also mint receipts. If the service is not fully trusted, use an asymmetric signature instead, where the platform signs and the service verifies with a public key.

## What the design has to refuse

- Serving the work before both sides agree on the price.
- Charging for a failed, refused or timed-out call; if settlement already ran, reverse it for both the caller and the provider.
- Trusting a price or a cap that arrives in a caller-set header. The price comes from the price list; the cap comes from the caller's own configuration.
- Charging twice when a client retries. One reference per logical call, and a repeat of a reference is a no-op.
- Letting the service skip the receipt because the gateway is "always" in front. The service's own address is reachable too.
- Answering a missing credential with 402. That is 401's job, and a client that sees 402 may retry with money instead of fixing its key.

## The shape in five steps

1. The caller sends the request without payment.
2. The server answers 402 with the price and what it buys.
3. The caller retries with acceptance — the exact price or a maximum.
4. The server checks the balance or quota, does the work, settles one charge, and returns the result with a receipt.
5. If the work fails after settlement, reverse it; if the caller retries, reuse the reference so the ledger charges once.

## Related pages

- [The cloud, for AI apps](Cloud-for-AI-apps.md): the three jobs you pay for, and how idle and always-on apps are billed.
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md): where costs enter the build-and-deploy workflow.
- [Where your keys come from](Where-your-keys-come-from.md): recording who is calling when agents sign up instead of people.
- [Security for AI apps and agents](Security-for-AI-apps.md): runaway costs as one of the risks specific to agent apps.
- [Why a page can't read another site's API, and how to serve it from your own](Fetching-an-API-from-your-page.md): what changes when the caller is a browser page.

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Container](Glossary.md#container), [Provider](Glossary.md#provider), [Secret](Glossary.md#secret).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-26.

- IETF, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html) (June 2022): the definitions of 402 (§15.5.3) and 401 (§15.5.2)
- IETF, [RFC 7515: JSON Web Signature (JWS)](https://www.rfc-editor.org/rfc/rfc7515.html) (May 2015): compact serialization and what the signature covers
- Cloudflare, [What is Pay Per Crawl?](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/what-is-pay-per-crawl/) and [Crawl pages](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/use-pay-per-crawl-as-ai-owner/crawl-pages/): the 402 with `crawler-price`, the two acceptance headers, `crawler-charged`, and the closed-beta status
- x402, [x402.org](https://x402.org) and [README](https://github.com/coinbase/x402): the standard's description, the `PAYMENT-REQUIRED` / `PAYMENT-SIGNATURE` / `PAYMENT-RESPONSE` flow, and the facilitator
- Stripe, [Basic usage-based billing](https://docs.stripe.com/billing/subscriptions/usage-based) and [Billing credits](https://docs.stripe.com/billing/subscriptions/usage-based/billing-credits): post-paid metering and prepaid credit grants
- Cloudish, [skill.md](https://cloudish.ai/skill.md?ref=cc-wiki): the disclosed prepaid example and its 402 on an out-of-credit project

---

First version written with AI assistance, from a session that documented a paid-call gateway, and checked against the [sources](#sources) on 2026-11-26. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
