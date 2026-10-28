---
title: "AI providers and models: who makes what, and how to choose"
description: "The main model makers as of October 2026, open-weight vs closed, how model names and versions work, and how to pick one."
category: Foundations
tags: [providers, models, open-weight, costs]
checked: 2026-10-28
---

# AI providers and models: who makes what, and how to choose

**A handful of companies train the leading models; you can reach most of them through their own API, through the big cloud platforms, or, for open-weight models, by downloading and running them yourself.** Line-ups change every few months, so every fact below carries the date it was checked: 2026-10-28. Treat the names as a snapshot and confirm on the linked page before you build.

## Who makes what (snapshot, 2026-10-28)

**Each row lists the current flagship family as it appears on the vendor's own models page that day.**

| Maker | Current models, as listed | Closed or open weights | Its models page |
|---|---|---|---|
| Anthropic | Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5, Claude Haiku 5.5 | Closed (API only) | [Models overview](https://platform.claude.com/docs/en/models/overview) |
| OpenAI | GPT-6 Astra, GPT-6.1 Sol, GPT-6.1 Terra, GPT-6 Luna; also gpt-oss open-weight models | Closed API models; gpt-oss under Apache 2.0 ([Hugging Face](https://huggingface.co/openai/gpt-oss-120b)) | [Models](https://developers.openai.com/api/docs/models) |
| Google | Gemini 4 Argon, Gemini 3.8 Flash and other Flash / Flash-Lite models; Gemma open models | Gemini closed; Gemma 4 under Apache 2.0 on [Hugging Face](https://huggingface.co/google) | [Gemini models](https://ai.google.dev/gemini-api/docs/models), [Gemma](https://ai.google.dev/gemma/docs) |
| Mistral | Mistral Large 4, Mistral Medium 3.5, Mistral Small 4, Ministral 3; plus closed "Premier" models such as Codestral | Mixed: several open-weight (Apache 2.0, Modified MIT), some closed | [Models overview](https://docs.mistral.ai/getting-started/models/models_overview/) |
| Meta | Llama 4 (open weights); a newer Muse line, mostly API-only | Llama under the Llama 4 License; Muse mostly closed | [Llama](https://dev.meta.ai/llama/), [Muse overview](https://dev.meta.ai/docs/overview) |
| DeepSeek | DeepSeek V4.1 Flash, DeepSeek V4 Pro | Open weights, MIT License ([Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)) | [API docs](https://api-docs.deepseek.com/quick_start/pricing) |
| Alibaba (Qwen) | Qwen3.8-Max, Qwen3.7-Plus, Qwen3.8-Flash (API); open Qwen3.x models | Mixed: API tiers closed, many open models under Apache 2.0 | [Model Studio models](https://www.alibabacloud.com/help/en/model-studio/models) |
| xAI | Grok 4.7 and earlier Grok 4.x | Current models closed; older Grok 1 and 2 weights released | [Models](https://docs.x.ai/docs/models) |
| Cohere | Command A+, Command A, Embed, Rerank | Mostly closed | [Models](https://docs.cohere.com/docs/models) |
| Moonshot (Kimi) | Kimi K3.1 Pro, Kimi K3, Kimi K2.x | Some open weights, under their own licences | [Models](https://platform.kimi.ai/docs/models.md) |

Two families are hard to place in one row:

- **Licences differ by model, not by company.** Google's Gemma 3 uses a separate Gemma licence while Gemma 4 models are listed as Apache 2.0; Meta's Llama licences are Meta's own, not a standard open-source licence. Read the licence of the exact model you plan to use, on its model card.
- **"Open" means open weights, not open training data.** You can download and run the model; you usually cannot see or reproduce how it was trained.

## Closed vs open-weight models

**A closed model runs only on its maker's servers (or a cloud partner's) and you pay per token; an open-weight model you can download and run wherever you like, paying for the hardware instead.**

| | Closed (API) | Open-weight |
|---|---|---|
| Access | API key, per token | Download, for example from the [Hugging Face Hub](https://huggingface.co/docs/hub/models-the-hub) |
| Where data goes | To the provider (see [data protection](data-protection.md)) | Wherever you run it, including your own servers |
| Effort | None beyond the API call | You host it, on GPUs for larger models (see [the cloud](cloud-for-ai-apps.md#3-running-a-model-yourself-on-gpus)) |
| Customizing | Prompts; fine-tuning only where offered | Fine-tuning and modification, within the licence |
| Who else serves it | The maker and its cloud partners | Many hosts offer open models by API too |

You can also use open-weight models without running them: many providers and cloud platforms serve them by API. Mistral's own platform, for example, lists third-party models such as DeepSeek V4.1 Flash alongside its own ([Mistral models](https://docs.mistral.ai/getting-started/models/models_overview/), checked 2026-10-28).

## Where you can get them

**Most leading models are available both from their maker and from at least one large cloud platform, which matters if your company already buys from that cloud.** For example, Anthropic's models page lists IDs for the Claude API, Amazon Bedrock, Claude Models on Google Cloud, Microsoft Foundry and Claude Platform on AWS ([Anthropic models overview](https://platform.claude.com/docs/en/models/overview), checked 2026-10-28). Amazon Bedrock offers "access to hundreds of top foundation models" from several makers ([Bedrock models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html), checked 2026-10-28). Microsoft lists models "sold directly by Azure", including OpenAI's ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure), checked 2026-10-28).

The same model on two platforms can differ in price, regions, features, data terms and retirement dates. Anthropic notes that partner platforms "set their own retirement schedules" ([Anthropic model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations), checked 2026-10-28).

## How model names and versions work

**A model name usually has three parts: a family (Claude, GPT, Gemini), a generation number, and a size or speed tier; the exact ID you send in code may also pin a dated snapshot.**

**Tiers.** Each vendor sells bigger, slower, pricier models and smaller, faster, cheaper ones under its own names (all from the models pages above, checked 2026-10-28):

| Vendor | Tier names, most capable to fastest |
|---|---|
| Anthropic | Fable, Opus, Sonnet, Haiku |
| OpenAI | Astra, Sol, Terra, Luna |
| Google Gemini | Pro, Flash, Flash-Lite (where Gemini 4 Argon fits is not stated on the page) |
| Alibaba Qwen | Max, Plus, Flash |

**Snapshots and aliases.** In code you send a model ID. Some IDs are fixed snapshots; others are aliases that move to newer versions:

- **Anthropic:** "Starting with the Claude 4.6 generation, model IDs use a dateless format", and such an ID "is not an alias. It is the snapshot." Older models use dated IDs such as `claude-sonnet-4-5-20250929` ([Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions)).
- **OpenAI:** "Snapshots let you lock in a specific version of the model so that performance and behavior remain consistent"; older snapshots carry dates such as `gpt-4.1-2025-04-14` ([OpenAI models](https://developers.openai.com/api/docs/models)).
- **Google Gemini:** a *stable* name "Points to a specific stable model. Stable models usually don't change"; *preview* "may be used for production"; *latest* points to the newest release and changes over time; *experimental* models are not for production ([Gemini models](https://ai.google.dev/gemini-api/docs/models)).
- **Mistral:** IDs follow "a model-name-major-minor format, for example mistral-medium-3-5", and `-latest` aliases exist, with a warning: "Using an alias may expose you to silent updates in model behavior and pricing" ([Mistral model lifecycle](https://docs.mistral.ai/inference/model-lifecycle)).
- **xAI:** a bare model name is "aliased to the latest stable version", `-latest` to the latest version, and a dated name "will not be updated" ([xAI models](https://docs.x.ai/docs/models)).

All checked 2026-10-28. **In production, pin a fixed ID** and upgrade on purpose, after testing.

**Retirement.** Models are retired on a schedule, and calls to a retired ID fail. Published notice periods (checked 2026-10-28):

- Anthropic: "at least 60 days' notice before model retirement for publicly released models" ([deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations)).
- Mistral: 6 months for generally available models, 1 month for Labs, preview and third-party models; after retirement, "requests to its identifiers fail with a 404 error" ([model lifecycle](https://docs.mistral.ai/inference/model-lifecycle)).
- Google Vertex AI: "gives you at least 45 days to migrate" ([model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)).
- OpenAI publishes its notice periods and shutdown dates on its [deprecations page](https://developers.openai.com/api/docs/deprecations).

Put the model ID in configuration, not scattered through code, and subscribe to your provider's deprecation notices.

## How to choose

**Start from your task and your constraints, test two or three candidates on your own examples, and pick the cheapest one that passes.** Public rankings help you shortlist; only your own tests tell you which is good enough for you.

1. **Constraints first.** Must the data stay in the EU, or on your servers? Does your company already buy from one cloud? Do you need an open licence? These can eliminate most options before any test. See [data protection](data-protection.md).
2. **Shortlist by tier, not brand.** For classification and extraction, try the small fast tiers first. For long agentic coding or hard reasoning, the large tiers. Anthropic's own page, for instance, recommends its smallest current model "For high-volume, latency-sensitive tasks such as classification, extraction, and routing" ([models overview](https://platform.claude.com/docs/en/models/overview)).
3. **Test on 20 to 50 real examples** from your app, with a clear pass/fail check.
4. **Compare cost per task, not per token.** A cheaper model that needs two retries may cost more. Prices are on each vendor's pricing page ([Anthropic](https://platform.claude.com/docs/en/about-claude/pricing), [OpenAI](https://developers.openai.com/api/docs/pricing), [Google](https://ai.google.dev/gemini-api/docs/pricing), [Mistral](https://docs.mistral.ai/inference/pricing)).
5. **Check latency** if users wait for the answer: time to first token and total time.
6. **Keep switching cheap.** Wrap the model call in one function so a later change is one line.

**Public comparisons** (useful for shortlisting, each measuring something different):

- [Arena](https://arena.ai/faq) (formerly LMArena) ranks models from blind human votes between two anonymous answers; "Only votes made while the models are anonymous count toward official rankings" (checked 2026-10-28).
- [Artificial Analysis](https://artificialanalysis.ai/methodology) benchmarks "intelligence, quality, performance, and price", including speed and latency (checked 2026-10-28).
- The [Hugging Face Hub](https://huggingface.co/docs/hub/models-the-hub) is where most open-weight models are published, with their model cards and licences.

## Related pages

- [What generative AI is](generative-ai.md): tokens and costs
- [Ways to use AI](ways-to-use-ai.md): API, chat app, coding agent
- [Data protection](data-protection.md): vendor terms compared
- [Glossary](glossary.md)

## Sources

All checked on 2026-10-28. Vendor pages are listed in the tables and paragraphs above; the main ones:

- Anthropic: [Models overview](https://platform.claude.com/docs/en/models/overview), [Model IDs and versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions), [Deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- OpenAI: [Models](https://developers.openai.com/api/docs/models), [Deprecations](https://developers.openai.com/api/docs/deprecations), [Pricing](https://developers.openai.com/api/docs/pricing), [gpt-oss-120b model card](https://huggingface.co/openai/gpt-oss-120b)
- Google: [Gemini models](https://ai.google.dev/gemini-api/docs/models), [Gemini pricing](https://ai.google.dev/gemini-api/docs/pricing), [Gemma](https://ai.google.dev/gemma/docs), [Vertex AI model versions](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions)
- Mistral: [Models overview](https://docs.mistral.ai/getting-started/models/models_overview/), [Model lifecycle](https://docs.mistral.ai/inference/model-lifecycle), [Pricing](https://docs.mistral.ai/inference/pricing)
- Meta: [Llama](https://dev.meta.ai/llama/), [Muse overview](https://dev.meta.ai/docs/overview)
- DeepSeek: [Models and pricing](https://api-docs.deepseek.com/quick_start/pricing), [DeepSeek-V4.1-Flash-1017 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017)
- Alibaba Cloud: [Model Studio models](https://www.alibabacloud.com/help/en/model-studio/models)
- xAI: [Models](https://docs.x.ai/docs/models)
- Cohere: [Models](https://docs.cohere.com/docs/models)
- Moonshot: [Kimi models](https://platform.kimi.ai/docs/models.md)
- AWS: [Bedrock models at a glance](https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html)
- Microsoft: [Models sold directly by Azure](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure)
- Arena, [FAQ](https://arena.ai/faq); Artificial Analysis, [Methodology](https://artificialanalysis.ai/methodology); Hugging Face, [The Model Hub](https://huggingface.co/docs/hub/models-the-hub)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Model line-ups change often: if a name here is out of date, please [open an issue](../CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](../LICENSE).
