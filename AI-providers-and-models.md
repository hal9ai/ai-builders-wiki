---
title: "AI providers and models: who makes what, and how to choose"
description: "The main model makers as of October 2026, open-weight vs closed, where to get them, and how to pick one."
category: Models and providers
tags: [models, providers]
order: 1
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Models and providers](Category-Models-and-providers.md) · Tags: [models](Tag-models.md), [providers](Tag-providers.md)
<!-- NAV:END -->

# AI providers and models: who makes what, and how to choose

**A handful of companies train the leading [models](Glossary.md#model); you can reach most of them through their own [API](Glossary.md#api), through the big [cloud](Glossary.md#cloud) platforms, or, for [open-weight models](Glossary.md#open-weight-model), by downloading and running them yourself.** Line-ups change every few months, so every fact below carries the date it was checked: 2026-10-28. Treat the names as a [snapshot](Glossary.md#snapshot) and confirm on the linked page before you build.

## Who makes what (snapshot, 2026-10-28)

**Each row lists the current flagship family as it appears on the vendor's own models page that day.**

| Maker | Current models, as listed | Closed or open weights | Its models page |
|---|---|---|---|
| Anthropic | Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5, Claude Haiku 5.5 | Closed (API only) | [Models overview](https://platform.claude.com/docs/en/models/overview) |
| OpenAI | GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna; also gpt-oss open-weight models | Closed API models; gpt-oss under Apache 2.0 ([Hugging Face](https://huggingface.co/openai/gpt-oss-120b)) | [Models](https://developers.openai.com/api/docs/models) |
| Google | Gemini 4 Argon, Gemini 3.8 Flash and other Flash / Flash-Lite models; Gemma open models | Gemini closed; Gemma open-weight, licence on each model card ([Gemma docs](https://ai.google.dev/gemma/docs)) | [Gemini models](https://ai.google.dev/gemini-api/docs/models), [Gemma](https://ai.google.dev/gemma/docs) |
| Mistral | Mistral Large 4, Mistral Medium 3.5, Mistral Small 4, Ministral 3; plus closed "Premier" models such as Codestral | Mixed: Small 4 and Ministral 3 under Apache 2.0, Medium 3.5 under Modified MIT, Large 4 listed as "Open"; Premier models closed | [Models overview](https://docs.mistral.ai/getting-started/models/models_overview/) |
| Meta | Llama 4 (open weights); a newer Muse line, mostly hosted | Llama under the Llama 4 License; most Muse models hosted only, with Muse Spark Open and Muse Glimmer (Apache 2.0) open-weight | [Llama](https://dev.meta.ai/llama/), [Muse overview](https://dev.meta.ai/docs/overview) |
| DeepSeek | DeepSeek V4.1 Flash, DeepSeek V4 Pro | Open weights; V4.1 Flash under the MIT License ([Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)) | [API docs](https://api-docs.deepseek.com/quick_start/pricing) |
| Alibaba (Qwen) | Qwen3.8-Max, Qwen3.7-Plus, Qwen3.8-Flash (API); open Qwen3.x models | Mixed: API tiers closed; open Qwen models published on [Hugging Face](https://huggingface.co/Qwen), licence per model card | [Model Studio models](https://www.alibabacloud.com/help/en/model-studio/models) |
| xAI | Grok 4.7 and earlier Grok 4.x | Current models closed; older weights published: [Grok 1](https://huggingface.co/xai-org/grok-1), [Grok 2](https://huggingface.co/xai-org/grok-2) (Grok 2 Community License) | [Models](https://docs.x.ai/docs/models) |
| Cohere | Command A+, Command A, Embed, Rerank | Mostly closed | [Models](https://docs.cohere.com/docs/models) |
| Moonshot (Kimi) | Kimi K3.1 Pro, Kimi K3, Kimi K2.x | Some open weights: the page calls Kimi K3 an "open-source 3T-class model" | [Models](https://platform.kimi.ai/docs/models.md) |

Two families are hard to place in one row:

- **Licences differ by model, not by company.** Mistral uses Apache 2.0 for some models and a Modified MIT licence for others; Meta's Llama licences are Meta's own, not a standard open-source licence. Read the licence of the exact model you plan to use, on its model card.
- **"Open" means open weights, not open training data.** You can download and run the model; you usually cannot see or reproduce how it was trained.

## Closed vs open-weight models

**A closed model runs only on its maker's servers (or a cloud partner's) and you pay per [token](Glossary.md#token); an open-weight model you can download and run wherever you like, paying for the hardware instead.**

| | Closed (API) | Open-weight |
|---|---|---|
| Access | API key, per token | Download, for example from the [Hugging Face Hub](https://huggingface.co/docs/hub/models-the-hub) |
| Where data goes | To the provider (see [data protection](Data-protection.md)) | Wherever you run it, including your own servers |
| Effort | None beyond the API call | You host it, on GPUs for larger models (see [the cloud](Cloud-for-AI-apps.md#3-running-a-model-yourself-on-gpus)) |
| Customizing | Prompts; fine-tuning only where offered | Fine-tuning and modification, within the licence |
| Who else serves it | The maker and its cloud partners | Many hosts offer open models by API too |

You can also use open-weight models without running them: many [providers](Glossary.md#provider) and cloud platforms serve them by API. Mistral's own platform, for example, lists third-party models such as DeepSeek V4.1 Flash alongside its own ([Mistral models](https://docs.mistral.ai/getting-started/models/models_overview/), checked 2026-10-28).

## Where you can get them

**Most leading models are available both from their maker and from at least one large cloud platform, which matters if your company already buys from that cloud.** For example, Anthropic's models page lists IDs for the Claude API, Amazon Bedrock, Claude Models on Google Cloud, Microsoft Foundry and Claude Platform on AWS ([Anthropic models overview](https://platform.claude.com/docs/en/models/overview), checked 2026-10-28). Amazon Bedrock offers "access to hundreds of top foundation models" from several makers ([Bedrock models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html), checked 2026-10-28). Microsoft lists "Foundry Models sold by Azure", including OpenAI's ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure), checked 2026-10-28).

The same model on two platforms can differ in price, regions, features, data terms and retirement dates. Anthropic notes that partner platforms "set their own retirement schedules" ([Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations), checked 2026-10-28).

## How model names and versions work

**A model name usually combines a family, a generation number and a tier; in production, send a fixed model ID and upgrade on purpose.** Tiers, snapshots, aliases and retirement dates are explained on [Model names and versions](Model-names-and-versions.md).


## How to choose

**Start from your task and your constraints, test two or three candidates on your own examples, and pick the cheapest one that passes.** Public rankings help you shortlist; only your own tests tell you which is good enough for you.

1. **Constraints first.** Must the data stay in the EU, or on your servers? Does your company already buy from one cloud? Do you need an open licence? These can eliminate most options before any test. See [data protection](Data-protection.md).
2. **Shortlist by tier, not brand.** For classification and extraction, try the small fast tiers first. For long agentic coding or hard reasoning, the large tiers. Anthropic's own page, for instance, recommends its smallest current model "For high-volume, latency-sensitive tasks such as classification, extraction, and routing" ([models overview](https://platform.claude.com/docs/en/models/overview)).
3. **Test on 20 to 50 real examples** from your app, with a clear pass/fail check.
4. **Compare cost per task, not per token.** A cheaper model that needs two retries may cost more. Prices are on each vendor's pricing page ([Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), [OpenAI](https://developers.openai.com/api/docs/pricing), [Google](https://ai.google.dev/gemini-api/docs/pricing), [Mistral](https://docs.mistral.ai/inference/pricing)).
5. **Check latency** if users wait for the answer: time to first token and total time.
6. **Keep switching cheap.** Wrap the model call in one function so a later change is one line.

**Public comparisons** (useful for shortlisting, each measuring something different):

- [Arena](https://arena.ai/faq) ranks models from blind human votes between two anonymous answers; "Only votes made while the models are anonymous count toward official rankings" (checked 2026-10-28).
- [Artificial Analysis](https://artificialanalysis.ai/methodology) benchmarks "intelligence, quality, performance, and price", including speed and latency (checked 2026-10-28).
- The [Hugging Face Hub](https://huggingface.co/docs/hub/models-the-hub) is where most open-weight models are published, with their model cards and licences.

## Related pages

- [What generative AI is](Generative-AI.md): tokens and costs
- [Ways to use AI](Ways-to-use-AI.md): API, chat app, coding agent
- [Model names and versions](Model-names-and-versions.md)
- [Data protection by vendor](Data-protection-by-vendor.md): vendor terms compared
- [Glossary](Glossary.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [API key](Glossary.md#api-key), [Cloud](Glossary.md#cloud), [Fine-tuning](Glossary.md#fine-tuning), [GPU](Glossary.md#gpu), [Host](Glossary.md#host), [Model](Glossary.md#model), [Open-weight model](Glossary.md#open-weight-model), [Prompt](Glossary.md#prompt), [Provider](Glossary.md#provider), [Snapshot](Glossary.md#snapshot), [Token](Glossary.md#token).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28. Vendor pages are listed in the tables and paragraphs above; the main ones:

- Anthropic: [Models overview](https://platform.claude.com/docs/en/models/overview), [Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions), [Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- OpenAI: [Models](https://developers.openai.com/api/docs/models), [Deprecations](https://developers.openai.com/api/docs/deprecations), [Pricing](https://developers.openai.com/api/docs/pricing), [gpt-oss-120b model card](https://huggingface.co/openai/gpt-oss-120b)
- Google: [Gemini models](https://ai.google.dev/gemini-api/docs/models), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), [Gemma](https://ai.google.dev/gemma/docs), [Vertex AI model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)
- Mistral: [Models overview](https://docs.mistral.ai/getting-started/models/models_overview/), [Model lifecycle](https://docs.mistral.ai/inference/model-lifecycle), [Pricing](https://docs.mistral.ai/inference/pricing)
- Meta: [Llama](https://dev.meta.ai/llama/), [Muse overview](https://dev.meta.ai/docs/overview)
- DeepSeek: [Models and pricing](https://api-docs.deepseek.com/quick_start/pricing), [DeepSeek-V4.1-Flash-1017 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)
- Alibaba Cloud: [Model Studio models](https://www.alibabacloud.com/help/en/model-studio/models)
- xAI: [Models](https://docs.x.ai/docs/models), [Grok 1](https://huggingface.co/xai-org/grok-1) and [Grok 2](https://huggingface.co/xai-org/grok-2) model cards
- Cohere: [Models](https://docs.cohere.com/docs/models)
- Moonshot: [Kimi models](https://platform.kimi.ai/docs/models.md)
- AWS: [Bedrock models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)
- Microsoft: [Foundry Models sold by Azure](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure)
- Arena, [FAQ](https://arena.ai/faq); Artificial Analysis, [Methodology](https://artificialanalysis.ai/methodology); Hugging Face, [The Model Hub](https://huggingface.co/docs/hub/models-the-hub)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Model line-ups change often: if a name here is out of date, please [open an issue](CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](LICENSE).
