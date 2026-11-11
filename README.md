# AI Builders Wiki

**A practical, sourced, vendor-neutral wiki for people who build with AI: what the pieces are, how agents work, who makes the models, what vendors do with your data, and how to get an AI app online safely.** It is written for developers, and for founders who build with AI without being full-time programmers.

**How it is written.** Anyone can propose a change by pull request, written with or without AI help; maintainers review it against the sources before merging. Every claim about a vendor links to that vendor's own page, with the date it was checked, and each page's footer says how it was written and when it was last checked. Facts in this field change monthly, model names especially. Nothing here is legal or security advice.

## Start here

New to the subject? Read in this order:

1. [Glossary](Glossary.md): the basic words
2. [What generative AI is](Generative-AI.md)
3. [What an AI agent is](AI-agent.md)
4. [From idea to deployed AI app](Idea-to-deployed-AI-app.md)

## All pages

Also in the [sidebar](_Sidebar.md). Browse by [tag](Tags.md).

<!-- INDEX:START -->

### [Foundations](Category-Foundations.md)

- [Glossary: the basic words](Glossary.md): The core terms a newcomer meets, each defined in plain words, with links to the pages that go deeper.
- [What generative AI is, and why people build with it](Generative-AI.md): What the models do, what developers and founders use them for, where they fail, and how the bill works.
- [Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs](Ways-to-use-AI.md): The surfaces through which people and programs use models, and what each one is for.
- [The cloud, for AI apps](Cloud-for-AI-apps.md): Three different jobs: hosting your app, calling a model, running a model on GPUs. And serverless vs containers vs VMs.

### [Agents](Category-Agents.md)

- [What an AI agent is](AI-agent.md): How an agent differs from a chatbot and from a workflow: tools, the loop, and levels of autonomy.
- [Multi-agent systems: do AI agents work with each other?](Multi-agent-systems.md): Manager and helpers, handoffs, cross-organization agents, frameworks, and what the evidence says works.
- [Agent protocols: MCP and A2A](Agent-protocols-MCP-and-A2A.md): What the Model Context Protocol and the Agent2Agent protocol are, how they differ, and their status as of October 2026.
- [How an agent finds a tool you wrote](How-an-agent-finds-a-tool.md): An agent finds a tool through a skill file it reads — a folder with a SKILL.md whose name and one-line description it sees first and whose body it opens only when the job matches — so write the description for the match.

### [Models and providers](Category-Models-and-providers.md)

- [AI providers and models: who makes what, and how to choose](AI-providers-and-models.md): The main model makers as of October 2026, open-weight vs closed, where to get them, and how to pick one.
- [Model names and versions](Model-names-and-versions.md): How model families, tiers, snapshots, aliases and retirement dates work, vendor by vendor.

### [Security and data](Category-Security-and-data.md)

- [Security for AI apps and agents](Security-for-AI-apps.md): The risks that are specific to apps that call models and to agents that act: prompt injection, secrets, scopes, tool permissions, supply chain, runaway costs.
- [Data protection when you use AI](Data-protection.md): The five questions to ask any AI vendor, consumer vs business terms, and what to do in your own app.
- [Data protection by vendor](Data-protection-by-vendor.md): Training defaults, opt-outs, retention, zero data retention and data location for each major AI vendor, every cell sourced.
- [Where an AI app's terms of service and privacy policy should live](Legal-pages-for-an-AI-app.md): One canonical copy of each legal document, rendered as it is served: HTML for people and search, Markdown for agents, a last-known-good copy for outages.

### [How-to](Category-How-to.md)

- [From idea to deployed AI app: a typical workflow](Idea-to-deployed-AI-app.md): One concrete path, end to end: build with an assistant, keys and secrets, deploy, logs, costs, updates.
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md): Run it in a headless browser: load each page, click the main actions, and keep the console errors, failed requests and screenshots as evidence.
- [How to shrink a container image](Container-image-size.md): A working web server can fit in a few kilobytes: use a scratch image and a static binary. How to get there, what you give up, and how to measure the stored size.
- [Querying a web crawl from a small app](Querying-a-web-crawl-from-a-small-app.md): Read Common Crawl's Parquet index and hyperlink graph directly from a small container with DuckDB, without copying the data — and without the big join that runs a 256 MB container out of memory.
- [Where your keys come from: attribution for AI apps](Where-your-keys-come-from.md): When agents sign up instead of people, record a link ref, the agent and model the caller reports, and its HTTP client family, then count them by day.
- [How to point a domain at your app, with one record for every subdomain](Pointing-a-domain-at-your-app.md): Point one wildcard DNS record at your app's server so every app subdomain resolves without its own record, and one wildcard certificate covers them for HTTPS.
- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md): The deploy call returning is not the app running: wait for the build, check the port and read the logs before you believe it.
- [Serve one custom domain from more than one datacenter](Serve-one-domain-from-more-than-one-datacenter.md): One hostname for an app that runs in several datacenters: point the domain at one entry point that looks up which datacenter holds each name, and forward the rest with the Host header kept.
- [Persistent storage for many AI sandboxes](Persistent-storage-for-many-AI-sandboxes.md): A block volume per sandbox stops scaling at the host's per-machine limit: give each sandbox a directory on a shared filesystem, and plan isolation, quotas and snapshots.
- [Where an AI-built app keeps its data](Where-an-AI-built-app-keeps-its-data.md): Data that must outlive a visit, a restart or a redeploy belongs on the server, in a database or files on storage that outlives the container — not in the browser or in process memory.

