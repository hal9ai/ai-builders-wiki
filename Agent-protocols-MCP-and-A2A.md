---
title: "Agent protocols: MCP and A2A"
description: "What the Model Context Protocol and the Agent2Agent protocol are, how they differ, and their status as of October 2026."
category: Agents
tags: [agents, mcp]
order: 3
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Agents](Category-Agents.md) · Tags: [agents](Tag-agents.md), [mcp](Tag-mcp.md)
<!-- NAV:END -->

# Agent protocols: MCP and A2A

**[MCP](Glossary.md#mcp-model-context-protocol) connects an [agent](Glossary.md#agent) to [tools](Glossary.md#tool) and data; [A2A](Glossary.md#a2a-agent2agent) connects an agent to other agents.** Both are open specifications now hosted under the Linux Foundation, and both change often, so the versions below are dated.

This page assumes you know [what an agent is](AI-agent.md). How agents are combined, with or without these protocols, is on [Multi-agent systems](Multi-agent-systems.md).

## MCP: connecting agents to tools

**The Model Context Protocol (MCP) is an open standard for plugging tools and data into an AI app; it connects an agent to tools, not to other agents.** The specification calls it "an open protocol that enables seamless integration between LLM applications and external data sources and tools" ([MCP specification](https://modelcontextprotocol.io/specification/latest), checked 2026-10-28).

- **Origin and governance.** Anthropic open-sourced MCP in November 2024 ([Anthropic announcement](https://www.anthropic.com/news/model-context-protocol)). In December 2025, "Anthropic is donating MCP to the Agentic AI Foundation, a directed fund under the Linux Foundation" ([MCP blog](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/), checked 2026-10-28).
- **Versions.** The spec is versioned by date. "The current protocol version is 2026-07-28" ([MCP versioning](https://modelcontextprotocol.io/specification/versioning), checked 2026-10-28).
- **Parts.** An MCP *server* offers tools, resources (data) and [prompts](Glossary.md#prompt). An MCP *client*, inside an app such as a chat app or [coding agent](Glossary.md#coding-agent), connects to it. Messages use JSON-RPC 2.0.
- **Transports.** Two ways to connect ([MCP transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports), checked 2026-10-28):
  - **stdio:** the app starts the server as a local process and talks over standard input and output. Good for tools on your own machine.
  - **Streamable HTTP:** "each message is an HTTP POST to a single MCP endpoint". This is how a *remote* MCP server runs, hosted like any web service. See [the cloud for AI apps](Cloud-for-AI-apps.md).

*Example:* a company runs an MCP server that exposes "search our tickets" and "create a ticket". Any MCP-capable assistant its staff use can then work with tickets, without a custom integration for each assistant.

One MCP server can itself call a model, so an "agent behind a tool" is possible. But MCP's design centres on tools for one agent, and its security questions (who may call which tool, with whose [token](Glossary.md#token)) are covered on the [security page](Security-for-AI-apps.md#mcp-servers-and-tool-permissions).

## A2A: agents talking to agents

**Agent2Agent (A2A) is an open protocol for one agent to discover another agent, send it a task and follow the task's progress, across vendors and organizations.** Its site calls it "an open standard for seamless communication and collaboration between AI agents", "originally developed by Google and donated to the Linux Foundation" ([A2A](https://a2a-protocol.org/latest/), checked 2026-10-28).

- **Agent Card.** Each agent publishes "A JSON metadata document … describing its identity, capabilities, skills, service endpoint" so others can find out what it does and how to call it ([A2A specification](https://a2a-protocol.org/latest/specification/), checked 2026-10-28).
- **Task.** "The fundamental unit of work managed by A2A, identified by a unique ID." Tasks have a lifecycle (submitted, working, completed and so on), so long jobs can report progress.
- **Version.** The specification page lists 1.0.0 as the latest released version (checked 2026-10-28).
- **Consolidation.** IBM's Agent Communication Protocol (ACP) "is officially merging with the A2A under the Linux Foundation umbrella" ([LF AI & Data, August 2025](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/), checked 2026-10-28).

**MCP and A2A are complementary:** MCP is how an agent uses tools; A2A is how an agent asks another agent, which may use its own tools, to do a job.

A2A is younger than MCP in practice. Most teams today build multi-agent systems inside one program with a framework, and use A2A only when the other agent belongs to someone else.

## Related pages

- [Multi-agent systems](Multi-agent-systems.md)
- [What an AI agent is](AI-agent.md)
- [Security for AI apps](Security-for-AI-apps.md#mcp-servers-and-tool-permissions): MCP risks
- [The cloud, for AI apps](Cloud-for-AI-apps.md): hosting a remote MCP server

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [A2A (Agent2Agent)](Glossary.md#a2a-agent2agent), [Agent](Glossary.md#agent), [Cloud](Glossary.md#cloud), [Coding agent](Glossary.md#coding-agent), [LLM](Glossary.md#llm), [MCP (Model Context Protocol)](Glossary.md#mcp-model-context-protocol), [Model](Glossary.md#model), [Prompt](Glossary.md#prompt), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28.

- Anthropic, [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (November 2024)
- Model Context Protocol, [Specification](https://modelcontextprotocol.io/specification/latest), [Versioning](https://modelcontextprotocol.io/specification/versioning), [Transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
- MCP blog, [MCP joins the Agentic AI Foundation](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/) (December 2025)
- A2A, [Overview](https://a2a-protocol.org/latest/), [Specification](https://a2a-protocol.org/latest/specification/)
- LF AI & Data, [ACP joins forces with A2A](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/) (August 2025)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Open an issue](CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](LICENSE).
