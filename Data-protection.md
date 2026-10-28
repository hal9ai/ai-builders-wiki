---
title: "Data protection when you use AI"
description: "The five questions to ask any AI vendor, consumer vs business terms, and what to do in your own app."
category: Security and data
tags: [privacy, providers, security]
order: 2
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Security and data](Category-Security-and-data.md) · Tags: [privacy](Tag-privacy.md), [providers](Tag-providers.md), [security](Tag-security.md)
<!-- NAV:END -->

# Data protection when you use AI

**What happens to the text you send an AI [model](Glossary.md#model) depends less on the vendor than on the plan: consumer chat apps often train on your conversations unless you opt out, while business and [API](Glossary.md#api) terms usually do not, and keep data for a limited time.** This page explains what to ask; [Data protection by vendor](Data-protection-by-vendor.md) compares the answers, vendor by vendor, with sources.

**This is not legal advice.** It summarizes public vendor pages to help you ask the right questions. Policies change often, your contract may say something different, and laws such as the GDPR put obligations on *you* as the app maker. For a real decision, read the current terms and ask a lawyer or your data protection officer.

## The questions that matter

Before you send personal or confidential data to a model, ask five questions, for the exact plan you use:

1. **Training.** Does the vendor use my [prompts](Glossary.md#prompt) and answers to train its models by default?
2. **Opt-out.** If yes, can I turn it off, and how?
3. **Retention.** How long does it keep my data, including after I delete it, and when content is flagged for abuse review?
4. **[Zero data retention](Glossary.md#zero-data-retention-zdr) (ZDR).** Can I arrange for nothing to be stored, and who qualifies?
5. **Location.** Where is the data processed and stored? Can I keep it in the EU?

The answers for each major vendor are in the [comparison table](Data-protection-by-vendor.md#comparison-table).

## Consumer vs business terms

**The same vendor usually has two sets of rules: consumer terms for individual chat-app plans, and commercial terms for business plans and the API.** Anthropic, for example, says its 2025 consumer-terms update applies "to users on our Claude Free, Pro, and Max plans" and does "not apply to services under our Commercial Terms", which cover Claude for Work, the API and access through Amazon Bedrock and Google Cloud ([Anthropic, Updates to our consumer terms](https://www.anthropic.com/news/updates-to-our-consumer-terms), checked 2026-10-28).

In practice: if your employees paste customer data into a personal chat-app account, the consumer rules apply, whatever your company's API contract says.

## What to do in your own app

- **Use business or API terms for anything involving other people's data**, not a personal chat-app account.
- **Check the default, not just the option.** "You can opt out" is different from "off by default".
- **Retention is not zero just because training is off.** Most APIs keep data for abuse monitoring, often around 30 days, unless you have a ZDR arrangement.
- **Location is a setting, and sometimes a contract.** EU processing usually means choosing a region or endpoint, and sometimes an approval.
- **Same model, different terms.** A model through a cloud platform (Bedrock, Vertex AI, Foundry) follows that platform's terms. See [providers and models](AI-providers-and-models.md#where-you-can-get-them).
- **Tell your users.** Your privacy notice should say which AI [providers](Glossary.md#provider) receive their data and why.
- **Send less.** Strip names, emails and IDs before the model call when the task does not need them, and do not log full inputs ([logs](Idea-to-deployed-AI-app.md#5-read-the-logs)).

## Related pages

- [Data protection by vendor](Data-protection-by-vendor.md): the comparison table
- [Security for AI apps](Security-for-AI-apps.md)
- [AI providers and models](AI-providers-and-models.md)
- [Ways to use AI](Ways-to-use-AI.md): chat apps vs API

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Cloud](Glossary.md#cloud), [Logs](Glossary.md#logs), [Model](Glossary.md#model), [Prompt](Glossary.md#prompt), [Provider](Glossary.md#provider), [Zero data retention (ZDR)](Glossary.md#zero-data-retention-zdr).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28.

- Anthropic, [Updates to our consumer terms](https://www.anthropic.com/news/updates-to-our-consumer-terms)
- Vendor pages for every other claim: see [Data protection by vendor](Data-protection-by-vendor.md#sources)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Not legal advice. Found a mistake? [Open an issue](CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](LICENSE).
