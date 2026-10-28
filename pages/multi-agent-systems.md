---
title: "Do AI agents work with each other? How?"
description: "Multi-agent patterns, handoffs, MCP and A2A, and what the evidence says works."
category: Agents
tags: [agents, multi-agent, mcp, a2a]
checked: 2026-10-28
---

# Do AI agents work with each other? How?

**Yes: agents can call other agents, hand a task over to them, or exchange messages through a protocol, but most production systems that work well still use one agent, or one lead agent with helpers.** Splitting work across agents helps when the parts are independent. It hurts when the parts need the same context.

This page assumes you know [what an agent is](ai-agents.md).

## Three ways agents interact

**1. Manager and helpers ("agents as tools").** A lead agent calls other agents as if they were tools, then combines their answers. OpenAI describes this as "A central 'manager' agent coordinates multiple specialized agents via tool calls" ([OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), p. 17, checked 2026-10-28).

*Example:* a research agent sends three helper agents to search three topics in parallel, then writes one report from their notes.

**2. Handoffs (peers).** One agent passes the whole conversation to another, which takes over. OpenAI: "Multiple agents operate as peers, handing off tasks to one another based on their specializations" (same guide, p. 17). The OpenAI Agents SDK has this built in: handoffs "allow agents to delegate to other agents for specific tasks" ([OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), checked 2026-10-28).

*Example:* a support triage agent hands a billing question to a billing agent that has access to the payments tool, and a bug report to a technical agent.

The difference, in OpenAI's words: "In the manager pattern, edges represent tool calls whereas in the decentralized pattern, edges represent handoffs that transfer execution between agents" (p. 17).

