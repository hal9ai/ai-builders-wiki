---
title: "Running Claude Code against another model provider"
description: "Point Claude Code at an Anthropic-compatible endpoint with three environment variables, and keep the provider key out of the agent's shell."
category: How-to
tags: [coding-agents, models, providers, security, secrets]
order: 9
checked: 2026-11-13
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [coding-agents](Tag-coding-agents.md), [models](Tag-models.md), [providers](Tag-providers.md), [security](Tag-security.md), [secrets](Tag-secrets.md)
<!-- NAV:END -->

# Running Claude Code against another model provider

**Claude Code can send its model requests to an Anthropic-compatible endpoint other than Anthropic's by setting an endpoint URL, an auth token and a model name in its environment; some model providers publish exactly such an endpoint, along with a setup page for Claude Code.** The agent loop, tools and permission prompts stay the same. What changes is which model answers, what it costs, and which fields of the request the provider understands.

## The three variables

Claude Code reads these from the environment, or from the `env` block of a settings file:

| Variable | What Claude Code does with it |
|---|---|
| `ANTHROPIC_BASE_URL` | "Override the API endpoint to route requests through a proxy or gateway" ([Claude Code environment variables](https://code.claude.com/docs/en/env-vars), checked 2026-11-13) |
| `ANTHROPIC_AUTH_TOKEN` | "Custom value for the `Authorization` header (the value you set here will be prefixed with `Bearer `)" (same page) |
| `ANTHROPIC_MODEL` | "Name of the model setting to use" (same page) |

`ANTHROPIC_API_KEY` is a different control: it is sent as an `X-Api-Key` header and takes precedence over a Claude subscription ([Claude Code environment variables](https://code.claude.com/docs/en/env-vars), checked 2026-11-13). With a non-Anthropic endpoint, the provider's own page says which of the two headers it accepts.

## A concrete provider: DeepSeek

DeepSeek publishes an Anthropic-compatible endpoint at `https://api.deepseek.com/anthropic` and a page titled "Integrate with Claude Code" ([DeepSeek, Integrate with Claude Code](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/), checked 2026-11-13). Its setup page gives these values:

```sh
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN="<your DeepSeek API key>"
export ANTHROPIC_MODEL="deepseek-flash[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-flash[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-flash[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-flash"
```

The same page says "Models starting with claude-opus are mapped to deepseek-v4-pro" and that names beginning with `claude-haiku` or `claude-sonnet` map to `deepseek-flash` ([DeepSeek, Integrate with Claude Code](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/), checked 2026-11-13). That mapping matters when a tool or a stored setting asks for a Claude model by name.

**Providers are not interchangeable at the field level.** DeepSeek's Anthropic-compatibility page lists what it supports, ignores and rejects; for example, it documents that a client tool definition should not carry `type: "custom"`, and that `anthropic-beta` and `anthropic-version` are ignored ([DeepSeek, Using the Anthropic API](https://api-docs.deepseek.com/guides/anthropic_api), checked 2026-11-13). Before relying on a feature such as prompt caching or a beta header, check the provider's compatibility page rather than assuming Anthropic's behaviour carries over.

## Running it from a program

For an app that starts Claude Code itself, print mode gives a line-oriented stream instead of a terminal UI:

```sh
claude -p "Create a file called notes.md with a haiku about rivers" \
  --output-format stream-json --verbose \
  --allowedTools Read,Write,Edit,Glob,Grep,Bash \
  --max-turns 6
```

`-p` queries "via SDK, then exit"; `--output-format` accepts `text`, `json` or `stream-json`; `--allowedTools` names "[t]ools that execute without prompting for permission"; `--max-turns` limits "[t]he number of agentic turns" in print mode ([Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference), checked 2026-11-13). `--verbose` turns on "full turn-by-turn output", which the streaming examples pair with `stream-json` (same page).

To let the agent edit and run things without a person at the keyboard, `--dangerously-skip-permissions` skips permission prompts ([Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference), checked 2026-11-13). That shift is acceptable only when the process is already fenced in: a container or sandbox that holds nothing valuable, with a workspace it cannot escape, time and output limits, and no credentials beyond the model token. See [Security for AI apps and agents](Security-for-AI-apps.md).

## Keep the provider key out of the agent's shell

**A model key exported into a coding agent's environment is reachable by every command the agent runs, so untrusted text that reaches the agent can ask it to print or send that key.** This is the same prompt-injection path described in [Security for AI apps and agents](Security-for-AI-apps.md): the agent treats what it reads as possible instructions, and a shell tool makes the environment readable.

A small proxy removes that exposure without changing Claude Code:

1. Run a proxy on your own server. It accepts a request path under `/v1/`, adds the provider's real `Authorization` header, and forwards the request to the provider's Anthropic-compatible base URL.
2. Give the sandbox `ANTHROPIC_BASE_URL` pointing at that proxy and `ANTHROPIC_AUTH_TOKEN` set to a separate, revocable token that only the proxy accepts.
3. The provider key lives in the proxy's environment. The sandbox can spend model tokens through the proxy, but it cannot read the key, and revoking the sandbox token cuts it off without rotating the provider key.

The proxy is also the place to enforce limits the provider does not: a per-user budget, a maximum request size, or an allowlist of model names. It must not forward arbitrary hosts, and it should refuse paths outside the provider's API.

## Related pages

- [Ways to use AI: chat, projects, coding agents, IDEs, APIs, SDKs](Ways-to-use-AI.md)
- [AI providers and models: who makes what, and how to choose](AI-providers-and-models.md)
- [How an agent finds a tool](How-an-agent-finds-a-tool.md)
- [Security for AI apps and agents](Security-for-AI-apps.md)
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [Coding agent](Glossary.md#coding-agent), [Container](Glossary.md#container), [Environment variable](Glossary.md#environment-variable), [Host](Glossary.md#host), [Model](Glossary.md#model), [Prompt](Glossary.md#prompt), [Provider](Glossary.md#provider), [Streaming](Glossary.md#streaming), [Token](Glossary.md#token), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-13.

- Anthropic, [Claude Code environment variables](https://code.claude.com/docs/en/env-vars)
- Anthropic, [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference)
- DeepSeek, [Integrate with Claude Code](https://api-docs.deepseek.com/quick_start/agent_integrations/claude_code/)
- DeepSeek, [Using the Anthropic API](https://api-docs.deepseek.com/guides/anthropic_api)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-13. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
