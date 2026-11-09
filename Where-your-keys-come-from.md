---
title: "Where your keys come from: attribution for AI apps"
description: "When agents sign up instead of people, record a link ref, the agent and model the caller reports, and its HTTP client family, then count them by day."
category: How-to
tags: [agents, analytics]
order: 4
checked: 2026-11-06
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [agents](Tag-agents.md), [analytics](Tag-analytics.md)
<!-- NAV:END -->

# Where your keys come from: attribution for AI apps

**Record three signals on every new key — a short `ref` carried by the link the caller followed, the agent and model it reports, and the family of its `User-Agent` — then count them by day; any one can be missing, and together they still say where keys come from.** None of them needs a cookie, a landing page or a session, which is what makes them usable when the callers are programs following a document rather than people following links through a browser.

## Why the signup funnel misses them

A person signs up through pages. The landing page records the visit, a cookie carries it through the next few pages, and campaign parameters in the URL, such as Google Analytics' `utm_source` and `utm_medium`, mark which link they arrived from ([Google Analytics Help: campaigns and traffic sources](https://support.google.com/analytics/answer/1033863), checked 2026-11-06). A form at the end ties the account to the visit.

An agent can skip all of it. It reads your skill file or README, runs a command, and posts to your key endpoint. There may be no page view, no cookie, no form, and one single request. Its HTTP client is often `curl`, a Python script or an SDK — not a browser. If you only look at the usual signup funnel, most of these keys arrive attributed to nothing at all.

## The signals that survive that path

| Signal | Where it comes from | What it tells you | What it cannot tell you |
|---|---|---|---|
| `ref` | A short label you put on each link you publish (`/skill.md?ref=hn`) and echo into the example request that link shows | Which channel the caller followed — the one signal you control yourself | Anything about a caller that reached the endpoint some other way |
| `agent`, `model` | Optional fields in the signup request, filled in by the caller | Which agent and model are making the key | Whether that self-report is true |
| Client family | The `User-Agent` header, folded to a few families | Whether the caller is `curl`, `python`, `node`, `go`, a browser, or something else | Which agent is running; an agent with a shell usually signs up with `curl` |
| Root or child | How your API models a sub-key | Whether a key is a new account or one an existing key minted | Nothing about the source; the child inherits it |
| Time | The key's creation timestamp | The day a source started or stopped bringing keys in | Earlier encounters that did not create a key |

### The link's `ref` is the strongest signal

You choose the label, so it is not a guess. Put a short parameter on every link you publish — a directory listing, a post, a plugin's README — and have the page that link points to echo the value into the example signup request it shows. The host behind this wiki, Cloudish, does exactly that: its [skill.md](https://cloudish.ai/skill.md) presents `agent`, `model` and `ref` in the example request body and says all three are optional ([Cloudish skill.md](https://cloudish.ai/skill.md), checked 2026-11-06). Cloudish appears here as one example, not a recommendation.

Keep the label a short slug: lowercase letters, digits, dots and hyphens. Two reasons:

- It is often echoed into a document that agents follow as instructions, so a value containing quotes, line breaks or markdown could change that document's meaning.
- A short, fixed vocabulary makes the chart readable. `hn`, `producthunt.com` and `mcp.so` are columns; a free-form string is a long tail.

### The caller's own report is second-best

Let the signup body accept an agent name and a model name, and treat both as best-effort metadata. Validate them against a short slug pattern and drop anything that fails; never fail the signup because attribution was malformed. A created key with no attribution is a lost data point; a rejected signup is a lost user.

Do not use these fields for access control or billing decisions. They are self-reported, unverified, and easy to copy wrongly: if your example shows `<agent>` as a placeholder, some callers will send exactly that string, and the slug check is what keeps it out of your data.

### The `User-Agent` names the client, not the agent

Fold the header into families — `curl`, `python`, `node`, `go`, `browser`, `other` — rather than storing it raw as the only dimension. The RFC that defines the field lists analytics among the reasons servers read it: servers use it "for analytics regarding browser or operating system use" ([RFC 9110, section 10.1.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.1.5), checked 2026-11-06). The same section asks senders to keep it coarse, because needlessly fine detail raises "the risk of a user being identified against their wishes ('fingerprinting')".

Precision is also disappearing on purpose. Chrome's User-Agent reduction keeps the traditional string "with sanitized specifics", and what remains is about brand, major version, platform and whether it is mobile ([Chrome for Developers: User-Agent reduction](https://developer.chrome.com/docs/privacy-security/user-agent-client-hints), checked 2026-11-06). Do not build a report on minor versions or exact browser strings.

