---
title: "How to serve a single-page app from one container"
description: "One HTML file plus its assets in an nginx image, with no build step: hash routes need no rewrite rule, path routes need one, and the build context must not carry your secrets."
category: How-to
tags: [hosting]
order: 14
checked: 2026-11-14
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md)
<!-- NAV:END -->

# How to serve a single-page app from one container

**A single-page app goes online as a folder of static files behind a web server: one `index.html`, its CSS, JavaScript and images, copied into the official nginx [container](Glossary.md#container) image, with no build step and no framework.** The page keeps its views in the browser and calls the [API](Glossary.md#api) from JavaScript, so the server only has to hand over files. Two things go wrong in this setup: a view address the server cannot find, and a build context that carries files the page never uses.

## 1. Hash routes never reach the server

**A view written after `#` is not part of the address the browser requests, so every view is the same request for `/` and the server needs no rule at all.** The [fragment](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment) "is not sent to the server when the URI is requested; it is processed by the client (e.g., the browser) after the resource is retrieved" ([MDN, Fragment](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment), checked 2026-11-14).

That is why so many demos use routes like `/#profile/amara` or `/#cameras`. The request is for `/`, nginx answers with `index.html` from its default document root, and the page's own JavaScript reads `location.hash` and draws the matching view. Refresh, a bookmark and a link pasted into a chat all work, because they all fetch the same file.

## 2. Path routes need one fallback rule

**A view in the path, such as `/profile/amara`, is a request for a file that does not exist, so a plain file server answers `404` until you tell it to answer with `index.html` instead.** In nginx that is one `try_files` line inside `location /`: when the named file is not there, "an internal redirect to the _uri_ specified in the last parameter is made" ([nginx, `ngx_http_core_module`](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files), checked 2026-11-14).

```nginx
location / {
  try_files $uri /index.html;
}
```

Use one style and stay with it. Mixing hash links with path links gives a page whose deep links work on one host and `404` on another.

## 3. Copy only the files the page serves

**The build context of a [deploy](Glossary.md#deploy) is everything the build can see, so a `.env` file sitting next to `index.html` is uploaded with it unless you exclude it.** Docker defines the context as "the set of files that your build can access", and says entries in a `.dockerignore` file are "removed from the build context before it's sent to the builder" ([Docker, Build context](https://docs.docker.com/build/building/context/), checked 2026-11-14).

Two habits make this hard to get wrong:

- list the files to copy in the Dockerfile (`COPY index.html styles.css app.js …`) and copy a folder of assets, rather than `COPY . .`;
- when you hand the host a tarball instead of a folder, build it from that same list, or pass the excludes explicitly.

A demo page often lives next to the `.env` that generated its images, so this is the common case, not the paranoid one.

## 4. Give the host the port nginx listens on

**The port you give the [host](Glossary.md#host) must be the one the server inside the container listens on, which for the official nginx image is 80.** The image's own documentation shows it publishing `-p 8080:80` and copying content to `/usr/share/nginx/html` ([Docker Hub, nginx](https://hub.docker.com/_/nginx), checked 2026-11-14); `EXPOSE 80` in a Dockerfile documents the port but does not choose the one the host routes to ([Docker, Dockerfile reference](https://docs.docker.com/reference/dockerfile/#expose), checked 2026-11-14). A host that assumes 8080 for an nginx container that listens on 80 gets no answer back — the check in [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md) covers the rest.

## A minimal Dockerfile

This is the shape used by a one-page demo built as `index.html`, `styles.css`, `app.js` and an `assets/` folder:

```dockerfile
FROM nginx:1.27-alpine

COPY index.html styles.css app.js /usr/share/nginx/html/
COPY assets /usr/share/nginx/html/assets

EXPOSE 80
```

That is the whole build. Adding a custom `nginx.conf` is optional and only needed for things like the `try_files` rule above, gzip, or cache headers; serve the HTML with a short cache and the assets with a long one, as [Stale cache after a deploy](Stale-cache-after-a-deploy.md) explains.

## A disclosed example: Cloudish

*Cloudish is made by Hal9, which started this wiki.* Its server-side build takes a tar.gz context that "must contain a `Dockerfile` at its root", accepts a `port` field which "must be the port your server listens on" — "an nginx image listens on `80`, so send `port=80` for one" — and answers `503` when the port is wrong. Its example context command excludes the risky files up front: `tar --exclude='.env*' --exclude='.git' -czf context.tar.gz .` ([Cloudish, skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), checked 2026-11-14).

Other hosts take the same pieces in different words: a folder or archive, a Dockerfile, and a port.

## Checklist

| Question | What to do | What it does not fix |
|---|---|---|
| Do deep links work? | Hash routes, or a `try_files` fallback to `index.html` | A view that needs data the page cannot fetch |
| Is anything secret in the image? | Explicit `COPY` lines, `.dockerignore`, excludes on the archive | Secrets the page itself embeds in its JavaScript |
| Which port? | The one the server listens on (80 for nginx) | A process that died before listening |
| Will a redeploy show? | Short cache on HTML, long cache on assets with changed names | A browser that kept the old HTML |

## Related pages

- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md)
- [Why a deploy looks broken in one browser but fine in another](Stale-cache-after-a-deploy.md)
- [How to shrink a container image](Container-image-size.md)
- [From idea to deployed AI app: a typical workflow](Idea-to-deployed-AI-app.md)
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Container](Glossary.md#container), [Deploy](Glossary.md#deploy), [Dockerfile](Glossary.md#dockerfile), [Host](Glossary.md#host), [Secret](Glossary.md#secret).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-14.

- MDN, [URI fragment](https://developer.mozilla.org/en-US/docs/Web/URI/Reference/Fragment)
- nginx, [`ngx_http_core_module`: `try_files`](https://nginx.org/en/docs/http/ngx_http_core_module.html#try_files)
- Docker, [Build context](https://docs.docker.com/build/building/context/); [Dockerfile reference: `EXPOSE`](https://docs.docker.com/reference/dockerfile/#expose)
- Docker Hub, [nginx](https://hub.docker.com/_/nginx)
- Cloudish, [skill.md](https://cloudish.ai/skill.md)

---

First version written with AI assistance, out of a session that built and deployed a one-page demo, and checked against the [sources](#sources) on 2026-11-14. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