**3. Across organizations, through a protocol.** An agent built by one company calls an agent run by another, over the network. This is what [A2A](#a2a-agents-talking-to-agents) is for.

## What the evidence says

**Multi-agent systems can do better on broad, parallel tasks, at a much higher token cost, and they fail in characteristic ways.**

- **It can help.** Anthropic reports that its multi-agent research system "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval" ([Anthropic, How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), June 2025, checked 2026-10-28). That is an internal evaluation by the vendor, on research tasks.
- **It costs more.** The same post: "multi-agent systems use about 15× more tokens than chats".
- **It suits some tasks, not others.** Anthropic: these systems "excel at valuable tasks that involve heavy parallelization", while "most coding tasks involve fewer truly parallelizable tasks than research", and some domains "require all agents to share the same context".
- **Context is the main problem.** Cognition, which builds a coding agent, argues against multi-agent designs for that reason. Its first principle: "Share context, and share full agent traces, not just individual messages"; its second: "Actions carry implicit decisions, and conflicting decisions carry bad results" ([Cognition, Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents), June 2025, checked 2026-10-28).
- **Failures are common and classifiable.** A study of more than 1,600 annotated traces from 7 multi-agent frameworks found that "their performance gains on popular benchmarks are often minimal", and grouped 14 failure modes into three categories: system design issues, misalignment between agents, and task verification ([Cemri et al., Why Do Multi-Agent LLM Systems Fail?, arXiv 2503.13657](https://arxiv.org/abs/2503.13657), 2025, checked 2026-10-28).

Vendors converge on the same advice. OpenAI: "Our general recommendation is to maximize a single agent's capabilities first" ([OpenAI guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), p. 16).

### Works vs hype, in short

| Claim | What the sources support |
|---|---|
| "Teams of agents beat one agent" | Sometimes, for parallel research-like tasks, at many times the tokens |
| "Split a coding task across agents" | Risky: parts depend on shared decisions |
| "Parallel helpers that only read and report" | Works well: little shared state, the lead decides |
| "Agents negotiating freely with each other" | Little evidence in production; failure studies show coordination is the weak point |
| "A standard protocol solves interoperability" | It solves the wire format, not trust, quality or cost |

## MCP: connecting agents to tools

**The Model Context Protocol (MCP) is an open standard for plugging tools and data into an AI app; it connects an agent to tools, not to other agents.** The specification calls it "an open protocol that enables seamless integration between LLM applications and external data sources and tools" ([MCP specification](https://modelcontextprotocol.io/specification/latest), checked 2026-10-28).

- **Origin and governance.** Anthropic open-sourced MCP in November 2024 ([Anthropic announcement](https://www.anthropic.com/news/model-context-protocol)). In December 2025, "Anthropic is donating MCP to the Agentic AI Foundation, a directed fund under the Linux Foundation" ([MCP blog](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/), checked 2026-10-28).
- **Versions.** The spec is versioned by date. "The current protocol version is 2026-07-28" ([MCP versioning](https://modelcontextprotocol.io/specification/versioning), checked 2026-10-28).
- **Parts.** An MCP *server* offers tools, resources (data) and prompts. An MCP *client*, inside an app such as a chat app or coding agent, connects to it. Messages use JSON-RPC 2.0.
- **Transports.** Two ways to connect ([MCP transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports), checked 2026-10-28):
  - **stdio:** the app starts the server as a local process and talks over standard input and output. Good for tools on your own machine.
  - **Streamable HTTP:** "each message is an HTTP POST to a single MCP endpoint". This is how a *remote* MCP server runs, hosted like any web service. See [the cloud for AI apps](cloud-for-ai-apps.md).

*Example:* a company runs an MCP server that exposes "search our tickets" and "create a ticket". Any MCP-capable assistant its staff use can then work with tickets, without a custom integration for each assistant.

One MCP server can itself call a model, so an "agent behind a tool" is possible. But MCP's design centres on tools for one agent, and its security questions (who may call which tool, with whose token) are covered on the [security page](security.md#mcp-servers-and-tool-permissions).

## A2A: agents talking to agents

**Agent2Agent (A2A) is an open protocol for one agent to discover another agent, send it a task and follow the task's progress, across vendors and organizations.** Its site calls it "an open standard for seamless communication and collaboration between AI agents", "originally developed by Google and donated to the Linux Foundation" ([A2A](https://a2a-protocol.org/latest/), checked 2026-10-28).

- **Agent Card.** Each agent publishes "A JSON metadata document … describing its identity, capabilities, skills, service endpoint" so others can find out what it does and how to call it ([A2A specification](https://a2a-protocol.org/latest/specification/), checked 2026-10-28).
- **Task.** "The fundamental unit of work managed by A2A, identified by a unique ID." Tasks have a lifecycle (submitted, working, completed and so on), so long jobs can report progress.
- **Version.** The specification page lists 1.0.0 as the latest released version (checked 2026-10-28).
- **Consolidation.** IBM's Agent Communication Protocol (ACP) "is officially merging with the A2A under the Linux Foundation umbrella" ([LF AI & Data, August 2025](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/), checked 2026-10-28).

**MCP and A2A are complementary:** MCP is how an agent uses tools; A2A is how an agent asks another agent, which may use its own tools, to do a job.

A2A is younger than MCP in practice. Most teams today build multi-agent systems inside one program with a framework, and use A2A only when the other agent belongs to someone else.

## Frameworks for multi-agent systems

**Frameworks handle the loop, tool calls, handoffs and state for you; they do not decide whether you need several agents.** Each description below is the project's own.

| Framework | By | Its own description |
|---|---|---|
| [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | OpenAI | "build agentic AI apps in a lightweight, easy-to-use package with very few abstractions" |
| [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) | Anthropic | "Build production AI agents with Claude Code as a library" |
| [Agent Development Kit (ADK)](https://adk.dev/) | Google | "the open-source agent development framework that lets you build, debug, and deploy reliable AI agents" |
| [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/) | Microsoft | "the next generation of both Semantic Kernel and AutoGen" |
| [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) | LangChain | "a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful" agents |
| [CrewAI](https://docs.crewai.com/) | CrewAI | "Build collaborative AI agents, crews, and flows" |

All checked 2026-10-28.

## Practical checklist before going multi-agent

1. **Can one agent with better tools do it?** Try that first.
2. **Are the sub-tasks independent?** If they share decisions, keep them in one agent.
3. **Who checks the combined result?** Give the lead agent, or a person, an explicit verification step.
4. **What is the token budget?** Multiply your single-agent cost by the number of agents and turns, then set a limit.
5. **What may each agent touch?** Give each the fewest tools and narrowest credentials it needs. See [security](security.md#tool-permissions).

## Related pages

- [What an AI agent is](ai-agents.md)
- [Ways to use AI](ways-to-use-ai.md): agent SDKs among other surfaces
- [Security](security.md)
- [Glossary](glossary.md)

## Sources

All checked on 2026-10-28.

- OpenAI, [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF)
- OpenAI, [Agents SDK](https://openai.github.io/openai-agents-python/)
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (June 2025)
- Anthropic, [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) (November 2024)
- Cognition, [Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) (June 2025)
- Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) (arXiv, 2025)
- Model Context Protocol, [Specification](https://modelcontextprotocol.io/specification/latest), [Versioning](https://modelcontextprotocol.io/specification/versioning), [Transports](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports)
- MCP blog, [MCP joins the Agentic AI Foundation](https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/) (December 2025)
- A2A, [Overview](https://a2a-protocol.org/latest/), [Specification](https://a2a-protocol.org/latest/specification/)
- LF AI & Data, [ACP joins forces with A2A](https://lfaidata.foundation/communityblog/2025/08/29/acp-joins-forces-with-a2a-under-the-linux-foundations-lf-ai-data/) (August 2025)
- Framework pages linked in the table above

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Open an issue](../CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](../LICENSE).
