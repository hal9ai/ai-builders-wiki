---
title: "Multi-agent systems: do AI agents work with each other?"
description: "Manager and helpers, handoffs, cross-organization agents, frameworks, and what the evidence says works."
category: Agents
tags: [agents]
order: 2
checked: 2026-10-28
---

<!-- NAV:START -->
[Home](README.md) › [Agents](Category-Agents.md) · Tags: [agents](Tag-agents.md)
<!-- NAV:END -->

# Multi-agent systems: do AI agents work with each other?

**Yes: [agents](Glossary.md#agent) can call other agents, hand a task over to them, or exchange messages through a protocol, but most production systems that work well still use one agent, or one lead agent with helpers.** Splitting work across agents helps when the parts are independent. It hurts when the parts need the same context.

This page assumes you know [what an agent is](AI-agent.md).

## Three ways agents interact

**1. Manager and helpers ("agents as tools").** A lead agent calls other agents as if they were [tools](Glossary.md#tool), then combines their answers. OpenAI describes this as "A central 'manager' agent coordinates multiple specialized agents via tool calls" ([OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), p. 17, checked 2026-10-28).

*Example:* a research agent sends three helper agents to search three topics in parallel, then writes one report from their notes.

**2. Handoffs (peers).** One agent passes the whole conversation to another, which takes over. OpenAI: "Multiple agents operate as peers, handing off tasks to one another based on their specializations" (same guide, p. 17). The OpenAI Agents SDK has this built in: handoffs "allow agents to delegate to other agents for specific tasks" ([OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), checked 2026-10-28).

*Example:* a support triage agent hands a billing question to a billing agent that has access to the payments tool, and a bug report to a technical agent.

The difference, in OpenAI's words: "In the manager pattern, edges represent tool calls whereas in the decentralized pattern, edges represent handoffs that transfer execution between agents" (p. 17).

**3. Across organizations, through a protocol.** An agent built by one company calls an agent run by another, over the network. This is what [A2A](Agent-protocols-MCP-and-A2A.md#a2a-agents-talking-to-agents) is for.

## What the evidence says

**Multi-agent systems can do better on broad, parallel tasks, at a much higher [token](Glossary.md#token) cost, and they fail in characteristic ways.**

- **It can help.** Anthropic reports that its multi-agent research system "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval" ([Anthropic, How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), June 2025, checked 2026-10-28). That is an internal evaluation by the vendor, on research tasks.
- **It costs more.** The same post: "multi-agent systems use about 15× more tokens than chats".
- **It suits some tasks, not others.** Anthropic: these systems "excel at valuable tasks that involve heavy parallelization", while "most coding tasks involve fewer truly parallelizable tasks than research", and some domains "require all agents to share the same context".
- **Context is the main problem.** Cognition, which builds a [coding agent](Glossary.md#coding-agent), argues against multi-agent designs for that reason. Its first principle: "Share context, and share full agent traces, not just individual messages"; its second: "Actions carry implicit decisions, and conflicting decisions carry bad results" ([Cognition, Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents), June 2025, checked 2026-10-28).
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

## Protocols: MCP and A2A

**Two open protocols matter here: [MCP](Glossary.md#mcp-model-context-protocol) connects an agent to tools, [A2A](Glossary.md#a2a-agent2agent) connects an agent to another agent.** Both are explained on [Agent protocols: MCP and A2A](Agent-protocols-MCP-and-A2A.md).


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
5. **What may each agent touch?** Give each the fewest tools and narrowest credentials it needs. See [security](Security-for-AI-apps.md#tool-permissions).

## Related pages

- [What an AI agent is](AI-agent.md)
- [Ways to use AI](Ways-to-use-AI.md): agent SDKs among other surfaces
- [Security](Security-for-AI-apps.md)
- [Glossary](Glossary.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [A2A (Agent2Agent)](Glossary.md#a2a-agent2agent), [Agent](Glossary.md#agent), [Agent SDK](Glossary.md#agent-sdk), [Coding agent](Glossary.md#coding-agent), [Deploy](Glossary.md#deploy), [LLM](Glossary.md#llm), [MCP (Model Context Protocol)](Glossary.md#mcp-model-context-protocol), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-10-28.

- OpenAI, [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF)
- OpenAI, [Agents SDK](https://openai.github.io/openai-agents-python/)
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (June 2025)
- Cognition, [Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) (June 2025)
- Cemri et al., [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) (arXiv, 2025)
- Framework pages linked in the table above

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Open an issue](CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](LICENSE).
