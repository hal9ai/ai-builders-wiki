---
title: "The cloud, for AI apps"
description: "Three different jobs: hosting your app, calling a model, running a model on GPUs. And serverless vs containers vs VMs."
category: Foundations
tags: [hosting, costs]
order: 4
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Foundations](Category-Foundations.md) · Tags: [hosting](Tag-hosting.md), [costs](Tag-costs.md)
<!-- NAV:END -->

# The cloud, for AI apps

**For an AI app, "the cloud" usually means three separate things: a place that runs your app, a [provider](Glossary.md#provider) that runs the [model](Glossary.md#model) your app calls, and, only sometimes, [GPUs](Glossary.md#gpu) where you run a model yourself.** Most small AI apps need the first two and never touch a GPU.

## What the cloud is

**[Cloud](Glossary.md#cloud) computing is renting computers, storage and software over the internet, on demand, instead of owning them.** The standard definition, from NIST: "a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources" ([NIST SP 800-145](https://csrc.nist.gov/pubs/sp/800/145/final), 2011, checked 2026-10-28).

NIST names three service models, still the common vocabulary:

| Model | You get | You manage | Example for an AI app |
|---|---|---|---|
| SaaS (software as a service) | A finished application | Your account and data | A chat app such as ChatGPT or Claude |
| PaaS (platform as a service) | A place to deploy your code | Your code and its settings | A host that runs your container or function |
| IaaS (infrastructure as a service) | Raw virtual machines, disks, networks | Almost everything, including the operating system | A VM with a GPU where you install a model server |

A model [API](Glossary.md#api) (you send text, you get text back, you pay per [token](Glossary.md#token)) sits between these: you use it like SaaS from your code. Vendors call it "model as a service" or simply "the API".

## Three jobs, three bills

**Hosting your app, calling a model and running a model are different services, often from different companies, each with its own bill.**

### 1. Hosting the app

Your code (the web page, the backend that holds your [API key](Glossary.md#api-key), the bot, the [MCP server](Agent-protocols-MCP-and-A2A.md#mcp-connecting-agents-to-tools)) has to run somewhere with a public address. This is ordinary web hosting. You choose between the shapes in [serverless, containers or VMs](#serverless-containers-or-vms) below.

### 2. Calling a model

Your backend sends requests to a model provider's API: Anthropic, OpenAI, Google, Mistral and others, or the same models through a cloud platform. Examples of such platforms, in their own words (checked 2026-10-28):

- **Amazon Bedrock**: "a fully managed service that provides secure, enterprise-grade access to high-performing foundation models from leading AI companies" ([AWS docs](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html)).
- **Microsoft Foundry** (formerly Azure AI Foundry): "unifies agents, models, and tools under a single management grouping" ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)).
- **Google Cloud**: its AI platform docs, at the former Vertex AI address, now present "Gemini Enterprise Agent Platform" ([Google Cloud docs](https://docs.cloud.google.com/vertex-ai/docs)).

Teams use these when they already have a contract, data-location requirements or billing with that cloud. See [providers and models](AI-providers-and-models.md) and [data protection](Data-protection.md).

### 3. Running a model yourself, on GPUs

You only need this if you run an [open-weight model](Glossary.md#open-weight-model) yourself: for privacy, cost at high volume, a fine-tuned model, or a model no API offers. Options range from managed to raw (descriptions are the vendors' own, checked 2026-10-28):

- **Managed model endpoints:** Hugging Face Inference Endpoints, "a managed service to deploy your AI model to production" ([docs](https://huggingface.co/docs/inference-endpoints/index)).
- **GPU demo apps:** a Hugging Face Space can be upgraded "to use a GPU accelerator", billed "by the minute" ([docs](https://huggingface.co/docs/hub/spaces-gpus)).
- **[Serverless](Glossary.md#serverless) GPU:** for example Modal ([docs](https://modal.com/docs/guide)) or Runpod Serverless, "Pay-as-you-go compute for AI models and compute-intensive workloads" ([docs](https://docs.runpod.io/serverless/overview)). You pay while a request runs; the first request after idle can be slow while the model loads.
- **GPU virtual machines** from any large cloud: most control, most work, and you pay while the machine is on, used or not.

GPUs are the expensive part of AI infrastructure. Before renting one, check whether a hosted API for the same or a similar model would do.

## Serverless, containers or VMs

**The shape of your app decides where it can run: short request-and-response code fits serverless functions; anything that streams for long, runs all day or keeps files fits [containers](Glossary.md#container) or VMs better.**

| Shape | What you deploy | Runs | Good for | Watch out for |
|---|---|---|---|---|
| Serverless functions | A function | Only during a request, with a maximum duration | Webhooks, short API calls, low traffic | Time limits; no local files that last |
| Containers | A container image (your app plus its dependencies) | As long as you want, or scaled to zero when idle | Web apps, bots, agents, MCP servers | Sleeping apps start slowly; disks only if the host offers volumes |
| Virtual machines | A whole server | Always, until you stop it | Full control, GPUs, unusual software | You patch and secure the operating system |

### Time limits and streaming

**AI responses are slow and are usually streamed, so check your [host](Glossary.md#host)'s maximum request time before you choose it.** Both Anthropic and OpenAI stream answers with server-sent events (SSE): Anthropic lets you "set `"stream": true` to incrementally stream the response using server-sent events (SSE)" ([Anthropic, Streaming](https://platform.claude.com/docs/en/build-with-claude/streaming)); OpenAI's guide covers "HTTP streaming (`stream=true`) over server-sent events (SSE)" ([OpenAI, Streaming](https://developers.openai.com/api/docs/guides/streaming-responses)). An [agent](Glossary.md#agent) that works for several minutes needs the connection, or a background job, to last that long.

Some published limits, checked 2026-10-28:

| Platform | Limit, as documented |
|---|---|
| AWS Lambda | Default 3 seconds, adjustable "up to a maximum value of 900 seconds (15 minutes)" ([AWS docs](https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html)) |
| Google Cloud Run | Default "5 minutes (300 seconds)", "can be extended up to 60 minutes (3600 seconds)" ([Google Cloud docs](https://docs.cloud.google.com/run/docs/configuring/request-timeout)) |
| Vercel Functions | Depends on plan; Pro and Enterprise "can set individual Vercel Functions … to run for up to 30 minutes" ([Vercel docs](https://vercel.com/docs/functions/configuring-functions/duration)) |

Limits change and have exceptions (plans, beta options, async invocations): read the linked page for your case. If your work can take longer than the limit, put it in a background job or a queue and let the user poll or get notified.

### A disclosed example: a long-lived container

Hosts that run containers without a per-request limit suit bots, agents and [MCP](Glossary.md#mcp-model-context-protocol) servers that hold connections open. Cloudish (made by Hal9, which started this wiki) works this way: "Cloudish deploys apps as long-lived containers with a public URL", and apps can stay on or sleep when idle and wake on the next request ([Cloudish skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), checked 2026-10-28). Many other hosts offer containers too; the point is the shape, not the vendor.

## Which setup for which app

| Your app | Hosting | Model | GPU? |
|---|---|---|---|
| A chatbot on your website | Small container or function with streaming | Hosted API | No |
| A nightly job that summarizes reports | Scheduled function or container | Hosted API, batch mode if offered | No |
| A Slack or Discord bot | Always-on container | Hosted API | No |
| A remote MCP server for your team | Container with HTTPS | Usually none of its own | No |
| A private document assistant that must not leave your network | Your own servers or VPC | Open-weight model you run | Yes |
| A demo of a fine-tuned image model | GPU Space or serverless GPU | Your model | Yes |

## Related pages

- [From idea to deployed AI app](Idea-to-deployed-AI-app.md): the concrete steps
- [Security](Security-for-AI-apps.md): keys, tokens, permissions
- [Data protection](Data-protection.md): where your users' data goes
- [Providers and models](AI-providers-and-models.md)
- [Glossary](Glossary.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [API key](Glossary.md#api-key), [Chatbot](Glossary.md#chatbot), [Cloud](Glossary.md#cloud), [Container](Glossary.md#container), [Deploy](Glossary.md#deploy), [GPU](Glossary.md#gpu), [Host](Glossary.md#host), [Inference](Glossary.md#inference), [MCP (Model Context Protocol)](Glossary.md#mcp-model-context-protocol), [Model](Glossary.md#model), [Open-weight model](Glossary.md#open-weight-model), [Provider](Glossary.md#provider), [Serverless](Glossary.md#serverless), [Streaming](Glossary.md#streaming), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28.

- NIST, [SP 800-145, The NIST Definition of Cloud Computing](https://csrc.nist.gov/pubs/sp/800/145/final) (2011)
- AWS, [What is Amazon Bedrock?](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html); [Lambda function timeout](https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html)
- Microsoft, [What is Microsoft Foundry?](https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry)
- Google Cloud, [AI platform documentation](https://docs.cloud.google.com/vertex-ai/docs); [Cloud Run request timeout](https://docs.cloud.google.com/run/docs/configuring/request-timeout)
- Vercel, [Configuring maximum duration](https://vercel.com/docs/functions/configuring-functions/duration)
- Hugging Face, [Inference Endpoints](https://huggingface.co/docs/inference-endpoints/index); [Spaces GPU upgrades](https://huggingface.co/docs/hub/spaces-gpus)
- Modal, [Guide](https://modal.com/docs/guide)
- Runpod, [Serverless overview](https://docs.runpod.io/serverless/overview)
- Anthropic, [Streaming messages](https://platform.claude.com/docs/en/build-with-claude/streaming)
- OpenAI, [Streaming API responses](https://developers.openai.com/api/docs/guides/streaming-responses)
- Cloudish, [skill.md](https://cloudish.ai/skill.md?ref=cc-wiki)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