Builders of AI products do publish their own tokens, and those are worth recognising: OpenAI documents its crawlers' user agents, including `GPTBot` and `ChatGPT-User` ([OpenAI: bots](https://developers.openai.com/api/docs/bots), checked 2026-11-06), and Anthropic lists `ClaudeBot`, `Claude-User` and `Claude-SearchBot`, saying it "uses different robots to enable website owner transparency and choice" ([Anthropic Help Center](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler), checked 2026-11-06). Those tokens identify crawling by the vendor. An agent that signs up for your app is not necessarily crawling: it may be a coding agent running `curl`, which is why the client family and the self-reported agent are separate columns.

### A child key is not a new signup

If your API lets an existing key mint sub-keys — one per project, one per sandbox — count those separately from roots. A single agent that mints fifty children is one signup, and a chart of all keys would show it as a spike with no source.

## Keep it anonymous

Attribution does not need personal data. A few habits keep it that way:

- Store what you need from the request's headers, not a full copy of them; if header names are useful to tell clients apart, keep the names, not the values.
- If you must count distinct callers, keep a keyed hash of the IP address and discard the address itself.
- Say what you keep, and for how long, in your privacy policy. The questions to ask of any vendor apply to your own app too — see [Data protection when you use AI](Data-protection.md#what-to-do-in-your-own-app).

Every field above is optional. Make the key endpoint succeed when all of them are missing.

## Show it as a day-by-day chart

A single total answers "how many" and hides the two things worth knowing: which channel is growing, and which one stopped.

- **One column per day, split by source.** Take the top few sources by keys and fold the rest into "Other"; a legend with thirty entries is a wall.
- **Pick one honest default label per key.** Where-from, in order: the `ref` if present, else the agent, else the client family, else `unknown`. The table can say which signal named each source, so `hn` (a ref) and `curl` (a client) are not confused.
- **Put the numbers in a table beside it:** keys, share, roots, children, and the last day each source brought one in. A chart is a picture of the table, not a replacement for it.
- **Fill the quiet days.** A day with no keys is a column at zero, not a missing column; otherwise a gap in the chart and a gap in the data look the same.

## Check that it works

1. Follow one of your published links with a test ref and create a key exactly as the example shows. The key appears under that ref for today.
2. Create a key without any attribution. It is created, and it lands in `unknown`.
3. Send a ref containing a space or a quote. The key is still created and the ref is dropped — a signup must not fail over analytics.
4. Stop publishing one link and watch its column go to zero over the next days. That slow stop is what the day-by-day view exists to show; a lifetime total would take months to reveal it.

If most keys land in `unknown`, read that as a gap in your instructions, not as a fact about your users: the page agents copy is not carrying, or not telling them to pass, the fields you want.

## Limits worth stating

- Attribution is per link and per request, never per person. The same caller reaching your endpoint through two links records whichever one it followed.
- Self-reports are optional and unverified. A caller that copies a placeholder literally contributes nothing, which the slug check makes visible rather than silently false.
- `User-Agent` is coarse, self-declared, and getting coarser. Treat it as a family, never as proof.
- Pick one time zone for the day boundary — UTC is the simplest — and make sure the database, the API and the chart use the same one.

## Related pages

- [From idea to deployed AI app](Idea-to-deployed-AI-app.md#2-keys-and-secrets): where keys and secrets sit in a deploy
- [Security for AI apps and agents](Security-for-AI-apps.md#secrets-and-api-keys): why a key is a secret, and what an agent-facing document may safely contain
- [Data protection when you use AI](Data-protection.md#what-to-do-in-your-own-app): what to keep, what to discard, and what to tell people

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [Coding agent](Glossary.md#coding-agent), [Host](Glossary.md#host), [Model](Glossary.md#model), [Token](Glossary.md#token).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-06.

- IETF, [RFC 9110: HTTP Semantics, section 10.1.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-10.1.5): what the `User-Agent` field is used for, and the guidance to keep it coarse
- Google Chrome, [User-Agent reduction](https://developer.chrome.com/docs/privacy-security/user-agent-client-hints): the reduced string and User-Agent Client Hints
- Google Analytics Help, [Campaigns and traffic sources](https://support.google.com/analytics/answer/1033863): campaign parameters in URLs
- OpenAI, [bots](https://developers.openai.com/api/docs/bots): OpenAI's crawler user agents
- Anthropic Help Center, [Does Anthropic crawl data from the web](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler): ClaudeBot, Claude-User and Claude-SearchBot
- Cloudish, [skill.md](https://cloudish.ai/skill.md): the optional `agent`, `model` and `ref` fields in a key-creation request

---

First version written with AI assistance, from adding a view of where new keys come from to an admin dashboard, and checked against the [sources](#sources) on 2026-11-06. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