### [Problems & solutions](Category-Problems-solutions.md)

- [An app that looks fine but its buttons do nothing](App-looks-fine-but-buttons-do-nothing.md): The page painted but no JavaScript ran: how to spot a script request that the server answered with an HTML page, and how to fix the rule that caused it.
- [A login that loops between your app and the sign-in provider](A-login-that-loops.md): The address bar flashes a callback URL with a code in it, over and over: how a page that redirects before the code is exchanged turns a sign-in into an endless loop, and how to fix it.
- [A sign-in that breaks behind a proxy: the redirect URI](A-sign-in-that-breaks-behind-a-proxy.md): The provider says the redirect URI does not match, or the callback address comes out as 'https,http://example.com': why a forwarded header can carry a list of values, and how to build the address safely.
- [Why a deploy looks broken in one browser but fine in another](Stale-cache-after-a-deploy.md): A new HTML page paired with an old cached CSS or JS file: how to spot it, and how to give assets a URL that changes when they do.

### Tags

[agents](Tag-agents.md) · [analytics](Tag-analytics.md) · [auth](Tag-auth.md) · [basics](Tag-basics.md) · [coding-agents](Tag-coding-agents.md) · [costs](Tag-costs.md) · [data](Tag-data.md) · [hosting](Tag-hosting.md) · [mcp](Tag-mcp.md) · [models](Tag-models.md) · [privacy](Tag-privacy.md) · [providers](Tag-providers.md) · [secrets](Tag-secrets.md) · [security](Tag-security.md) · [skills](Tag-skills.md) · [storage](Tag-storage.md)

<!-- INDEX:END -->

## How this wiki works

- **Pages** are Markdown files at the top level of the repository, named in wiki style (`AI-agent.md`). Each starts with a breadcrumb, answers its question in the first sentence, and ends with *Related pages*, *See also*, *Sources* and a footer.
- **Categories and tags** live in each page's front matter. They were chosen from the pages as they were written, and will change.
- **Navigation** (this index, the sidebar, the category and tag pages, the breadcrumbs and the glossary links under *See also*) is generated by `python3 scripts/build_wiki.py`, which also checks that every internal link resolves.

## Contribute

This wiki is open to everyone. Fix a sentence, update a fact that changed, add a page, or translate one: open a pull request, or an issue if you'd rather point at a problem. How, in [CONTRIBUTING.md](CONTRIBUTING.md).

## About this wiki

Started by the team behind [Cloudish](https://cloudish.ai/?ref=cc-wiki), at [Hal9](https://hal9.com). Cloudish appears on a few pages as one example among other hosts, and says so where it does. If a page favours anyone unfairly, please [open an issue](CONTRIBUTING.md#report-a-mistake).

## Licence

Text is licensed under [CC BY 4.0](LICENSE). The build script is under the MIT licence.
