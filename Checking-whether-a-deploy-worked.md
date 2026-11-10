---
title: "How to tell whether a deploy actually worked"
description: "The deploy call returning is not the app running: wait for the build, check the port and read the logs before you believe it."
category: How-to
tags: [hosting]
order: 5
checked: 2026-11-09
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md)
<!-- NAV:END -->

# How to tell whether a deploy actually worked

**A [deploy](Glossary.md#deploy) has worked when the running app answers, not when the deploy call returns.** Most deploy APIs answer as soon as they accept the work: deploying a prebuilt [container](Glossary.md#container) image returns a registered app that may still fail to start, and deploying source returns a build that has not run yet. Check in this order: the build reached success, the app's [logs](Glossary.md#logs) show it started and is listening, and the URL answers when you can reach it.

The steps below name no host in particular. Section 6 shows how they map onto one.

## 1. Wait for the build to reach a terminal state

**A source deploy is finished when its build leaves the "running" state — every other value, and a response with no status at all, is the end.** A build API in progress usually reports `status: "running"`; a finished one reports success or failure. Do not treat "the build has not failed yet" as success, and do not keep polling a build that has already stopped.

While it runs, print only the log lines you have not shown before: in the APIs that return a growing log tail, the same lines come back on every poll, and repeating them buries the line that matters.

## 2. Read the failure before you change the Dockerfile

**A build that dies with `Job has reached the specified backoff limit` and nothing else has usually hit a resource limit, not a mistake in the Dockerfile.** That message comes from Kubernetes: a Job retries failed Pods with an exponential back-off, and once the number of retries reaches `.spec.backoffLimit` — 6 by default — "the Job will be marked as failed and any running Pods will be terminated" ([Kubernetes, Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/), checked 2026-11-09).

Memory is the usual limit. A container that allocates more than its memory limit "becomes a candidate for termination", and if it keeps consuming, it "is terminated"; the pod then shows `OOMKilled` ([Kubernetes, Assign Memory Resources](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/), checked 2026-11-09). A compile that needs more memory than the builder gives it therefore fails the same way every retry, with no useful Dockerfile error.

Before rewriting the Dockerfile, retry the build with more build memory and CPU if the host lets you choose them. If it fails the same way at the larger size, it is probably the Dockerfile — read the end of the build log, which names the layer or the command that failed.

## 3. Check the port the app actually listens on

**The port you give the host must be the one the process listens on, which is not necessarily the one the Dockerfile's `EXPOSE` names.** `EXPOSE` "informs Docker that the container listens on the specified network ports at runtime" but "doesn't actually publish the port", and it "functions as a type of documentation" ([Docker, Dockerfile reference](https://docs.docker.com/reference/dockerfile/#expose), checked 2026-11-09). A host that routes traffic to its own chosen port will not follow it for you.

Two cases catch people out:

- an image whose server listens on 80 because that is nginx's default, deployed with the host's default of 8080;
- an app that binds to `127.0.0.1` inside the container instead of `0.0.0.0`, so nothing outside the container can reach it even on the right port.

Both look the same from outside: a build that succeeded and an app that never answers, usually with a `502` or `503`.

## 4. Read the running app's logs

**The container's own output is what says whether the process started, and it often names the problem itself.** Look for the line where the server says it is listening, then for the first error above it. Connection-refused errors on a database or a model API usually mean a secret or an environment variable is missing under the name the app expects.

Logs that come from the running container's stdout and stderr may not be kept by the host, so read them before the next deploy replaces them. That same view often includes the previous attempt and the platform's own events — an image that will not pull, a volume that will not mount — which is the only explanation you get when the container died before writing a single line.

## 5. Try the URL, in the right spirit

**Open the app's public URL and run the same few inputs you ran locally; if you cannot reach it, say that, rather than calling the deploy a failure.** Some environments can reach the host's API but not the app's own domain, so a page that does not load from your machine is not by itself evidence that the app is down. Fall back on status and logs, and ask someone on a different network to try.

## 6. A disclosed example: Cloudish

*Cloudish is made by Hal9, which started this wiki.* Its API shows the shape above in one place. A source deploy returns `{"project": …, "build": {"id": …, "status": "running"}}`, and the build endpoint returns `{"build": {"status", "logs"}, "image"}`; you "poll only while `status` is `"running"`", since `"succeeded"`, `"failed"`, or a response with no status at all is the end ([Cloudish, skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), last updated 2026-11-07, checked 2026-11-09).

The same document says the `port` field "must be the port your server listens on, whatever the Dockerfile's `EXPOSE` says", and that a wrong port answers `503` with "nothing accepts connections on port …"; that the build's own resources are distinct from the container's and can be raised when a build dies at the backoff limit; and that the logs endpoint pulls the container's stdout/stderr fresh on every call, "never persisted server-side", along with recent Kubernetes events. It also states the URL caveat: an environment that reaches cloudish.ai but not the app's domain is not seeing a failure.

Other hosts use different endpoints and field names for the same three facts: a build that ended, a process that is listening, and a URL that answers.

## Checklist

| Question | Evidence that answers it | What it does not tell you |
|---|---|---|
| Did the build finish? | Build status left "running" and reports success | That the app starts |
| Did the process start? | A log line saying it is listening | That its port is the one the host routes to |
| Is it reachable? | The URL answers with your own inputs | That it is reachable from every network |
| Is it healthy? | Logs after a real request, no errors above it | That it will stay healthy under load |

## When an agent does the deploy

**An agent that deploys should report success only after these checks, because the deploy call's answer is the easiest thing to mistake for a result.** The instruction to the agent is one sentence: do not say a deploy succeeded until the build reached success, the logs show the app started and is listening, and the URL was tried where it can be tried. An agent that stops at the create response reports a failure as a success, and the next person to look has to start from the build log anyway.

**Check the field names against a live response, not against your own wrapper.** A test with the HTTP layer stubbed proves the request your client builds; it cannot prove the service returns the fields your instructions tell the agent to read. A wrapper written from an API reference can pass every test and still send an agent looking for a top-level `url` where the service nests it under `project.subdomain`. Make one real call with a throwaway key, read the JSON that came back, and fix the instructions to match it. Then delete the test app so it is not billed.

## Related pages

- [From idea to deployed AI app: a typical workflow](Idea-to-deployed-AI-app.md)
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md)
- [How to shrink a container image](Container-image-size.md)
- [The cloud, for AI apps](Cloud-for-AI-apps.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [Container](Glossary.md#container), [Deploy](Glossary.md#deploy), [Dockerfile](Glossary.md#dockerfile), [Environment variable](Glossary.md#environment-variable), [Host](Glossary.md#host), [Logs](Glossary.md#logs), [Model](Glossary.md#model), [Secret](Glossary.md#secret).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-09.

- Docker, [Dockerfile reference: EXPOSE](https://docs.docker.com/reference/dockerfile/#expose)
- Kubernetes, [Jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/); [Assign Memory Resources to Containers and Pods](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/)
- Cloudish, [skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), last updated 2026-11-07

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-09. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
