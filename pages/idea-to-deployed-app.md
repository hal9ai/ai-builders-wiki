---
title: "From idea to deployed AI app: a typical workflow"
description: "One concrete path, end to end: build with an assistant, keys and secrets, deploy, logs, costs, updates."
category: Guides
tags: [deploy, hosting, secrets, costs, coding-agents]
checked: 2026-10-28
---

# From idea to deployed AI app: a typical workflow

**A typical AI app goes through seven steps: scope it, build it with an assistant, keep the API key secret, test it locally, deploy it to a host, read its logs, and watch its costs, then repeat for every update.** This page walks through one concrete example. The tools are interchangeable; the steps are not.

*Disclosure: this wiki is made by Hal9, which also runs Cloudish, one of the hosts used as an example below.*

**The example:** a small web app where a team pastes meeting notes and gets back a summary with action items. A Python backend calls a model API; a single HTML page is the front end.

## 1. Scope the idea and build it with an assistant

**Write down, in a few lines, what the app does, what it must never do, and how you will know it works, before you ask an assistant to write code.** That text becomes the first prompt, and later the project's instruction file.

```text
Build a small web app:
- One page with a text box and a "Summarize" button.
- A Python (FastAPI) backend with POST /summarize that sends the text to a model API
  and returns: a 3-sentence summary and a list of action items with owners.
- The API key comes from the environment variable MODEL_API_KEY. Never put it in the page.
- Reject inputs over 20,000 characters.
- Include a Dockerfile, a requirements.txt, a .gitignore that excludes .env, and a test.
- The app listens on the port given in the PORT environment variable (default 8000).
```

