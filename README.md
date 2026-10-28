# Deploying AI apps

**A practical, sourced, vendor-neutral wiki about building and running apps that use AI: what the pieces are, how agents work, which providers exist, what they do with your data, and how to get an AI app online safely.** It is written for developers and for founders who build with AI without being full-time programmers.

Each page answers one question in its first sentence, then gives context, examples and caveats. Every claim about a vendor or product links to that vendor's own page, with the date it was checked.

**Who makes it.** This wiki is made by [Hal9](https://hal9.com). Hal9 also runs [Cloudish](https://cloudish.ai), a cloud host where AI agents deploy apps. Cloudish appears on a few pages as a disclosed example, next to other hosts; it is never a recommendation. If you think a page favours anyone unfairly, please [open an issue](CONTRIBUTING.md#report-a-mistake).

**How it is written.** Pages are drafted with AI assistance, then checked against their sources; each page says when. Facts in this field change monthly, model names especially. Nothing here is legal or security advice.

## Start here

New to the subject? Read in this order: [Glossary](pages/glossary.md) → [What generative AI is](pages/generative-ai.md) → [What an AI agent is](pages/ai-agents.md) → [From idea to deployed AI app](pages/idea-to-deployed-app.md).

<!-- INDEX:START -->

## Pages by category

### Agents

- [What an AI agent is](pages/ai-agents.md): How an agent differs from a chatbot and from a workflow: tools, the loop, and levels of autonomy.
- [Do AI agents work with each other? How?](pages/multi-agent-systems.md): Multi-agent patterns, handoffs, MCP and A2A, and what the evidence says works.

### Foundations

- [The cloud, for AI apps](pages/cloud-for-ai-apps.md): Three different jobs: hosting your app, calling a model, running a model on GPUs. And serverless vs containers vs VMs.
- [What generative AI is, and why people build with it](pages/generative-ai.md): What the models do, what developers and founders use them for, where they fail, and how the bill works.
- [Glossary: the basic words](pages/glossary.md): The core terms a newcomer meets, each defined in plain words, with links to the pages that go deeper.
- [AI providers and models: who makes what, and how to choose](pages/providers-and-models.md): The main model makers as of October 2026, open-weight vs closed, how model names and versions work, and how to pick one.
- [Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs](pages/ways-to-use-ai.md): The surfaces through which people and programs use models, and what each one is for.

### Guides

- [From idea to deployed AI app: a typical workflow](pages/idea-to-deployed-app.md): One concrete path, end to end: build with an assistant, keys and secrets, deploy, logs, costs, updates.

### Operations

- [Data protection: what AI vendors do with your data](pages/data-protection.md): Training by default, retention, consumer vs business terms, opt-outs, zero data retention and data location, compared vendor by vendor.
- [Security for AI apps and agents](pages/security.md): The risks that are specific to apps that call models and to agents that act: prompt injection, secrets, scopes, tool permissions, supply chain, runaway costs.

## Tags

- **a2a**: [Do AI agents work with each other? How?](pages/multi-agent-systems.md)
- **agents**: [What an AI agent is](pages/ai-agents.md), [Do AI agents work with each other? How?](pages/multi-agent-systems.md), [Security for AI apps and agents](pages/security.md), [Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs](pages/ways-to-use-ai.md)
- **api**: [Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs](pages/ways-to-use-ai.md)
- **autonomy**: [What an AI agent is](pages/ai-agents.md)
- **cloud**: [The cloud, for AI apps](pages/cloud-for-ai-apps.md)
- **coding-agents**: [From idea to deployed AI app: a typical workflow](pages/idea-to-deployed-app.md), [Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs](pages/ways-to-use-ai.md)
- **costs**: [What generative AI is, and why people build with it](pages/generative-ai.md), [From idea to deployed AI app: a typical workflow](pages/idea-to-deployed-app.md), [AI providers and models: who makes what, and how to choose](pages/providers-and-models.md)
- **data-protection**: [Data protection: what AI vendors do with your data](pages/data-protection.md)
- **deploy**: [From idea to deployed AI app: a typical workflow](pages/idea-to-deployed-app.md)
- **eu**: [Data protection: what AI vendors do with your data](pages/data-protection.md)
- **generative-ai**: [What generative AI is, and why people build with it](pages/generative-ai.md)
- **glossary**: [Glossary: the basic words](pages/glossary.md)
- **gpu**: [The cloud, for AI apps](pages/cloud-for-ai-apps.md)
- **hosting**: [The cloud, for AI apps](pages/cloud-for-ai-apps.md), [From idea to deployed AI app: a typical workflow](pages/idea-to-deployed-app.md)
- **llm**: [What generative AI is, and why people build with it](pages/generative-ai.md)
- **mcp**: [Do AI agents work with each other? How?](pages/multi-agent-systems.md), [Security for AI apps and agents](pages/security.md)
- **models**: [AI providers and models: who makes what, and how to choose](pages/providers-and-models.md)
- **multi-agent**: [Do AI agents work with each other? How?](pages/multi-agent-systems.md)
- **open-weight**: [AI providers and models: who makes what, and how to choose](pages/providers-and-models.md)
- **prompt-injection**: [Security for AI apps and agents](pages/security.md)
- **providers**: [Data protection: what AI vendors do with your data](pages/data-protection.md), [AI providers and models: who makes what, and how to choose](pages/providers-and-models.md)
- **retention**: [Data protection: what AI vendors do with your data](pages/data-protection.md)
- **secrets**: [From idea to deployed AI app: a typical workflow](pages/idea-to-deployed-app.md), [Security for AI apps and agents](pages/security.md)
- **security**: [Security for AI apps and agents](pages/security.md)
- **serverless**: [The cloud, for AI apps](pages/cloud-for-ai-apps.md)
- **streaming**: [The cloud, for AI apps](pages/cloud-for-ai-apps.md)
- **tokens**: [What generative AI is, and why people build with it](pages/generative-ai.md)
- **tools**: [What an AI agent is](pages/ai-agents.md), [Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs](pages/ways-to-use-ai.md)

<!-- INDEX:END -->

## Contributing and licence

Corrections are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md). The index above is generated from each page's front matter by `python3 scripts/build_index.py`, which also checks that every internal link resolves.

Text is licensed under [CC BY 4.0](LICENSE). The index script is under the MIT licence.
