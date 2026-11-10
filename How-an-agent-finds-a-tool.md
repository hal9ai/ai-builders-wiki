---
title: "How an agent finds a tool you wrote"
description: "An agent finds a tool through a skill file it reads — a folder with a SKILL.md whose name and one-line description it sees first and whose body it opens only when the job matches — so write the description for the match."
category: Agents
tags: [agents, skills]
order: 4
checked: 2026-11-10
---

<!-- NAV:START -->
[Home](README.md) › [Agents](Category-Agents.md) · Tags: [agents](Tag-agents.md), [skills](Tag-skills.md)
<!-- NAV:END -->

# How an agent finds a tool you wrote

**An [agent](Glossary.md#agent) finds a tool through a file it reads, not through a page you publish: a skill file whose name and one-line description it loads up front, and whose body it opens only when the job matches.** The description is therefore the part that decides whether your tool is ever used, and the rest of the file only matters after it has won that match.

## A skill is a folder with a `SKILL.md`

Anthropic's Agent Skills are "modular capabilities that extend Claude's functionality. Each Skill packages instructions, metadata, and optional resources (scripts, templates) that Claude uses automatically when relevant" ([Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), checked 2026-11-10). In practice a skill is a directory holding a `SKILL.md` with YAML front matter, plus any scripts and reference files it needs. Claude Code looks for them in `~/.claude/skills/` (personal) and `.claude/skills/` (project).

The file is loaded in stages, which is the whole design:

| Level | What it is | When it loads | Cost in the context window |
|---|---|---|---|
| 1 | `name` and `description` from the front matter | At startup, for every installed skill | About 100 [tokens](Glossary.md#token) per skill |
| 2 | The body of `SKILL.md` | When the description matches the request | Under 5k tokens |
| 3 | Bundled files and scripts | When the instructions point to them | Nothing until read; a script's code never enters the context |

Two fields are required: `name`, up to 64 characters of lowercase letters, numbers and hyphens, and `description`, up to 1,024 characters. "The `description` is what Claude matches your request against when determining whether to trigger the Skill, so it must say both what the Skill does and when to use it" ([Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), checked 2026-11-10).

So write the description as the trigger, not as a summary: name the thing ("deploy a container", "parse a PDF"), then the situations that should wake it ("when the user mentions a Dockerfile or asks for a public URL"). The body can be long; the description cannot.

## The same shape shows up in other agents

The format is not tied to one vendor. AMD's GAIA keeps its skills in the same shape — "a skill is a reusable capability *any* agent composes — a procedure written for a model to follow, plus the tools it needs" — as one directory per skill under `hub/skills/`, with a required `SKILL.md`, an optional `tools.py`, and an optional `scripts/` ([GAIA skills README](https://github.com/amd/gaia/blob/main/hub/skills/README.md), checked 2026-11-10). Its front matter carries the same kind of identity (`name`, `version`, `description`, `license`) and adds what that platform gates on: a security tier, permissions, the tools the skill requires and its provenance.

GAIA also shows the other half of discovery: a way to publish. `gaia skill publish ./<name>/` takes the skill's identity from its front matter and ships the directory as the bundle ([GAIA skills README](https://github.com/amd/gaia/blob/main/hub/skills/README.md), checked 2026-11-10). Writing the folder is step one; putting it where an agent's platform lists it is step two, and that step is a submission to the platform, not something you publish on your own site.

## Project instructions are a different file

An `AGENTS.md` at the root of a repository is not a tool. It is "a README for agents" — "a dedicated, predictable place to provide the context and instructions to help AI coding agents work on your project" ([AGENTS.md](https://agents.md/), checked 2026-11-10). It is plain Markdown with no required fields, and the nearest file in the directory tree wins, so a monorepo can give each package its own. Use it for how the project is built and tested; use a skill when you are handing the agent a capability it did not have.

For tools that live behind a network call rather than a file, the other mechanism is a server the agent is given and whose tools it can call: see [Agent protocols: MCP and A2A](Agent-protocols-MCP-and-A2A.md).

## A skill is instructions the agent obeys

Because the file changes what the agent does, it is closer to installed software than to documentation. Anthropic's own warning: "a malicious Skill can direct Claude to call tools or run code in ways that don't match the Skill's stated purpose" ([Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), checked 2026-11-10). Read a skill's scripts before installing it from anywhere you do not control, and keep secrets out of the file: its text is read into the model's context.

One more limit worth knowing before you write four copies: custom skills do not sync across surfaces. A skill uploaded to one product is not automatically available on another, so the same folder may have to be installed once per place the agent runs ([Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), checked 2026-11-10).

## Related pages

- [What an AI agent is](AI-agent.md): tools, the loop, and levels of autonomy
- [Agent protocols: MCP and A2A](Agent-protocols-MCP-and-A2A.md): the network side of the same question
- [Where your keys come from](Where-your-keys-come-from.md): how to see which channel actually sent the callers

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [A2A (Agent2Agent)](Glossary.md#a2a-agent2agent), [Agent](Glossary.md#agent), [Coding agent](Glossary.md#coding-agent), [Container](Glossary.md#container), [Context window](Glossary.md#context-window), [Deploy](Glossary.md#deploy), [Dockerfile](Glossary.md#dockerfile), [MCP (Model Context Protocol)](Glossary.md#mcp-model-context-protocol), [Model](Glossary.md#model), [Secret](Glossary.md#secret), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-10.

- Anthropic, [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): what a skill is, the `SKILL.md` structure and required fields, the three loading levels, where Claude Code looks for skills, the cross-surface limit, and the security warning
- AMD, [GAIA skills README](https://github.com/amd/gaia/blob/main/hub/skills/README.md): the skill package format, the front matter fields, and `gaia skill publish`
- [AGENTS.md](https://agents.md/): what the file is for, the format and the nearest-file rule

---

First version written with AI assistance, from adding a deploy skill to an agent platform's skills directory, and checked against the [sources](#sources) on 2026-11-10. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
