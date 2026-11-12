---
title: "How to run an app that keeps its own SQLite database"
description: "Run the official image as one container with a volume at the app's storage path, keep its secret keys outside the image, and finish the first-run setup once."
category: How-to
tags: [hosting, storage, secrets]
order: 13
checked: 2026-11-12
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [hosting](Tag-hosting.md), [storage](Tag-storage.md), [secrets](Tag-secrets.md)
<!-- NAV:END -->

# How to run an app that keeps its own SQLite database

**Run it as one [container](Glossary.md#container) with a persistent volume mounted at the directory the app documents for its storage, supply its secret key from outside the image, and complete the app's first-run setup once.** An app like Campfire — a self-hosted team chat — ships its own web server, background worker, Redis and database, so the [host](Glossary.md#host)'s job is to give it one writable directory that outlives the container and the configuration it cannot generate itself.

Campfire is the worked example; the same shape fits any app whose documentation says its database and uploads live in one directory. Cloudish is one host that exposes these pieces; it appears here as an example, not a recommendation.

## 1. Run one container, not a replica set

**SQLite is a file, so every copy of the app that can write it must sit on the same volume, and a block volume attaches to one container.** Cloudish's API reference says `volumeSizeGb` must be 1, 5 or 20, that `volumeMountPath` defaults to `/data`, and that "A volume can only attach to one container, so an app with one can't run replicas" ([Cloudish, skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), checked 2026-11-12).

That matches what Campfire asks for: "Campfire keeps all of its storage - the database and uploaded file attachments - inside the path `/rails/storage`" ([Campfire, Self-hosting Campfire](https://github.com/basecamp/once-campfire/blob/main/docs/self-hosting.md), checked 2026-11-12). Mount the volume at that path, not at the host's default: a volume at `/data` leaves the database inside the container and loses it on the next deploy.

## 2. Keep the instance's secrets out of the image

**Campfire needs a `SECRET_KEY_BASE` and a VAPID private/public key pair, and its docs say to reuse the same values across restarts and upgrades** ([Campfire, Self-hosting Campfire](https://github.com/basecamp/once-campfire/blob/main/docs/self-hosting.md), checked 2026-11-12). Generate them once, store them in the host's [secret](Glossary.md#secret) store, and let them reach the container as [environment variables](Glossary.md#environment-variable). Cloudish stores secrets encrypted at rest and merges them into the container environment; saving or deleting one restarts a running app, and an idle app receives the values when it next starts ([Cloudish, skill.md](https://cloudish.ai/skill.md?ref=cc-wiki), checked 2026-11-12).

A `SECRET_KEY_BASE` that changes invalidates signed session cookies, so a redeploy that regenerates it signs every user out. Keep it stable.

## 3. Pin the process counts to the container's size

**An image that sizes its worker pool from the host's CPU count can start far more processes than its container's CPU limit, and the memory limit is what gets hit.** Campfire's Puma config uses `workers ENV.fetch("WEB_CONCURRENCY") { worker_count }`, and its job-pool config is `default: <%= (Concurrent.processor_count * 0.5).ceil %>` ([config/puma.rb](https://github.com/basecamp/once-campfire/blob/main/config/puma.rb), [config/resque-pool.yml](https://github.com/basecamp/once-campfire/blob/main/config/resque-pool.yml), checked 2026-11-12). Set the web worker count explicitly, and the job-pool size too when the image reads one.

For Campfire the job pool comes from a YAML file rather than an environment variable, so the explicit value has to be in the image: a one-line wrapper Dockerfile that copies a `default: 1` config over the stock one is enough. The web server is set with `WEB_CONCURRENCY=1`.

## 4. Decide where TLS terminates

**Either the container terminates TLS (Campfire: `TLS_DOMAIN`) or a proxy in front does; Campfire's docs say to set `DISABLE_SSL=true` in the second case and publish port 80** ([Campfire, Self-hosting Campfire](https://github.com/basecamp/once-campfire/blob/main/docs/self-hosting.md), checked 2026-11-12). Whichever you pick, check the result: a redirect to the public URL should be `https`, and the session cookie should carry `Secure`.

Port numbers matter as much as TLS. Campfire's image runs Thruster, a proxy that listens on port 80 by default and forwards to Puma on `TARGET_PORT`, default 3000 ([Thruster, README](https://github.com/basecamp/thruster/blob/main/README.md), checked 2026-11-12). Tell the host port 80, not the port Puma listens on inside the container.

## 5. Finish the first-run setup once

**Many self-hosted apps create the first admin account through a web form, not an environment variable.** Campfire's docs say that when you start it for the first time, "you'll be guided through creating an admin account" ([Campfire, Self-hosting Campfire](https://github.com/basecamp/once-campfire/blob/main/docs/self-hosting.md), checked 2026-11-12). Open the site, complete the form, and note the email shown on the sign-in page: it is the admin's address, shown as the contact for anyone who forgets a password.

If a script or agent has to complete it, the form may not carry a CSRF token. Rails 8.2's `:header_only` strategy "Uses the `Sec-Fetch-Site` header sent by modern browsers" and "does not require authenticity tokens"; requests without a valid `Sec-Fetch-Site` header are rejected ([Rails, request_forgery_protection.rb](https://github.com/rails/rails/blob/main/actionpack/lib/action_controller/metal/request_forgery_protection.rb), checked 2026-11-12). Send the POST with `Sec-Fetch-Site: same-origin` and an `Origin` equal to the site's base URL, and it is treated like a browser form submit.

## 6. Check the app, not the deploy response

Wait for the build, then read the logs: the web server should say it is listening, and the job worker should say it started. The health endpoint answers when the app is up. Then sign in with the admin account: that exercises the database write path and the session cookie at once. [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md) gives the general checklist.

## Related pages

- [Where an AI-built app keeps its data](Where-an-AI-built-app-keeps-its-data.md)
- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md)
- [The cloud, for AI apps](Cloud-for-AI-apps.md)
- [How to shrink a container image](Container-image-size.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Agent](Glossary.md#agent), [API](Glossary.md#api), [Container](Glossary.md#container), [Deploy](Glossary.md#deploy), [Dockerfile](Glossary.md#dockerfile), [Environment variable](Glossary.md#environment-variable), [Host](Glossary.md#host), [Logs](Glossary.md#logs), [Secret](Glossary.md#secret), [Token](Glossary.md#token).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-12.

- Campfire, [Self-hosting Campfire](https://github.com/basecamp/once-campfire/blob/main/docs/self-hosting.md)
- Campfire, [config/puma.rb](https://github.com/basecamp/once-campfire/blob/main/config/puma.rb); [config/resque-pool.yml](https://github.com/basecamp/once-campfire/blob/main/config/resque-pool.yml)
- Thruster, [README](https://github.com/basecamp/thruster/blob/main/README.md)
- Rails, [Action Controller Request Forgery Protection](https://github.com/rails/rails/blob/main/actionpack/lib/action_controller/metal/request_forgery_protection.rb)
- Cloudish, [skill.md](https://cloudish.ai/skill.md?ref=cc-wiki)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-12. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
