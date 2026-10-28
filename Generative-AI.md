---
title: "What generative AI is, and why people build with it"
description: "What the models do, what developers and founders use them for, where they fail, and how the bill works."
category: Foundations
tags: [basics, costs]
order: 2
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Foundations](Category-Foundations.md) · Tags: [basics](Tag-basics.md), [costs](Tag-costs.md)
<!-- NAV:END -->

# What generative AI is, and why people build with it

**[Generative AI](Glossary.md#generative-ai) is software that produces new text, code, images or audio in response to an instruction, using a [model](Glossary.md#model) trained on very large amounts of existing data.** When people say "AI" in 2026 they usually mean a [large language model (LLM)](Glossary.md#llm): a model that reads text and writes text, such as the models behind ChatGPT, Claude, Gemini or Le Chat.

This page explains what these models do, what people actually use them for, where they fail, and how you pay for them. For the vocabulary, see the [glossary](Glossary.md).

## How it works, in one paragraph

**An LLM continues text: given everything so far, it predicts the next small piece, then the next, until it stops.** Anthropic describes pretraining as teaching a model "to predict the next word, given the previous context of text in the document" ([Anthropic glossary](https://platform.claude.com/docs/en/about-claude/glossary), checked 2026-10-28). A raw pretrained model is then further trained (fine-tuned, often with human feedback) so that it follows instructions and behaves like an assistant.

The pieces it reads and writes are called [tokens](Glossary.md#token). OpenAI's rule of thumb: "1 token is approximately 4 characters or 0.75 words for English text" ([OpenAI docs](https://developers.openai.com/api/docs/concepts), checked 2026-10-28). The exact ratio depends on the model and the language, so use the [provider](Glossary.md#provider)'s token counter when it matters.

Two consequences follow from this design:

- **The model has no live connection to the world.** It knows what was in its training data, plus whatever you put in the [prompt](Glossary.md#prompt). Anything newer, or private to you, has to be supplied: pasted in, retrieved from your documents ([RAG](Glossary.md#rag)), or fetched by a [tool](Glossary.md#tool).
- **The output is plausible, not guaranteed true.** The model writes what is likely to come next. Usually that is right; sometimes it is a confident invention.

## What developers and entrepreneurs use it for

**The most common use is writing and checking code.** In the 2025 Stack Overflow Developer Survey, "84% of respondents are using or planning to use AI tools in their development process" ([survey, 2025](https://survey.stackoverflow.co/2025/ai), checked 2026-10-28). In the 2026 edition, 73% of respondents use coding assistants and [agents](Glossary.md#agent) daily ([survey, 2026](https://survey.stackoverflow.co/2026/ai), checked 2026-10-28).

Beyond code, the uses that hold up well in practice share one trait: a person or a program can check the result.

| Use | Example | Why it works |
|---|---|---|
| Drafting | First version of an email, a product page, a job ad | A person edits before it goes out |
| Summarizing | A 40-page contract into one page of key clauses | You can check against the original |
| Extracting | Invoice PDFs into rows: supplier, date, total | Output is structured and testable |
| Classifying | Routing support tickets to "billing", "bug" or "sales" | Errors are cheap and measurable |
| Answering from your documents | A help bot that quotes your docs ([RAG](Glossary.md#rag)) | Answers can cite their source |
| Coding | Writing a function, a test, a migration script | Code can be run and tested |
| Acting through tools | An [agent](AI-agent.md) that reads an issue, edits code, runs tests | The loop checks its own work, within limits |

For a founder, the pattern is usually one of two:

- **AI inside the product:** the app calls a model to do part of its job (summarize a call, answer a customer). You pay per use; see [costs](#what-it-costs) below.
- **AI to build the product:** a coding assistant writes much of the app. You pay a subscription or per use, and you still own the result, its bugs and its security. See [a typical workflow](Idea-to-deployed-AI-app.md).

## Where it fails

**The main limit is that the model can be wrong without warning.** Anthropic's own guide says models "can sometimes generate text that is factually incorrect or inconsistent with the given context", which is called [hallucination](Glossary.md#hallucination), and that mitigation techniques "don't eliminate them entirely" ([Anthropic, reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations), checked 2026-10-28). Developers notice: in the 2025 survey, 66% named "AI solutions that are almost right, but not quite" as a frustration, and more respondents distrusted AI accuracy (46%) than trusted it (33%) ([survey, 2025](https://survey.stackoverflow.co/2025/ai)).

Other limits worth knowing before you build:

- **Not repeatable.** The same input can give different outputs. Even with [temperature](Glossary.md#temperature) set to 0, Anthropic notes that "results will not be fully deterministic" ([Anthropic glossary](https://platform.claude.com/docs/en/about-claude/glossary)). Tests must check properties ("is it valid JSON with a total field?"), not exact strings.
- **Limited memory per request.** A model only sees what fits in its [context window](Glossary.md#context-window). Long histories and big documents must be trimmed, summarized or retrieved in pieces.
- **Training cutoff.** The model does not know recent events unless you give them to it.
- **Latency.** A long answer can take many seconds. Apps usually [stream](Glossary.md#streaming) the answer word by word so users see progress, which affects [where you can host the app](Cloud-for-AI-apps.md#time-limits-and-streaming).
- **Data you send leaves your machine.** Prompts go to the provider. What it keeps, and whether it trains on them, depends on the vendor and the plan: see [data protection](Data-protection.md).
- **New attack surface.** Text the model reads can contain instructions that hijack it. See [security](Security-for-AI-apps.md#prompt-injection).

A practical rule: use generative AI where a wrong answer is cheap to spot and fix, and add a check (a person, a test, a schema) where it is not.

## What it costs

**There are two ways to pay: a monthly subscription for a chat app, or per token through an [API](Glossary.md#api).**

- **Subscriptions** (ChatGPT, Claude, Gemini and others) give a person a chat app and often a [coding agent](Glossary.md#coding-agent), with usage limits. They are for people, not for your app's users.
- **API pricing** is per million tokens, with separate prices for input (what you send) and output (what the model writes). Output costs more. Your app pays this every time it calls the model.

An example, using one vendor's list prices. Anthropic lists Claude Sonnet 5.5 at $2 per million input tokens and $10 per million output tokens ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), checked 2026-10-28). Suppose a support bot handles 1,000 conversations a day, each sending 2,000 tokens and receiving 500:

- input: 1,000 × 2,000 = 2 million tokens → $4 per day
- output: 1,000 × 500 = 0.5 million tokens → $5 per day
- total: about $9 per day, about $270 per month, before any discounts

This is arithmetic on list prices, not a measurement; real conversations vary a lot in length. The same page lists ways to pay less, for example a Batch API with "a 50 percent discount on both input and output tokens" for work that can wait, and lower prices for cached, repeated input ([Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)). Other providers have similar mechanisms; compare on [providers and models](AI-providers-and-models.md).

Three habits keep the bill predictable:

1. **Pick the smallest model that does the job.** Prices across one vendor's own tiers can differ by more than ten times.
2. **Set a spend limit** in the provider's console, and per-user limits in your app. See [the workflow page](Idea-to-deployed-AI-app.md#6-watch-costs).
3. **Count the hosting separately.** Calling a model and hosting your app are two different bills. See [the cloud for AI apps](Cloud-for-AI-apps.md).

## Related pages

- [Glossary](Glossary.md)
- [What an AI agent is](AI-agent.md)
- [Providers and models](AI-providers-and-models.md)
- [Ways to use AI](Ways-to-use-AI.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [Cloud](Glossary.md#cloud), [Coding agent](Glossary.md#coding-agent), [Context window](Glossary.md#context-window), [Generative AI](Glossary.md#generative-ai), [Hallucination](Glossary.md#hallucination), [Host](Glossary.md#host), [LLM](Glossary.md#llm), [Model](Glossary.md#model), [Prompt](Glossary.md#prompt), [Provider](Glossary.md#provider), [RAG](Glossary.md#rag), [Temperature](Glossary.md#temperature), [Token](Glossary.md#token), [Tool](Glossary.md#tool), [Workflow](Glossary.md#workflow).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28.

- Anthropic, [Glossary](https://platform.claude.com/docs/en/about-claude/glossary)
- Anthropic, [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Anthropic, [Reduce hallucinations](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)
- OpenAI, [Key concepts](https://developers.openai.com/api/docs/concepts)
- Stack Overflow, [Developer Survey 2025: AI](https://survey.stackoverflow.co/2025/ai)
- Stack Overflow, [Developer Survey 2026: AI](https://survey.stackoverflow.co/2026/ai)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
