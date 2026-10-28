---
title: "Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs"
description: "The surfaces through which people and programs use models, and what each one is for."
category: Foundations
tags: [basics, coding-agents, agents]
order: 3
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Foundations](Category-Foundations.md) · Tags: [basics](Tag-basics.md), [coding-agents](Tag-coding-agents.md), [agents](Tag-agents.md)
<!-- NAV:END -->

# Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs

**The same [model](Glossary.md#model) can be used through very different surfaces: a chat app for a person, a coding [agent](Glossary.md#agent) that edits files, an [API](Glossary.md#api) that your own app calls, or an SDK to build your own agent.** Choosing the surface matters as much as choosing the model, because it decides who pays, who controls the data, and what the AI is allowed to touch.

Product names below are examples, checked on 2026-10-28. Many vendors offer every surface; see [providers and models](AI-providers-and-models.md).

## The surfaces at a glance

| Surface | Who uses it | What it is for | How you pay | Example |
|---|---|---|---|---|
| Chat app | A person | Questions, writing, analysis, quick prototypes | Free tier or subscription | ChatGPT, Claude, Gemini, Le Chat |
| Projects / workspaces | A person or a team | Ongoing work with shared files and instructions | Subscription | Claude Projects, ChatGPT Projects |
| Coding agent (CLI) | A developer | Reading, editing, testing and committing code in a repository | Subscription or API usage | Claude Code, Codex CLI, Gemini CLI |
| IDE integration | A developer | Autocomplete, chat and agent inside the editor | Subscription | GitHub Copilot, Cursor, editor extensions of the CLIs |
| Cloud coding agent | A developer or team | Works on an issue in the background and opens a pull request | Subscription | Copilot cloud agent, Codex web |
| API | Your program | Putting a model inside your own product | Per token | Any provider's API |
| Agent SDK | Your program | Building your own agent with a ready-made loop and tools | Per token, plus your hosting | Claude Agent SDK, OpenAI Agents SDK, Google ADK |

## Chat apps

**A chat app is the model with a user interface, for one person at a time.** It is the fastest way to try an idea, draft text or analyse a file. Most chat apps now also search the web, run code and connect to other services.

What it is not: a way to give *your* users AI. Your users cannot share your subscription; for that you use the [API](#apis).

Before pasting company or customer data, check what the vendor keeps and trains on for your plan. Consumer and business plans differ: see [data protection](Data-protection.md).

## Projects and workspaces

**A project keeps related chats, files and instructions together, so you do not re-explain the context every time.** Anthropic: "Projects allow you to create self-contained workspaces with their own chat histories and knowledge bases" ([Claude Help Center](https://support.claude.com/en/articles/9517075-what-are-projects), checked 2026-10-28). OpenAI offers [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt) for the same purpose.

*Example:* a founder keeps a "Pitch deck" project with the business plan, last quarter's numbers and the instruction "answer as a skeptical investor".

## Coding agents in the terminal

**A [coding agent](Glossary.md#coding-agent) is an [agent](AI-agent.md) that works in your code repository: it reads files, edits them, runs commands and checks the result.** Anthropic describes Claude Code as "an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools", available "in your terminal, IDE, desktop app, and browser" ([Claude Code overview](https://code.claude.com/docs/en/overview), checked 2026-10-28). OpenAI's Codex CLI is a "Lightweight coding agent that runs in your terminal" ([openai/codex on GitHub](https://github.com/openai/codex)). Google's Gemini CLI is "An open-source AI agent that brings the power of Gemini directly into your terminal" ([google-gemini/gemini-cli on GitHub](https://github.com/google-gemini/gemini-cli)).

Use one when the task touches many files or needs running and testing: "add a CSV export", "upgrade this library and fix what breaks", "deploy this to staging". Because it runs commands on your machine, its [permission settings](Security-for-AI-apps.md#tool-permissions) matter.

## IDE integrations and extensions

**IDE integrations put the model inside your editor: autocomplete as you type, a chat panel that sees your open files, and increasingly an agent mode.** GitHub describes Copilot as "an AI assistant that helps you write, understand, and ship software" ([GitHub docs](https://docs.github.com/en/copilot/get-started/what-is-github-copilot), checked 2026-10-28). Cursor is an editor built around this, which calls itself "your coding agent for building ambitious software" ([cursor.com](https://cursor.com/)). The terminal agents above also ship editor extensions.

The difference from a CLI agent is mostly ergonomics: you see diffs inline and steer as it goes. Under the hood, both are agents with [tools](Glossary.md#tool).

## Cloud coding agents

**A [cloud](Glossary.md#cloud) coding agent works on a copy of your repository on the vendor's machines, in the background, and returns a pull request.** GitHub: "Copilot can research a repository, plan changes, and implement them in the background" ([About Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent), checked 2026-10-28). OpenAI's Codex has a web version described as "the cloud-based agent from OpenAI" ([openai/codex on GitHub](https://github.com/openai/codex)).

Good for well-defined issues you can review afterwards. It runs in a sandbox, which limits what it can break, and what it can test.

## APIs

**An API lets your own program send a [prompt](Glossary.md#prompt) to a model and get the answer back, paying per [token](Glossary.md#token).** This is how you put AI inside a product: a support bot, a document summarizer, a feature in your app.

- You need an [API key](Glossary.md#api-key), kept on your server. See [security](Security-for-AI-apps.md#secrets-and-api-keys).
- Answers can be [streamed](Glossary.md#streaming) word by word.
- You pay for what your users trigger, so set spend limits. See [costs](Generative-AI.md#what-it-costs).
- Business and API terms usually differ from consumer terms on training and retention. See [data protection](Data-protection.md).

A minimal call, in Python with Anthropic's SDK (other [providers](Glossary.md#provider)' SDKs look similar):

```python
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
reply = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    messages=[{"role": "user", "content": "Summarize this ticket in one line: ..."}],
)
print(reply.content[0].text)
```

Model IDs change; take the current one from the provider's models page ([how versions work](Model-names-and-versions.md)).

## Agent SDKs

**An [agent SDK](Glossary.md#agent-sdk) gives you the agent loop, tool calling and context handling as a library, so you build an agent without writing that plumbing.** Anthropic's Claude Agent SDK offers "the same tools, agent loop, and context management that power Claude Code, programmable in Python and TypeScript" ([Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), checked 2026-10-28). OpenAI's Agents SDK aims to "build agentic AI apps in a lightweight, easy-to-use package with very few abstractions" ([OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)). Google's [ADK](https://adk.dev/), Microsoft's [Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/), LangGraph and CrewAI are other options; see [multi-agent frameworks](Multi-agent-systems.md#frameworks-for-multi-agent-systems).

Use an SDK when you want an agent that runs as part of *your* system: a nightly agent that triages issues, a support agent with access to your order database. It then needs hosting like any other app: see [the cloud for AI apps](Cloud-for-AI-apps.md).

## Which one should I use?

- **I want to think, write or analyse:** chat app; a project if it is recurring.
- **I want to build an app and I am not a developer:** a chat app or an AI app builder for a prototype, then a coding agent for anything you will maintain. Read [from idea to deployed AI app](Idea-to-deployed-AI-app.md).
- **I am a developer working in a codebase:** IDE integration for small edits, a coding agent for multi-file tasks, a cloud agent for issues you will review.
- **My product needs AI for its users:** the API.
- **My product needs an agent that acts on its own:** an agent SDK, hosted on your infrastructure.

## Related pages

- [What an AI agent is](AI-agent.md)
- [Providers and models](AI-providers-and-models.md)
- [Security](Security-for-AI-apps.md)
- [Glossary](Glossary.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [Agent SDK](Glossary.md#agent-sdk), [API](Glossary.md#api), [API key](Glossary.md#api-key), [Cloud](Glossary.md#cloud), [Coding agent](Glossary.md#coding-agent), [Deploy](Glossary.md#deploy), [Model](Glossary.md#model), [Prompt](Glossary.md#prompt), [Provider](Glossary.md#provider), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28, except where noted.

- Anthropic, [What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects)
- Anthropic, [Claude Code overview](https://code.claude.com/docs/en/overview)
- Anthropic, [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- OpenAI, [Projects in ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt) (the page refused automated access on 2026-10-28; existence confirmed through search results only)
- OpenAI, [Codex repository](https://github.com/openai/codex)
- OpenAI, [Agents SDK](https://openai.github.io/openai-agents-python/)
- Google, [Gemini CLI repository](https://github.com/google-gemini/gemini-cli); [Agent Development Kit](https://adk.dev/)
- GitHub, [What is GitHub Copilot?](https://docs.github.com/en/copilot/get-started/what-is-github-copilot); [About Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)
- Cursor, [cursor.com](https://cursor.com/)
- Microsoft, [Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Open an issue](CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](LICENSE).
