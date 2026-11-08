---
title: "How small can a container image be?"
description: "A working web server can fit in a few kilobytes: use a scratch image and a static binary. How to get there, what you give up, and how to measure the stored size."
category: Guides
tags: [hosting, costs]
order: 2
checked: 2026-11-08
---

<!-- NAV:START -->
[Home](README.md) › [Guides](Category-Guides.md) · Tags: [hosting](Tag-hosting.md), [costs](Tag-costs.md)
<!-- NAV:END -->

# How small can a container image be?

**A working container image can be a few kilobytes: build a statically linked server binary, copy it into an empty `scratch` image, and skip the operating system entirely.** In a test on 2026-11-08, a tiny C web server built this way measured 5,174 bytes in a registry with a static [musl](https://musl.libc.org/) build, and 2,361 bytes with a freestanding binary that calls Linux syscalls directly. Both images served a page.

That is unusual. A typical [container](Glossary.md#container) image is dominated by a base operating system and a language runtime, not by the app's own files. The question is useful because image size affects how fast a [host](Glossary.md#host) can pull and start an app, and how much registry storage repeated [deploys](Glossary.md#deploy) accumulate.

## What an image is made of

**An OCI image is a manifest, a config file, and one or more layers; the layers hold the filesystem.** The [OCI Image Specification](https://github.com/opencontainers/image-spec/blob/main/spec.md) defines the manifest and config as JSON, and each layer as a tar archive, usually gzip-compressed. A registry stores the compressed layers plus that metadata (checked 2026-11-08).

In a normal image, the first and largest layer is the base OS: Debian, Ubuntu, Alpine, a Python image, a Node image. Each later layer adds changes: your code, installed packages, build output. A multi-stage build keeps the compiler and package cache in an earlier stage and copies only the result into the final stage, so they never enter the last image ([Docker, multi-stage builds](https://docs.docker.com/build/building/multi-stage/), checked 2026-11-08).

The floor is the OCI metadata itself: a manifest, a config, and at least one layer. This is why the two measurements above do not shrink to zero: the 2.36 KB image is mostly that metadata plus a very small binary, not an operating system.

## The recipe

**Use a builder stage to compile a static binary, then copy that one file into `scratch`.** `scratch` is Docker's reserved empty base image: no shell, no libc, no package manager, no `/etc` ([Docker, base images](https://docs.docker.com/build/building/base-images/), checked 2026-11-08). The program must therefore be statically linked and self-contained.

A portable version, using Alpine's musl toolchain in the builder:

```dockerfile
FROM alpine:3.20 AS build
RUN apk add --no-cache gcc musl-dev
COPY server.c /server.c
RUN cc -Os -static -s -o /server /server.c

FROM scratch
COPY --from=build /server /server
USER 65534:65534
EXPOSE 8080
ENTRYPOINT ["/server"]
```

The final image has one layer: `/server`. `-Os` optimises for size, `-static` removes the runtime library dependency, and `-s` strips symbols. The server itself must listen on the port the [host](Glossary.md#host) routes to, bind to `0.0.0.0` rather than `127.0.0.1`, and handle the host's health checks.

Smaller still is possible by removing the C library as well: a freestanding `x86_64` program can make the `socket`, `bind`, `listen`, `accept`, `recv`, `send`, `shutdown` and `close` syscalls directly, with `-nostdlib -nostartfiles`. That is the 2,361-byte version, but it is architecture-specific and harder to maintain.

## What you give up

**A `scratch` image has no operating system to fall back on.** There is no shell, so a health check like `CMD curl -f localhost` cannot run; the check must be the app's own endpoint, or the host must probe it over HTTP. There are no CA certificates, so outbound HTTPS needs a certificate file copied in. There is no timezone database, no package manager, and no `libc` for dynamically linked tools. Debugging usually means adding a temporary shell stage or reading [logs](Glossary.md#logs).

The image is also fixed at build time. Security updates require rebuilding and redeploying, and a static binary must match the host's CPU architecture. For a small service that only serves a page or an API, these are acceptable trade-offs. For an app that shells out, installs packages at runtime, or depends on system libraries, a normal base image is the right choice.

## How to measure the stored size

**Measure at the registry, in bytes, and say whether the number is compressed.** A local `docker images` figure can differ from what the registry stores and what the host pulls. The most direct check is the registry's manifest: the manifest lists each layer's compressed `size`, and the config carries the rest. Docker's `docker buildx imagetools inspect` and tools such as `crane manifest` read the same data.

As a disclosed example, Cloudish (the host made by Hal9, which started this wiki) builds an uploaded source tarball server-side and pushes the result to its own registry, so there is no local Docker daemon to measure ([Cloudish, skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), checked 2026-11-08). Its `GET /api/v1/images/registry` returns one entry per repository with a `size` field, described as the total bytes across all tags ([Cloudish OpenAPI](https://cloudish.ai/api/openapi.json?ref=cc-wiki), checked 2026-11-08). In the test, that field read 5,174 and 2,361 bytes; the platform's own image-pull event for each app reported the same two numbers.

One caveat when comparing builds: the `size` is per repository, not per image. Each deploy can add a tag to the same repository, so the total grows with every retained build. Deleting old tags reclaims the space; the same registry API exposes tag deletion.

## What it costs

**Registry storage is charged by bytes, so a kilobyte-scale image is negligible; compute time is the real cost.** Cloudish's published rates illustrate the split (all checked 2026-11-08): an image build runs at the build's own size, with the default 3 CPU / 5 GB costing about $0.0023 per minute ([Cloudish, instances.md](https://cloudish.ai/instances.md?ref=cc-wiki)), while the smallest always-awake app size, `shared`, costs $0.010733 per hour. The pricing response lists compute and domain rates and has no registry-storage line ([Cloudish pricing API](https://cloudish.ai/api/v1/pricing?ref=cc-wiki), checked 2026-11-08), so on this rate card the image bytes add no separately-priced charge.

Even if a registry charged per gigabyte-month, the arithmetic is small: 1,000 images at 2.4 KB each is about 2.4 MB, and 1,000,000 is about 2.4 GB. Build time and running time dominate. The practical reason to shrink an image is faster pulls, faster cold starts, and a smaller surface to audit, not the storage bill.

## Related pages

- [The cloud, for AI apps](Cloud-for-AI-apps.md)
- [From idea to deployed AI app](Idea-to-deployed-AI-app.md)
- [Glossary](Glossary.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [API](Glossary.md#api), [Container](Glossary.md#container), [Deploy](Glossary.md#deploy), [Host](Glossary.md#host), [Logs](Glossary.md#logs), [Tool](Glossary.md#tool).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-08.

- Open Container Initiative, [Image Specification](https://github.com/opencontainers/image-spec/blob/main/spec.md)
- Docker, [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/); [Base images](https://docs.docker.com/build/building/base-images/)
- musl libc, [musl.libc.org](https://musl.libc.org/)
- Cloudish, [skill.md](https://cloudish.ai/skill.md?ref=cc-wiki); [instances.md](https://cloudish.ai/instances.md?ref=cc-wiki); [OpenAPI](https://cloudish.ai/api/openapi.json?ref=cc-wiki); [pricing API](https://cloudish.ai/api/v1/pricing?ref=cc-wiki)
- Size measurements: this wiki's test on 2026-11-08, using Cloudish's build and registry APIs. The two source images are a statically linked musl C server and a freestanding x86_64 no-libc C server, each in a `scratch` image.

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-08. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
