---
title: "How to serve a web app and its API from one Node process"
description: "Node's standard library can serve the page, answer JSON routes and open a SQLite database, with no framework and no npm install: the shape to copy and the limits that come with it."
category: How-to
tags: [hosting, storage]
order: 16
checked: 2026-11-27
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md), [storage](Tag-storage.md)
<!-- NAV:END -->

# How to serve a web app and its API from one Node process

**A small web app can go online as one Node process that serves its own files, answers its JSON routes and opens a SQLite database, using only modules built into Node — no framework and no `npm install`.** That keeps the build small and the dependency list empty, at the cost of writing the routing, static-file and database code yourself. This page shows the shape and the parts that need care; the storage details are in [How to run an app that keeps its own SQLite database](How-to-run-an-app-that-keeps-its-own-SQLite-database.md).

## 1. Three built-in modules do most of the work

**`node:http` runs the server, `node:fs` reads files from disk, and `node:sqlite` opens the database in the same process.** Node describes `node:http` as containing "both a client and server" and notes that its interfaces "never buffer entire requests or responses", so you can stream a request body instead of holding it all in memory ([Node.js, `node:http`](https://nodejs.org/api/http.html), checked 2026-11-27).

The database module is newer. In Node 24 it is a release candidate, not a stable API, and the class that opens a database is `DatabaseSync`; the docs say all of its APIs "execute synchronously" ([Node.js 24, `node:sqlite`](https://nodejs.org/docs/latest-v24.x/api/sqlite.html), checked 2026-11-27). It has been available without the `--experimental-sqlite` flag since Node 23.4.0 and 22.13.0, and the module is only importable with the `node:` prefix. Pin the Node major version in the image, because a release-candidate API can change; check the docs for the version you pin.

A minimal server that serves a health route and a folder of files looks like this:

```js
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { DatabaseSync } from "node:sqlite";

const publicDir = path.resolve("public");
const dataDir = path.resolve(process.env.DATA_DIR ?? "./data");
fs.mkdirSync(dataDir, { recursive: true });
const db = new DatabaseSync(path.join(dataDir, "app.sqlite"));

const server = http.createServer((req, res) => {
  const url = new URL(req.url ?? "/", "http://localhost");

  if (url.pathname === "/api/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ ok: true }));
    return;
  }

  // Your JSON routes go here. Read the request body, validate it, and query db.

  const relative = decodeURIComponent(url.pathname).replace(/^\/+/, "") || "index.html";
  const file = path.resolve(publicDir, relative);
  if (file !== publicDir && !file.startsWith(publicDir + path.sep)) {
    res.writeHead(403).end("Forbidden");
    return;
  }

  try {
    const body = fs.readFileSync(file);
    res.writeHead(200, { "content-type": mimeType(file) });
    res.end(body);
  } catch {
    res.writeHead(404).end("Not found");
  }
});

server.listen(Number(process.env.PORT ?? 8080), "0.0.0.0");
```

The prefix check on `file` matters: a URL path is user input, and `path.resolve(publicDir, "../../.env")` would otherwise read a file outside the folder you meant to serve ([Node.js, `node:path`](https://nodejs.org/api/path.html), checked 2026-11-27). Also reject path segments starting with a dot, and serve only file types you expect.

## 2. Keep the database on storage that outlives the container

**The database is a file, so it belongs in a directory the host keeps across restarts and redeploys, not in the container's own filesystem.** In the example, `DATA_DIR` is where the app writes `app.sqlite`; on a host with persistent volumes, mount that directory at `/data`. If the container is replaced and `/data` was not on a volume, the votes, accounts or notes are gone.

That is the whole storage setup for a small app: one process, one SQLite file, one volume. The trade-off is that a volume and a SQLite file fit one writer, so do not plan to run several replicas of the process against the same file. The [SQLite database page](How-to-run-an-app-that-keeps-its-own-SQLite-database.md) covers mounting, permissions and first-run setup in more detail.

## 3. Ship a pinned Node image with no install step

**A dependency-free app still needs a [container](Glossary.md#container) and a [Dockerfile](Glossary.md#dockerfile), but the image only has to copy the app and start Node.** There is no package install layer because there are no packages. A Dockerfile in this shape is enough:

```dockerfile
FROM node:24-bookworm-slim
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=8080
ENV DATA_DIR=/data
COPY package.json ./
COPY server ./server
COPY public ./public
RUN mkdir -p /data
EXPOSE 8080
CMD ["node", "server/index.js"]
```

`COPY` copies files from the build context, `EXPOSE` documents the port, and `CMD` is the process that starts when the container runs ([Docker, Dockerfile reference](https://docs.docker.com/reference/dockerfile/), checked 2026-11-27). The `node:24-bookworm-slim` tag is the official Node image on Docker Hub ([Docker Hub, `node`](https://hub.docker.com/_/node), checked 2026-11-27); replace the major version when you deliberately move to a newer Node.

Keep the build context to the files the image needs. A `.env` file, `.git`, a local `data/` directory and `node_modules/` should not be uploaded; explicit `COPY` lines and an archive exclude list are easier to audit than hoping a dry run catches everything.

## 4. Know what you are giving up

**You are trading a framework's ready-made routing, middleware and ORM for a small image and a short list of things that can break.** The costs are real:

- you write URL parsing, method checks, body limits and error responses yourself;
- `node:sqlite` calls are synchronous, so a slow query blocks every other request in the process; keep queries small and never scan a large table on a user request;
- a release-candidate module can change between Node versions, so pin the version and read the release notes before upgrading;
- one process with a local SQLite file is not a horizontally scaled service.

For a group board, a small internal tool or a prototype, those costs are often lower than adding a framework and a separate database. For a public app with many concurrent writers, use a server database and a framework built for it.

## 5. Check the result, not the deploy response

**A successful build only means the image exists; check that the process listened on the port, that `/api/health` answers, and that the database survives a redeploy.** Read the container logs for the listening line, open the health route, then write one row, redeploy, and read it back. [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md) has the general checklist.

## Related pages

- [How to run an app that keeps its own SQLite database](How-to-run-an-app-that-keeps-its-own-SQLite-database.md)
- [How to serve a single-page app from one container](Serving-a-single-page-app-from-one-container.md)
- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md)
- [Where an AI-built app keeps its data](Where-an-AI-built-app-keeps-its-data.md)
- [How to shrink a container image](Container-image-size.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Container](Glossary.md#container), [Deploy](Glossary.md#deploy), [Dockerfile](Glossary.md#dockerfile), [Host](Glossary.md#host), [Logs](Glossary.md#logs), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-27.

- Node.js, [`node:http`](https://nodejs.org/api/http.html)
- Node.js 24, [`node:sqlite`](https://nodejs.org/docs/latest-v24.x/api/sqlite.html)
- Node.js, [`node:path`](https://nodejs.org/api/path.html)
- Docker, [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- Docker Hub, [`node`](https://hub.docker.com/_/node)

---

First version written with AI assistance, out of a session that built and deployed a small Node and SQLite app, and checked against the [sources](#sources) on 2026-11-27. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
