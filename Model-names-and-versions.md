---
title: "Model names and versions"
description: "How model families, tiers, snapshots, aliases and retirement dates work, vendor by vendor."
category: Models and providers
tags: [models]
order: 2
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Models and providers](Category-Models-and-providers.md) · Tags: [models](Tag-models.md)
<!-- NAV:END -->

# Model names and versions

**A [model](Glossary.md#model) name usually has three parts: a family (Claude, GPT, Gemini), a generation number, and a size or speed tier; the exact ID you send in code may also pin a dated [snapshot](Glossary.md#snapshot).** Knowing which kind of ID you use tells you whether the model can change under you, and when it will stop working.

## Tiers

 Each vendor sells bigger, slower, pricier models and smaller, faster, cheaper ones under its own names (from each vendor's models page, linked on [AI providers and models](AI-providers-and-models.md#who-makes-what-snapshot-2026-10-28), checked 2026-10-28):

| Vendor | Tier names, most capable to fastest |
|---|---|
| Anthropic | Fable, Opus, Sonnet, Haiku |
| OpenAI | Astra, Sol, Terra, Luna |
| Google Gemini | Pro, Flash, Flash-Lite (where Gemini 4 Argon fits is not stated on the page) |
| Alibaba Qwen | Max, Plus, Flash |

## Snapshots and aliases

 In code you send a model ID. Some IDs are fixed snapshots; others are aliases that move to newer versions:

- **Anthropic:** "Starting with the Claude 4.6 generation, model IDs use a dateless format", and such an ID "is not an alias. It is the snapshot." Older models use dated IDs such as `claude-sonnet-4-5-20250929` ([Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)).
- **OpenAI:** "Snapshots let you lock in a specific version of the model so that performance and behavior remain consistent"; older snapshots carry dates such as `gpt-4.1-2025-04-14` ([OpenAI models](https://developers.openai.com/api/docs/models)).
- **Google Gemini:** a *stable* name "Points to a specific stable model. Stable models usually don't change"; *preview* "may be used for production"; *latest* points to the newest release and changes over time; *experimental* models are not for production ([Gemini models](https://ai.google.dev/gemini-api/docs/models)).
- **Mistral:** IDs follow "a model-name-major-minor format, for example mistral-medium-3-5", and `-latest` aliases exist, with a warning: "Using an alias may expose you to silent updates in model behavior and pricing" ([Mistral model lifecycle](https://docs.mistral.ai/inference/model-lifecycle)).
- **xAI:** a bare model name is "aliased to the latest stable version", `-latest` to the latest version, and a dated name "will not be updated" ([xAI models](https://docs.x.ai/docs/models)).

All checked 2026-10-28. **In production, pin a fixed ID** and upgrade on purpose, after testing.

## Retirement

 Models are retired on a schedule, and calls to a retired ID fail. Published notice periods (checked 2026-10-28):

- Anthropic: "at least 60 days' notice before model retirement for publicly released models" ([deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)).
- Mistral: 6 months for generally available models, 1 month for Labs, preview and third-party models; after retirement, "requests to its identifiers fail with a 404 error" ([model lifecycle](https://docs.mistral.ai/inference/model-lifecycle)).
- Google Vertex AI: "gives you at least 45 days to migrate" ([model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)).
- OpenAI publishes its notice periods and shutdown dates on its [deprecations page](https://developers.openai.com/api/docs/deprecations).

Put the model ID in configuration, not scattered through code, and subscribe to your [provider](Glossary.md#provider)'s deprecation notices.

## Related pages

- [AI providers and models](AI-providers-and-models.md): who makes what, and how to choose
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md#7-updates): changing models safely

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Model](Glossary.md#model), [Provider](Glossary.md#provider), [Snapshot](Glossary.md#snapshot).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28.

- Anthropic: [Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions), [Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)
- OpenAI: [Models](https://developers.openai.com/api/docs/models), [Deprecations](https://developers.openai.com/api/docs/deprecations)
- Google: [Gemini models](https://ai.google.dev/gemini-api/docs/models), [Vertex AI model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)
- Mistral: [Model lifecycle](https://docs.mistral.ai/inference/model-lifecycle)
- xAI: [Models](https://docs.x.ai/docs/models)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Open an issue](CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](LICENSE).
