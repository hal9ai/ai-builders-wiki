---
title: "Glossary: the basic words"
description: "The core terms a newcomer meets, each defined in plain words, with links to the pages that go deeper."
category: Foundations
tags: [basics]
order: 1
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Foundations](Category-Foundations.md) · Tags: [basics](Tag-basics.md)
<!-- NAV:END -->

# Glossary: the basic words

**These are the words you meet first when you build or deploy something with AI, each explained using only plain words or other words on this page.** Terms are in alphabetical order. A word in *italics* inside a definition has its own entry here.

Jump to: [A](#a2a-agent2agent) · [C](#chatbot) · [D](#deploy) · [E](#environment-variable) · [F](#fine-tuning) · [G](#generative-ai) · [H](#hallucination) · [I](#inference) · [L](#llm) · [M](#mcp-model-context-protocol) · [O](#open-weight-model) · [P](#prompt) · [R](#rag) · [S](#secret) · [T](#temperature) · [W](#workflow) · [Z](#zero-data-retention-zdr)

### A2A (Agent2Agent)

An open set of rules for one *agent* to find another agent, give it a task and follow its progress, even when the two are run by different companies. It started at Google and is now a Linux Foundation project. → [Agents working together](Agent-protocols-MCP-and-A2A.md#a2a-agents-talking-to-agents)

### Agent

A program in which a *model* decides, step by step, which *tools* to use to finish a task, and keeps going until it is done or stopped. A *chatbot* answers; an agent acts. → [What an AI agent is](AI-agent.md)

### Agent SDK

A code library that gives you the loop, *tool* calls and memory handling of an *agent*, so you can build your own agent without writing that part. Examples: Claude Agent SDK, OpenAI Agents SDK, Google ADK. → [Ways to use AI](Ways-to-use-AI.md#agent-sdks)

### API

A way for one program to ask another program to do something over the internet, by sending a structured request and getting a structured answer. A model API lets your app send a *prompt* and receive the model's answer. → [Ways to use AI](Ways-to-use-AI.md#apis)

### API key

A long secret string that identifies your account when your program calls an *API*. Anyone who has it can use, and spend from, your account, so it is a *secret*. → [Security](Security-for-AI-apps.md#secrets-and-api-keys)

### Chatbot

An app where a person types messages and a *model* answers, one turn at a time. It does not take actions on its own; that is what an *agent* adds.

### Cloud

Computers, storage and software rented over the internet, on demand, instead of owned. For AI apps it covers three separate jobs: running your app, running the model your app calls, and sometimes running a model on your own rented *GPUs*. → [The cloud, for AI apps](Cloud-for-AI-apps.md)

### Coding agent

An *agent* that works inside a code project: it reads files, edits them, runs commands and checks the result. It can run in a terminal, an editor or on the vendor's servers. → [Ways to use AI](Ways-to-use-AI.md#coding-agents-in-the-terminal)

### Container

A packaged copy of your app together with everything it needs to run (libraries, settings), so it runs the same on your laptop and on a *host*. A *Dockerfile* is the recipe for building one. → [The cloud](Cloud-for-AI-apps.md#serverless-containers-or-vms)

### Context window

The amount of text a *model* can take into account at once: your *prompt*, earlier messages, documents and its own answer, counted in *tokens*. Anthropic calls it the model's "working memory" ([Anthropic glossary](https://platform.claude.com/docs/en/about-claude/glossary), checked 2026-10-28). What does not fit is not seen.

### Deploy

To put your app on a *host* so it runs there and others can reach it at a web address. Redeploying means replacing the running version with a new one. → [From idea to deployed app](Idea-to-deployed-AI-app.md#4-deploy)

### Dockerfile

A short text file listing the steps to build a *container*: which base system to start from, which files to copy, which command starts the app.

### Environment variable

A named setting given to a program from outside its code, such as `PORT=8000` or `MODEL_API_KEY=...`. Keeping settings and *secrets* in environment variables means the same code runs everywhere and no key sits in the code. → [Keys and secrets](Idea-to-deployed-AI-app.md#2-keys-and-secrets)

### Fine-tuning

Training an existing *model* further on your own examples, so it picks up a style, format or specialty. Many apps never need it: good *prompts* and *RAG* often do the job.

### Generative AI

Software that produces new text, code, images or sound from an instruction, using a *model* trained on large amounts of existing data. → [What generative AI is](Generative-AI.md)

### GPU

A chip built to do very many small calculations at the same time. Training and running large *models* needs GPUs, which is why they are the expensive part of AI. You only rent them if you run a model yourself. → [The cloud](Cloud-for-AI-apps.md#3-running-a-model-yourself-on-gpus)

### Hallucination

When a *model* states something false or made up, in the same confident tone as true statements. It can be reduced but not removed, so important answers need checking. → [Where it fails](Generative-AI.md#where-it-fails)

### Host

A company or service that runs your app on its computers and gives it a web address. Also called a hosting provider or platform. → [The cloud](Cloud-for-AI-apps.md#1-hosting-the-app)

### Inference

Running a trained *model* to get an answer. Each call to a model *API* is an inference; you pay for it in *tokens*. (Training is the separate, earlier step that creates the model.)

### LLM

Large language model: a *model* trained on very large amounts of text that reads text and writes text. ChatGPT, Claude, Gemini and Le Chat are apps built on LLMs. → [What generative AI is](Generative-AI.md)

### Logs

The lines a running app writes about what it is doing: requests, errors, warnings. They are the first place to look when something goes wrong. → [Read the logs](Idea-to-deployed-AI-app.md#5-read-the-logs)

### MCP (Model Context Protocol)

An open set of rules for connecting *tools* and data to an AI app, so one tool server works with many assistants. Created by Anthropic in 2024 and donated in 2025 to a foundation under the Linux Foundation. → [MCP](Agent-protocols-MCP-and-A2A.md#mcp-connecting-agents-to-tools)

### Model

The trained program that turns an input (text, an image) into an output (text, an image). Models come in families and sizes, such as a large slow one and a small fast one. → [Providers and models](AI-providers-and-models.md)

### Open-weight model

A *model* whose trained files (the "weights") are published, so you can download it and run it on your own computers, under its licence. The opposite is a closed model, which you can only use through its maker's *API*. → [Closed vs open-weight](AI-providers-and-models.md#closed-vs-open-weight-models)

### Prompt

The text you send to a *model*: your question or instruction, plus any documents or examples. A *system prompt* is the part that sets the rules for a whole conversation.

### Prompt injection

An attack where text the *model* reads (a web page, an email, a file) contains instructions that make it do something its owner did not intend. The main new security risk of AI apps. → [Security](Security-for-AI-apps.md#prompt-injection)

### Provider

A company that offers *models* through an *API*: either the maker (Anthropic, OpenAI, Google, Mistral…) or a *cloud* platform that resells many makers' models. → [Providers and models](AI-providers-and-models.md)

### RAG

Retrieval-augmented generation: before asking the *model*, your app searches your own documents and puts the most relevant passages into the *prompt*, so the answer is based on them. Used for help bots that answer from your docs.

### Rate limit

The maximum number of requests or *tokens* a service accepts from you per minute or per day. Above it, the service answers with an error (often `429`) until the next period.

### Secret

A value that must stay private, such as an *API key*, a password or a token. Secrets live in a host's secret settings or a secret manager, and reach the app as *environment variables*, never in the code. → [Security](Security-for-AI-apps.md#secrets-and-api-keys)

### Serverless

A way of hosting where you give the host a function and it runs it only when a request arrives, with a time limit per request. You pay per use, but long or always-on work does not fit. → [The cloud](Cloud-for-AI-apps.md#serverless-containers-or-vms)

### Snapshot

A fixed version of a *model* that does not change behind your back, identified by an exact model ID. An alias, by contrast, can move to a newer version. → [How versions work](Model-names-and-versions.md)

### Streaming

Sending an answer piece by piece as it is produced, instead of all at once at the end. Chat apps stream so you see words appear; this needs a connection that stays open, which affects hosting. → [Time limits and streaming](Cloud-for-AI-apps.md#time-limits-and-streaming)

### System prompt

Instructions given to a *model* before the conversation starts, setting its role, rules and limits ("You are a support assistant for…; never…").

### Temperature

A setting that controls how varied a *model*'s answers are: low gives more predictable wording, high more varied. Even at zero, answers are not perfectly repeatable.

### Token

The small piece of text a *model* reads and writes: a word, part of a word or a punctuation mark. Prices and limits are counted in tokens. OpenAI's rule of thumb for English: "1 token is approximately 4 characters or 0.75 words" ([OpenAI docs](https://developers.openai.com/api/docs/concepts), checked 2026-10-28). → [What it costs](Generative-AI.md#what-it-costs)

### Tool

A function an *agent* is allowed to use, such as "search the web", "read a file" or "run a command". The model asks for the tool; your program runs it and returns the result. Also called tool use or function calling. → [What an AI agent is](AI-agent.md#the-three-parts-model-tools-instructions)

### Workflow

A fixed sequence of steps, written in code in advance, in which a *model* may do some steps. Unlike an *agent*, the model does not choose what comes next. → [Chatbot, workflow, agent](AI-agent.md#chatbot-workflow-agent)

### Zero data retention (ZDR)

An arrangement where a *provider* does not store your requests and answers after it has processed them. Usually only for business customers, sometimes only on approval. → [Data protection by vendor](Data-protection-by-vendor.md)

## Related pages

- [What generative AI is](Generative-AI.md)
- [What an AI agent is](AI-agent.md)
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md)
- [All pages by category](_Sidebar.md)

## See also

<!-- SEEALSO:START -->
- [All pages, by category](_Sidebar.md)
- [All tags](Tags.md)
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28.

- Anthropic, [Glossary](https://platform.claude.com/docs/en/about-claude/glossary)
- OpenAI, [Key concepts](https://developers.openai.com/api/docs/concepts)
- Facts about A2A and MCP: see the [sources of the agents page](Multi-agent-systems.md#sources)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake or a missing word? [Open an issue](CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](LICENSE).
