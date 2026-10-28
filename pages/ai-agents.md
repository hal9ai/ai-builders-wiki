---
title: "What an AI agent is"
description: "How an agent differs from a chatbot and from a workflow: tools, the loop, and levels of autonomy."
category: Concepts
tags: [agents, tools, workflows, autonomy]
checked: 2026-10-28
---

# What an AI agent is

**An AI agent is a program in which a language model decides, step by step, which actions to take with the tools it has been given, and keeps going until the task is done or it is stopped.** A chatbot only answers; an agent acts.

Definitions vary between vendors, but they agree on the core. OpenAI: "Agents are systems that independently accomplish tasks on your behalf" ([OpenAI, A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), p. 4, checked 2026-10-28). Anthropic's Agent SDK docs: "An agent is an application that completes a task by planning its own steps and calling tools that read files, run commands, or edit code" ([Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), checked 2026-10-28).

## Chatbot, workflow, agent

**The difference is who decides the next step: the person, your code, or the model.**

| | Chatbot | Workflow | Agent |
|---|---|---|---|
| Who decides the next step | The person typing | Your code, written in advance | The model, at run time |
| Uses tools | No, or one fixed lookup | Yes, in a fixed order | Yes, chosen as it goes |
| Number of model calls | One per message | A fixed number | Unknown in advance |
| Example | "Rewrite this email more politely" | Every new invoice: extract fields → check totals → save to the database | "This test fails; find out why and fix it" |
| Main risk | A wrong answer | A wrong answer at one step | Wrong actions, repeated, at your expense |

Anthropic draws the same line. Workflows are "systems where LLMs and tools are orchestrated through predefined code paths"; agents are "systems where LLMs dynamically direct their own processes and tool usage" ([Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents), December 2024, checked 2026-10-28). OpenAI says that "simple chatbots, single-turn LLMs, or sentiment classifiers—are not agents" ([OpenAI guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), p. 4).

Both vendors advise starting with the simplest option. Anthropic recommends "finding the simplest solution possible, and only increasing complexity when needed" ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)). Microsoft is blunter: "If you can write a function to handle the task, do that instead of using an AI agent" ([Microsoft Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/), checked 2026-10-28).

## The three parts: model, tools, instructions

**Every agent is a model, a set of tools, and instructions.** OpenAI's guide names exactly these three components (p. 7).

- **Model:** the LLM that reads the situation and picks the next action. See [providers and models](providers-and-models.md).
- **Tools:** functions the model may call: search the web, read a file, run a shell command, query a database, send an email. The model does not run them itself. It asks for a call ("run `pytest`"), your program runs it, and the result goes back to the model. This mechanism is called [tool use](glossary.md#tool) or function calling. [MCP](multi-agent-systems.md#mcp-connecting-agents-to-tools) is a common standard for plugging tools in.
- **Instructions:** the system prompt and project files that say what the agent is for, what it may do, and when to stop. Coding agents often read a file in the repository, such as `AGENTS.md` or `CLAUDE.md`, for project rules.

## The loop

**An agent runs in a loop: the model picks an action, the program runs it, the model reads the result, and repeats.** OpenAI: a run is "typically implemented as a loop that lets agents operate until an exit condition is reached" ([OpenAI guide](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf), p. 14).

A concrete run of a coding agent asked to fix a failing test:

1. Model: "Run the tests." → program runs `npm test` → 1 failure in `cart.test.js`.
2. Model: "Read `cart.js`." → program returns the file.
3. Model: "Edit line 42: the discount is applied twice." → program edits the file.
4. Model: "Run the tests again." → all pass.
5. Model: "Done. Here is what I changed and why." → loop ends.

Exit conditions are usually: the model says it is done, a step or cost limit is reached, an error occurs, or a person stops it. Without limits, a confused agent can loop for a long time, and every turn costs tokens. Anthropic measured that its agents "typically use about 4× more tokens than chat interactions" ([Anthropic, multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), June 2025, checked 2026-10-28).

## Levels of autonomy

**How much an agent may do without asking is a design choice, separate from how capable its model is.** A research paper from the University of Washington proposes "five levels of escalating agent autonomy, characterized by the roles a user can take when interacting with an agent: operator, collaborator, consultant, approver, and observer" ([Feng, McDonald and Zhang, Levels of Autonomy for AI Agents, arXiv 2506.12469](https://arxiv.org/abs/2506.12469), 2025, checked 2026-10-28).

In practice, coding agents expose this as permission settings. A simplified ladder, as you will meet it in tools:

| Level | What the agent may do alone | Typical setting |
|---|---|---|
| Suggest | Nothing; it proposes, you apply | Chat, autocomplete |
| Ask each time | Read freely; every edit or command needs your approval | Default in many coding agents |
| Allow-listed | Run approved commands (tests, linters) alone; ask for the rest | Per-project permission files |
| Autonomous in a sandbox | Anything inside an isolated container or VM, no access to your real accounts | Cloud agents, CI runners |
| Autonomous with real credentials | Deploy, pay, email, change production | Only with tight scopes and spend limits |

The ladder is our summary, not a standard. Each step up saves human time and raises the cost of a mistake, so the right level depends on what the tools can reach. The [security page](security.md#tool-permissions) covers how to set it.

## When an agent is the wrong tool

- **The steps are known in advance.** Write a workflow: cheaper, faster, testable.
- **One call is enough.** Summarizing a text or classifying a ticket needs no loop.
- **Mistakes are expensive and hard to undo.** Keep a person as the approver for those actions.
- **You cannot check the result.** An agent that "fixed" something you cannot test only moved the uncertainty.

## Related pages

- [Do agents talk to each other?](multi-agent-systems.md): multi-agent patterns, MCP, A2A
- [Ways to use AI](ways-to-use-ai.md): where you meet agents (coding CLIs, IDEs, SDKs)
- [Security](security.md): prompt injection and tool permissions
- [Glossary](glossary.md)

## Sources

All checked on 2026-10-28.

- Anthropic, [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) (December 2024)
- Anthropic, [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) (June 2025)
- Anthropic, [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview)
- OpenAI, [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF)
- Microsoft, [Agent Framework overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- Feng, McDonald, Zhang, [Levels of Autonomy for AI Agents](https://arxiv.org/abs/2506.12469) (arXiv, 2025)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Open an issue](../CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](../LICENSE).