Which assistant: a chat app for a first prototype, a [coding agent](ways-to-use-ai.md#coding-agents-in-the-terminal) or [IDE integration](ways-to-use-ai.md#ide-integrations-and-extensions) for anything you will maintain. Keep the project in Git from the first commit so every change the assistant makes can be reviewed and undone.

What to check in what it produced:

- **Where the model is called.** It must be the backend, not the browser. If the key appears in any file sent to the browser, stop and fix it. See [security](security.md#secrets-and-api-keys).
- **New dependencies.** Make sure each package exists and is the one you meant ([slopsquatting](security.md#supply-chain)).
- **The model ID.** Take it from the provider's models page, and put it in configuration ([how versions work](providers-and-models.md#how-model-names-and-versions-work)).

## 2. Keys and secrets

**Create one API key for this app, store it as an environment variable locally and as a secret on the host, and never commit it.** This follows the Twelve-Factor rule that an app "stores config in environment variables", and its test: the code "could be made open source at any moment, without compromising any credentials" ([The Twelve-Factor App, Config](https://12factor.net/config), checked 2026-10-28).

Locally:

```sh
# .env  (listed in .gitignore, never committed)
MODEL_API_KEY=sk-...
MODEL_ID=the-model-id-from-the-provider-page
```

```sh
echo ".env" >> .gitignore
```

Anthropic's guidance says the same and adds that you should "prefer encypted [sic] secret storage instead of dotenv files" ([Anthropic, API key best practices](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure), checked 2026-10-28). OpenAI recommends "separate projects for your staging and production environments" ([OpenAI, Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices), checked 2026-10-28), so a test key can be revoked without touching production.

On the host, set the same names in its secrets or environment settings (web dashboard, CLI or API). The app reads them the same way in both places.

If a coding agent does the deploy for you, give it a token scoped to this one app, not your account password. See [over-scoped tokens](security.md#over-scoped-tokens).

## 3. Run and test it locally

**Run the app on your machine with the real key and a few real inputs before deploying, because most deploy failures are local failures that nobody noticed.**

```sh
docker build -t meeting-notes .
docker run --env-file .env -e PORT=8000 -p 8000:8000 meeting-notes
# then open http://localhost:8000 and try 3 or 4 real meeting notes
```

Checks that save time later:

- The app reads its port from `PORT` and listens on `0.0.0.0`, not only `localhost`. Many hosts set the port for you.
- A test checks the *shape* of the answer (a summary and a list), not the exact words. Model output is not repeatable ([why](generative-ai.md#where-it-fails)).
- A very long input is rejected with a clear message, not sent to the model.

## 4. Deploy

**Pick a host that fits the app's shape, push the code or the container image, set the secrets, and open the public URL.** For this app, a request takes a few seconds and the answer can be streamed, so a container host or a serverless function with a long enough time limit both work ([which shape](cloud-for-ai-apps.md#serverless-containers-or-vms), [time limits](cloud-for-ai-apps.md#time-limits-and-streaming)).

The steps are similar everywhere:

1. Create the app on the host (dashboard, CLI or API).
2. Give it the code: connect the Git repository, upload the build context, or point to an image.
3. Set `MODEL_API_KEY` and `MODEL_ID` as secrets or environment variables.
4. Deploy, and wait for the build to finish.
5. Open the URL and run the same 3 or 4 inputs as locally.

*A disclosed example.* On Cloudish, the host run by Hal9, one API call "creates the project and starts the build", and the same call updates it later, so "a redeploy script can always call this unconditionally"; secrets are set through a separate endpoint and are "encrypted at rest, and merged into the container's environment automatically" ([Cloudish skill.md](https://cloudish.ai/skill.md), checked 2026-10-28). Other hosts use a Git push, a CLI command or a dashboard button for the same steps.

Before sharing the link more widely: add a simple sign-in or a shared password if the app should not be public, and a per-user rate limit, because every request costs model tokens.

## 5. Read the logs

**Logs are what the app prints while it runs; read them after every deploy and whenever something fails.** They answer "did it start?", "which request failed?" and "what did the model provider return?".

What to log for an AI app:

- one line per request: time, input length, model ID, tokens used, duration, success or error
- the provider's error code and message when a call fails (rate limit, invalid key, overloaded)
- **never** the API key, and think twice before logging users' full inputs: they may contain personal data ([data protection](data-protection.md))

Most hosts show logs in their dashboard and through a CLI or API. Cloudish, for example, can "Fetch the running container's own stdout/stderr on demand" and does not store logs on its side ([Cloudish skill.md](https://cloudish.ai/skill.md), checked 2026-10-28), so anything you need to keep should go to your own log store. Check your host's retention before relying on its logs for later.

Common first-deploy errors and their usual cause:

| What you see | Usual cause |
|---|---|
| Build succeeds, app never becomes ready | App listens on the wrong port or only on `localhost` |
| `401` or "invalid API key" from the provider | Secret not set on the host, or set under another name |
| `429` from the provider | Rate limit reached: add retries with back-off, or request a higher limit |
| Request cut off after a fixed time | The host's request time limit; stream the answer or move the work to a background job |

## 6. Watch costs

**An AI app has at least two bills, hosting and model usage, and you should cap both before strangers can reach the app.**

- **Model usage.** Set a spend limit at the provider. Anthropic: "Spend limits set a maximum monthly cost an organization can incur for API usage", and you can set your own below your tier's cap ([Anthropic, Rate limits](https://platform.claude.com/docs/en/api/rate-limits), checked 2026-10-28). OpenAI's page mentions hard limits that "stop affected API traffic when tracked spend reaches the limit" ([OpenAI, Rate limits](https://developers.openai.com/api/docs/guides/rate-limits), checked 2026-10-28).
- **Hosting.** Know whether you pay while the app is idle. Some hosts charge for an always-on instance; others let the app sleep and wake on the next request. Some bill against prepaid credit: Cloudish's credits are "prepaid, like a gift card" and "spend never exceeds the key's balance" ([Cloudish skill.md](https://cloudish.ai/skill.md), checked 2026-10-28). Others bill a card at the end of the month, so set a budget alert there.
- **Estimate before launch.** Tokens per request × requests per day × price, as in the [worked example](generative-ai.md#what-it-costs). Then compare with the provider's usage page after the first week.

Your logged token counts (step 5) are the cheapest early warning: a sudden jump means a loop, a bug or abuse.

## 7. Updates

**Every change goes through the same loop: change in a branch, test locally, deploy, check the logs, and keep the previous version ready to roll back.**

- **Code changes.** Ask the assistant for the change, review the diff, run the tests, then redeploy.
- **Model changes.** Changing `MODEL_ID` is a real change: run your 20 to 50 test inputs on the new model first. Plan for retirement dates; providers publish them on their deprecation pages ([retirement](providers-and-models.md#how-model-names-and-versions-work)).
- **Dependency updates.** Update regularly, read what changed, and keep a lockfile.
- **Key rotation.** Create a new key, set it on the host, redeploy, then revoke the old one.
- **Rollback.** Know how to go back: redeploy the previous image or Git commit. Try it once before you need it.

## The whole path on one screen

| Step | Do | Do not |
|---|---|---|
| 1. Scope and build | Write the spec first; use Git from the start | Accept code that calls the model from the browser |
| 2. Keys and secrets | One key per app and environment; env vars; secrets on the host | Commit `.env`; give an agent your account login |
| 3. Test locally | Real inputs; check answer shape | Deploy what you never ran |
| 4. Deploy | Match the host to the app's shape; add rate limits | Share the URL before limits are set |
| 5. Logs | One line per request with tokens and errors | Log keys or full personal data |
| 6. Costs | Spend limit at the provider; budget alert at the host | Discover the bill at month end |
| 7. Updates | Test model changes on real examples; practise rollback | Switch models silently in production |

## Related pages

- [The cloud, for AI apps](cloud-for-ai-apps.md)
- [Security](security.md)
- [Data protection](data-protection.md)
- [Ways to use AI](ways-to-use-ai.md)
- [Glossary](glossary.md)

## Sources

All checked on 2026-10-28.

- The Twelve-Factor App, [Config](https://12factor.net/config)
- Anthropic, [API key best practices](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure); [Rate limits](https://platform.claude.com/docs/en/api/rate-limits)
- OpenAI, [Production best practices](https://developers.openai.com/api/docs/guides/production-best-practices); [Rate limits](https://developers.openai.com/api/docs/guides/rate-limits)
- Cloudish, [skill.md](https://cloudish.ai/skill.md)

---

Written with AI assistance and checked against the [sources](#sources) on 2026-10-28. Found a mistake? [Open an issue](../CONTRIBUTING.md#report-a-mistake). Text licensed under [CC BY 4.0](../LICENSE).
