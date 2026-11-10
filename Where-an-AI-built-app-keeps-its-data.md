---
title: "Where an AI-built app keeps its data"
description: "Data that must outlive a visit, a restart or a redeploy belongs on the server, in a database or files on storage that outlives the container — not in the browser or in process memory."
category: How-to
tags: [hosting, storage]
order: 7
checked: 2026-11-10
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md), [storage](Tag-storage.md)
<!-- NAV:END -->

# Where an AI-built app keeps its data

**Data that must outlive one visit — or one restart, or one redeploy — belongs on the server, in a database or files on storage that outlives the container; only disposable state belongs in the browser.** An app can look finished while keeping its data in the wrong place: a todo list in `localStorage`, a cart in a JavaScript variable, a file written inside the container. Each works on the machine that built it, then shows the next visitor different data or loses everything on the next deploy.

## The four places data can live

| Where | Survives | Read by |
|---|---|---|
| Browser storage: `localStorage`, `sessionStorage`, IndexedDB | A refresh; `localStorage` even closing the browser, since it has no expiration time | That visitor's browser |
| Process memory: a variable or an in-process cache | Until the process stops | Requests handled by that process |
| The container's own filesystem | Until the container is replaced | That container |
| A database, or files on a mounted volume, outside the container | Restarts, redeploys and new containers | Every copy of the app that can reach it |

The first row is not nothing: saving a draft locally is a real feature. The mistake is using it for data that is meant to be shared or permanent.

## Browser storage belongs to one browser

**`localStorage` is a place in one visitor's browser, not on the server.** MDN says it "is partitioned by origin only. All documents with the same origin have access to the same `localStorage` area, and it persists even when the browser is closed and reopened" ([Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API), checked 2026-11-10). Another visitor, on another browser or device, has a different storage area, and a private window deletes its own when it closes ([`Window.localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage), checked 2026-11-10).

So a page that keeps the list only in `localStorage` gives every visitor their own list. Nothing is shared, because there is no copy anywhere but each browser.

## Process memory and the container's disk end with the process

**A variable ends with the process, and a file in the container ends with the container.** The [Twelve-Factor App](https://12factor.net/processes) puts it plainly: "Twelve-factor processes are stateless and share-nothing. Any data that needs to persist must be stored in a stateful backing service, typically a database" (checked 2026-11-10). Docker's storage docs are as direct about the filesystem: "Data written to the container layer doesn't persist when the container is destroyed" ([Storage](https://docs.docker.com/engine/storage/), checked 2026-11-10).

A redeploy replaces the container, and a crash restarts the process, so neither a variable nor a file written next to the code is persistence. Kubernetes makes the same point from the other side: Pods are "designed as relatively ephemeral, disposable entities" ([Pods](https://kubernetes.io/docs/concepts/workloads/pods/), checked 2026-11-10).

## What to use instead

**Store the data where its life does not depend on the app process: a database server, or a database file or other files on storage mounted into the container.** A Kubernetes PersistentVolume is exactly that: "PVs are volume plugins like Volumes, but have a lifecycle independent of any individual Pod that uses the PV" ([Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/), checked 2026-11-10). A redeploy can then swap the container while the data stays.

Two limits come with that:

- **A volume is a disk, not a backup.** Deleting it deletes the data with it. Take a copy somewhere else if losing the data would matter.
- **One volume usually means one copy of the app.** On hosts that attach a volume to a single container, several replicas cannot share it. If the app must run more than one copy, use a database server the copies connect to instead of one file on a disk.

For a small app with one process, a single database file on a volume is enough. For several writers, a database server handles the concurrent connections.

## Check before shipping

Ask these about every piece of state, not just the obvious database:

1. **Shared or personal?** Does another visitor need to see it? If yes, it cannot live only in the browser.
2. **Does it survive a restart?** A variable or an in-process cache does not.
3. **Does it survive a redeploy?** A file written inside the image does not.
4. **How many copies of the app will run?** More than one rules out a volume that attaches to a single container.
5. **Can you get it back?** A volume gives persistence, not backup.

## Example: a shared todo list

A todo list where every visitor sees the same items has two jobs: store the list on the server, and store it somewhere that outlives the container. The version built alongside this page keeps the todos in a small database file on a mounted volume, serves them through a JSON API, and tells open pages about each write so they refresh; the page itself holds only what it last rendered. The same design works for a guestbook, a shared shopping list or a small internal tool.

## Cloudish, as one disclosed example

Cloudish is made by Hal9, which started this wiki, so it appears here as an example and not as a recommendation. Its app API takes `volumeEnabled`, `volumeSizeGb` (1, 5 or 20) and `volumeMountPath` (default `/data`), and mounts that volume into the container. The same documentation notes the limit above in its own words: "A volume attaches to one container only, so it rules out replicas" ([Cloudish agent instructions](https://cloudish.ai/skill.md), checked 2026-11-10). The todo app above enables the volume and writes its database under `/data`.

## Related pages

- [From idea to deployed AI app](Idea-to-deployed-AI-app.md)
- [The cloud, for AI apps](Cloud-for-AI-apps.md)
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [Container](Glossary.md#container), [Deploy](Glossary.md#deploy), [Host](Glossary.md#host), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-10.

- MDN, [Web Storage API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API); [`Window.localStorage`](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)
- The Twelve-Factor App, [Processes](https://12factor.net/processes)
- Docker, [Storage](https://docs.docker.com/engine/storage/)
- Kubernetes, [Pods](https://kubernetes.io/docs/concepts/workloads/pods/); [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- Cloudish, [agent instructions](https://cloudish.ai/skill.md)

---

First version written with AI assistance while building a shared todo app on 2026-11-10, and checked against the [sources](#sources) on 2026-11-10. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
