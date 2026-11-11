---
title: "How to deploy your app on every push"
description: "Run the same deploy script from CI on every push to main: tests first, the key in the repository's secret store, one deploy at a time, and a check that the app answers."
category: How-to
tags: [hosting, secrets]
order: 6
checked: 2026-11-11
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md), [secrets](Tag-secrets.md)
<!-- NAV:END -->

# How to deploy your app on every push

**A push deploys your app when your Git host runs a workflow on every push to `main` that tests the code and then calls the deploy script you already run by hand — with the [API key](Glossary.md#api-key) kept in the repository's [secret](Glossary.md#secret) store, never in the repository.** The workflow is only the trigger; the [deploy](Glossary.md#deploy) script stays in the repository, so the deploy you run locally and the one CI runs are the same code.

The examples use GitHub Actions. Other Git hosts offer the same parts — a trigger, a secret store, and a job that runs commands — under other names.

## 1. Keep the deploy in a script, not in the workflow

**Put the whole deploy in one script committed next to the code, and let the workflow only call it.** Pack the build context, create or update the app, set the secrets, wait for the build and check the URL in that script. A change to how you deploy is then a reviewed diff, and a deploy that works locally runs unchanged in CI.

CI has no browser, no terminal to answer a prompt, and nobody watching, so the script has four jobs it cannot skip:

- exit non-zero when anything fails, so the job turns red instead of reporting success;
- read the key from an [environment variable](Glossary.md#environment-variable);
- print progress, and never the key;
- wait for the build to finish before it exits (step 5).

## 2. Store the key as a repository secret

**The deploy key authenticates to your host's API, so it belongs in the Git host's secret store and reaches the job as an environment variable.** On GitHub, add it with the `gh secret set` subcommand; the CLI "will prompt you to enter a secret value. Alternatively, you can read the value of the secret from a file" ([GitHub, Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets), checked 2026-11-11):

```sh
gh secret set DEPLOY_API_KEY              # prompts for the value
gh secret set DEPLOY_API_KEY < key.txt    # or reads it from a file
gh secret list                            # names and dates, never values
```

Two habits around the value itself:

- **Never print it, and do not rely on log masking.** GitHub's own guidance says "Because there are multiple ways a secret value can be transformed, automatic redaction is not guaranteed" ([GitHub, Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), checked 2026-11-11). A key echoed, split or pasted into an error message can come out unmasked; if it reaches a run log, delete the log and rotate the key.
- **Pass it as an environment variable, not as a command-line argument.** GitHub warns that "Some jobs will use secrets as command-line arguments which can be seen by another job running on the same runner" ([same page](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), checked 2026-11-11).

**A workflow triggered by a pull request from a fork does not get the secret.** GitHub states that, with the exception of `GITHUB_TOKEN`, "secrets are not passed to the runner when a workflow is triggered from a forked repository" ([GitHub, Using secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets), checked 2026-11-11). That is the behaviour you want: a stranger's pull request can run the tests but cannot deploy your app. Do not work around it by pasting the key into the workflow file.

## 3. Run the tests before the deploy step

**Put the test command in its own step above the deploy, so a broken change never reaches the deploy step.** Steps run in the order they are written: tests first, deploy last, and the deploy step is the one that carries the key.

## 4. Make the deploy call safe to repeat

**Every push runs the script, including a push that only edits the README, so the deploy call must be "create or update", not "create and fail if it exists".** A create-only call needs a lookup first, and the lookup and the create can race with another deploy.

*Disclosed example.* On Cloudish (made by Hal9, which started this wiki), `POST /api/v1/projects` "creates the project if it doesn't exist yet (or updates it if it does — same call either way, so a redeploy script can always call this unconditionally)" ([Cloudish skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), last updated 2026-11-11, checked 2026-11-11).

## 5. Wait for the build inside the job

**A deploy that builds from source returns a build that has not run yet, so the job must poll until the build ends and then check the app answers.** A script that exits when the API call returns gives a green job while the previous version is still serving.

On Cloudish, "Poll only while `status` is `"running"`: that's the only state a build in progress is in, so anything else — `"succeeded"`, `"failed"`, or a response with no status at all — is the end", and once it has succeeded "the project's docker app is already registered and its subdomain already provisioned" ([Cloudish skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), checked 2026-11-11). Other hosts use different field names for the same fact.

What to check after the build — the logs, the port, the URL — is a page of its own: [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md).

## 6. Let only one deploy run at a time

**Two pushes close together can start two deploys, and the older one can finish last, leaving the previous version live.** Give the workflow a concurrency group: "there can be at most one running job or workflow in a concurrency group at any time" ([GitHub, Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), checked 2026-11-11).

```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

With `cancel-in-progress: false`, a running deploy is never interrupted: a newer push waits as `pending`, replacing an earlier waiting one, which is what you want for a deploy. Do not set it to `true` here: a deploy cancelled halfway can leave a build that nobody polls and a configuration half applied.

## 7. Give the job only what it needs, and a manual button

**A checkout needs read access to the repository and nothing else; the deploy key does the rest.** Set that once for the whole workflow:

```yaml
permissions:
  contents: read
```

Once you list any permission this way, every permission you leave out is set to `none` ([GitHub, Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), checked 2026-11-11). GitHub calls it good practice "to set the default permission for the `GITHUB_TOKEN` to read access only for repository contents" ([GitHub, Security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), checked 2026-11-11).

Add `on: workflow_dispatch` to get a manual "Run workflow" button, for redeploying without a commit. One trap: "This trigger only receives events when the workflow file is on the default branch" ([GitHub, Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), checked 2026-11-11). The button appears only after the workflow is merged, so the merge is often the first real run.

## 8. Rotate the key, and remember who can read it

**Anyone who can push to the repository can read every secret in it**, because "Any user with write access to your repository has read access to all secrets configured in your repository" ([GitHub, Security hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), checked 2026-11-11). Give the deploy key the smallest scope the host offers, and treat it as shared with the whole team that can push.

To rotate: create a new key at the host, set it as the repository secret, run the workflow once and check the deploy, then revoke the old key. Rotation is cheap; GitHub calls it good practice "to reduce the window of time during which a compromised secret is valid" ([same page](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions), checked 2026-11-11).

## A complete workflow

```yaml
name: Deploy

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: deploy-production
  cancel-in-progress: false

jobs:
  deploy:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm test
      - name: Deploy
        env:
          DEPLOY_API_KEY: ${{ secrets.DEPLOY_API_KEY }}
        run: ./scripts/deploy.sh
```

The job timeout matters as much as the steps: without it, a build that never finishes holds a runner and a concurrency slot until the timeout GitHub applies to every job — "The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360" ([GitHub, Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax), checked 2026-11-11).

## When it goes wrong

| What you see | Usual cause |
|---|---|
| No run on push | The `branches` list does not include the branch, or the workflow file is not on the default branch |
| The job fails at the deploy step with `401` | The secret is missing, empty, or named differently from the variable in `env` |
| The job is green but the site shows the old version | The script exits when the API answers; poll the build and check the URL |
| An older version is live after two quick pushes | Two deploys ran at once; give them one concurrency group |
| The key appears in a log | Redaction is not guaranteed; delete the log and rotate the key |
| A pull request from a fork cannot deploy | Expected: fork-triggered workflows do not receive secrets |

## Related pages

- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md)
- [From idea to deployed AI app: a typical workflow](Idea-to-deployed-AI-app.md)
- [Security for AI apps and agents](Security-for-AI-apps.md)
- [The cloud, for AI apps](Cloud-for-AI-apps.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [API key](Glossary.md#api-key), [Deploy](Glossary.md#deploy), [Environment variable](Glossary.md#environment-variable), [Host](Glossary.md#host), [Logs](Glossary.md#logs), [Prompt](Glossary.md#prompt), [Secret](Glossary.md#secret), [Workflow](Glossary.md#workflow).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-11.

- GitHub, [Using secrets in GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)
- GitHub, [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- GitHub, [Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- Cloudish, [skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), last updated 2026-11-11

---

First version written with AI assistance. Last checked against the sources on 2026-11-11. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
