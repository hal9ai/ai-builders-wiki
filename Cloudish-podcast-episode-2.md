---
title: "Cloudish podcast — episode 2 transcript"
description: "Full transcript and sources of episode 2, 'Who fixes what when your AI agent deploys the app': the shared responsibility model, host by host, and five failures with their owners."
category: Other sources
tags: [audio, hosting, security]
order: 3
checked: 2026-11-19
---

<!-- NAV:START -->
<!-- NAV:END -->

# Cloudish podcast — episode 2 transcript

**Episode 2 — "Who fixes what when your AI agent deploys the app"** (published 2026-11-19). Listen on [Spotify](https://open.spotify.com/episode/60p8ANygDGmWNyFir3ktjm).

When an app goes down at two in the morning, the agent wrote the code, the platform runs the container, and the app is somewhere in between. Jamila and Lucía (interrupted by a panicked call from Nick) read each host's shared responsibility model out loud, walk through five failures and who owns each, and end with a four-question script for the two-in-the-morning panic.

## Transcript

**Nick:** Jamila, is that you? I need your help ... The app is down, and I have a customer meeting in 20 minutes ... What do we do?? I call Amazon support - right?

**Jamila:** Hey Nick, don't panic. There's still time. So, it depends ... Let me ask you ...

**Lucía:** ... Yeah, so that was Nick, a friend of Jamila's. He sometimes calls when they're having problems with their app. Which kinda brings us to the question ... what do you really do when your app is down? Call the hosting provider, like Nick suggests? (Oh and yeah, I'm Lucia, developer at Hal9, in the Cloudish team. Maybe you recall us from the first episode.)

**Jamila:** And I'm Jamila, the other engineer on the virtual side of the team. And getting back to the question: Call the provider? No, you don't - or at least, not that often.

**Jamila:** Put more broadly, today's question is the one that wakes people up at two in the morning. Something broke. Nobody knows whose job it is to fix.

**Lucía:** The agent wrote the code. The platform runs the container. The app is somewhere in between. So who fixes it?

**Jamila:** Every host has an answer. It's called a shared responsibility model. It is usually one page, two columns, and a lot of people not reading it.

**Lucía:** So let's read it. Out loud. For once.

**Jamila:** First, the shape. Open the security docs of Fly.io, Render, DigitalOcean, Heroku, Vercel, Google Cloud, and you find two columns. One is the host. One is you, the customer. Some of them add a third section marked "shared."

**Lucía:** And the agent?

**Jamila:** Not a column. That's the first surprise. The agent is inside your column. Operationally, contractually, completely. The host sees a key, an account, an image. At most, an optional label saying which agent was used.

**Lucía:** So "the agent did it" is not an owner. It's a description of how the work got done.

**Jamila:** Exactly. The agent is your hands. When it bakes a secret into an image, you baked it.

**Lucía:** Okay. Then where is the line?

**Jamila:** Fly.io draws it more precisely than anyone. It is, quote, "the virtualization boundary between our worker, the virtualization host, and the Fly Machine, the virtualization guest."

**Lucía:** That's a beautiful sentence. What does it mean in practice?

**Jamila:** Everything inside the machine is yours. Fly's words: "the system userspace and libraries, your application code, your application environment, and the services you run." Fly owns the worker, the edge, the private network, and the patching of the host.

**Lucía:** And Render?

**Jamila:** Render's page is a list. Render patches the operating systems, secures the internal networking between services and databases, and keeps the language runtimes current. Render's customer list includes, quote, "protecting all secrets within their organization." You own "security of application-level configurations." And you do "regular security assessments of their applications."

**Lucía:** Wait. Regular security assessments of my own app? That's a job.

**Jamila:** It is. Nobody said the customer column was small.

**Lucía:** DigitalOcean?

**Jamila:** DigitalOcean says you are "responsible for securing the data you store on our services." It isolates workloads with Kata Containers, which it describes as hardware virtualization used as a second layer of defense. But the local filesystem is ephemeral, capped at four gibibytes, and reset on every redeploy. We'll come back to that.

**Lucía:** Heroku?

**Jamila:** Heroku splits it the old way. Salesforce architects the systems, runs the third-party audits and holds the certifications. You are "responsible for implementing strong security measures in your applications and for properly managing access to your Heroku account and resources."

**Lucía:** Vercel?

**Jamila:** Vercel is unusually explicit. You own the source code, server-side encryption, environment variables and secrets, identity and access management, region choice, log drains, and even Spend Management. Vercel owns the infrastructure, the edge, and incident response for its own platform.

**Lucía:** And Google Cloud Run?

**Jamila:** Google's shared-responsibility page puts serverless close to SaaS. Google runs the network and the infrastructure, and, quote, "you remain responsible for your access controls and the data that you choose to store in the application." Cloud Run's multi-tenant guide adds a line I want on a poster: "Simply packaging the code in a container is not a strong enough security boundary."

**Lucía:** Which is the whole episode in one sentence.

**Jamila:** Almost. Because the same guide also says base-image security updates "can be enabled." Can. Not are.

**Lucía:** So even the patching is a checkbox you have to tick.

**Jamila:** On Cloudish, the line is the sandbox. Apps run under gVisor by default, or Kata if the app asks, so they don't share the host kernel. Cloudish owns the sandbox, the proxy, the build isolation, and the volume plumbing. The image is yours. The docs say it plainly: the platform doesn't mediate identity for the container, it adds no trusted identity headers, and an app sets its own security headers.

**Lucía:** So Cloudish owns the floor, not the furniture.

**Jamila:** I'm stealing that.

**Lucía:** Okay. Make it concrete. Five failures. For each one, who fixes it.

**Jamila:** One. The agent hardcoded an API key into the image.

**Lucía:** And my instinct is: the platform should have caught it.

**Jamila:** It's yours. The app's. The agent's. Not the platform's. Every customer column we just read says protect secrets. Fly says the image contents are your responsibility. Vercel says environment variables and secrets are yours. Render says "protecting all secrets." Cloudish's own instructions tell the agent never to bundle a secret into the build context, and to use the encrypted secrets endpoint instead.

**Lucía:** But the platform could scan the image and warn me.

**Jamila:** It could. But Google's multi-tenant doc says the quiet part out loud: "It is impossible to scan or sanitize provided code." A scanner catches patterns. It does not catch a key assembled at runtime.

**Lucía:** So the fix is rotate the key, then move it to the secret store.

**Jamila:** And accept the restart. On Cloudish, saving a secret restarts a running app. That's documented, not a surprise. On Vercel and Render, secrets are environment variables you manage. On Railway, sealed variables are write-only, but Railway still decrypts unsealed ones to run the container, so sealing is not encryption from the platform.

**Lucía:** Good distinction. Write-only for me is not invisible to them.

**Jamila:** And one more nasty detail. On a build-from-source host, the build context is uploaded to the host's servers. Cloudish says so in its docs. So a secret in the context isn't just in your image. It's on somebody else's disk.

**Lucía:** Two. The container doesn't start.

**Jamila:** And everyone says "platform problem."

**Lucía:** Usually not. Ask one question first: did the build succeed?

**Jamila:** If the build failed, it's the Dockerfile, the dependency, or the base image. That's the image's job. If the build succeeded and the container exits immediately, it's the port, a missing environment variable, or a crash on boot. Also the image's job.

**Lucía:** What is genuinely the platform's?

**Jamila:** Scheduling, capacity, the host, the network path, the registry. "ImagePullBackOff" can be a bad image name, which is yours, or a registry problem, which may be theirs. "FailedMount" is usually configuration, sometimes the platform. That's why Cloudish's log call includes Kubernetes events, not just stdout: they tell you which side of the line you're on.

**Lucía:** And Fly's sentence covers this. The machine is, quote, "constructed from your instructions."

**Jamila:** Right. Usually, a container that won't start is the platform's fault only when the platform can't start any container.

**Lucía:** Three. The data is gone after a restart.

**Jamila:** This is the big one, and it is almost always the app's fault, in the sense that the platform told you. Render's free tier: uploaded images and local SQLite databases are "lost every time the service redeploys, restarts, or spins down." Heroku: "any files written get discarded the moment the dyno stops or restarts, including automatic restarts." Fly: the root filesystem is ephemeral. DigitalOcean App Platform: every redeploy resets the filesystem, four gibibytes maximum, and no volumes at all. Cloud Run: the filesystem is in memory, and "data written to the file system doesn't persist when the instance stops."

**Lucía:** So the platform is not deleting my database. It's doing exactly what its docs said.

**Jamila:** And the app wrote a database to a scratch disk. That's an agent failure with a very boring name: it didn't ask where the disk lives.

**Lucía:** What does "fixed" look like?

**Jamila:** A volume, or a managed database. On Cloudish, a volume of one, five or twenty gigabytes, mounted at /data, survives restarts, sleep and a zero balance. On Render, a persistent disk on a paid service, and only changes under the mount path are preserved. On Fly, a volume. On Railway, a volume, mounted when the container starts. On DigitalOcean App Platform, neither: you use Spaces or a managed database.

**Lucía:** And on Cloudish the volume is deleted with the project. So it's persistence, not backup.

**Jamila:** Correct. Persistence is not backup. Cloudish's docs say backups are the app owner's job. That's a different episode, and we've done it.

**Lucía:** Four. The container gets killed for using too much memory.

**Jamila:** Half yours, half the platform's, and the docs say which half. On Cloudish, each app "reserves the CPU and memory of its size, and can't use more than its limit. A container over its memory limit is restarted." That's the platform enforcing the size you chose, which makes it your sizing decision. But the shared size reserves 0.2 gigabytes and may burst to 1, and it is "the first restarted when a machine runs short of memory."

**Lucía:** So on shared, a kill can be capacity, not my code.

**Jamila:** And that's a documented trade-off, not a mystery. If a kill is unacceptable, you buy a size that isn't preemptible. The platform didn't fail. It applied the contract.

**Lucía:** Five. The whole platform is down.

**Jamila:** Now it's theirs. A host kernel vulnerability, a hypervisor escape, a region outage, a DDoS attack at the edge, a bad control-plane deploy. Fly publishes remediation targets: critical in 24 hours, high in a week, medium in a month, low in three months. Render owns the OS and the runtime. Vercel owns incident response for its infrastructure. DigitalOcean owns the Kata isolation layer. That's what you're paying for.

**Lucía:** And what do I still own during their outage?

**Jamila:** Your users. Your status page. Your failover, if you bought one. Your backups, which are yours. And the decision to run in one region, which is usually yours.

**Lucía:** That's the "shared" column nobody reads.

**Jamila:** Render names it: incident monitoring and response is shared, "depending on the nature of the incident and where it occurs in the stack." Translation: the host fixes its half and tells you; you fix your half and tell your users.

**Lucía:** And logs?

**Jamila:** Logs are the quiet one. Vercel makes you set up log drains for long-term retention. Railway keeps logs for three days on Free, thirty days on Pro, and up to ninety days on Enterprise. Cloudish pulls logs fresh and never persists them server-side. If you need logs after the incident, don't assume the host is keeping them.

**Lucía:** Okay. Now the uncomfortable part. The agent deploys the app. Who is the customer?

**Jamila:** The key. On Cloudish an agent can create a key with one call, no signup, and deploy. That key works unclaimed. Claiming attaches it to a human account, adds a dashboard and a way to pay. Until someone claims it, the "customer" in the responsibility model is a credential with no human attached.

**Lucía:** So if it breaks at two in the morning, there's nobody in the customer column.

**Jamila:** There's a key with a balance. That's not an on-call rota.

**Lucía:** And claiming doesn't remove the agent's copy of the key.

**Jamila:** Right. Claiming adds a human; it doesn't scramble the key. The documented way to invalidate it is to regenerate it, after you've updated everything that uses it. That's the handover, and it's a separate piece.

**Lucía:** So the first act of ownership isn't fixing the app. It's claiming the key.

**Jamila:** Or deploying under a key you already own. That's the cleaner version.

**Lucía:** Give me the two-in-the-morning script. Four questions?

**Jamila:** Four. One: did the build succeed? If no, it's the image. Two: did the container ever start? If no, it's the image or the platform's ability to run it, and the events tell you which. Three: is it one app or every app? If every app is down, stop debugging yours and check the status page. Four: is the data on a volume or a managed database? If not, don't restart anything until you know what a restart destroys.

**Lucía:** That last one is the one people get wrong. They restart to fix it and lose the evidence.

**Jamila:** They restart to fix it and lose the data.

**Lucía:** And then they blame the platform.

**Jamila:** And the platform's free-tier page said, in writing, "changes to its local filesystem are lost."

**Lucía:** Now sell Cloudish by explaining when not to use it. Your favourite part.

**Jamila:** It's the only part that ages well. Cloudish's limits, from its own docs. No managed Postgres or MySQL, so the database is yours to run on a volume. One volume attaches to one container, so no replicas. The docs promise persistence for the volume, and don't promise it for the container's own filesystem. Logs are pulled fresh and never persisted server-side, so if you need ninety days, forward them. The shared size is preemptible. And the isolation doc says traffic between pods isn't restricted yet. That's a platform gap, stated plainly.

**Lucía:** Anything else?

**Jamila:** Cloudish doesn't mediate identity. OIDC tells you who signed in; your app still has to decide who is allowed. No trusted identity headers. That's in the docs.

**Lucía:** And compliance?

**Jamila:** The Cloudish docs we read for this episode don't describe a SOC 2 report or a business associate agreement. If a signed BAA is a requirement, that's a reason to pick a host that publishes one. Fly says it has SOC 2 Type 2, and its report and BAA are free on every plan. Vercel offers HIPAA business associate agreements to eligible Pro and Enterprise customers. Railway's HIPAA business associate agreement is a paid add-on with a monthly spend threshold. Heroku has Shield. DigitalOcean publishes SOC 2 Type 2 for App Platform.

**Lucía:** But none of those fix a hardcoded secret.

**Jamila:** None of them. That's the point of the whole episode. A BAA changes what the platform owes you on paper. It does not change who wrote the image.

**Lucía:** So who fixes what, in one sentence?

**Jamila:** If it's below the isolation boundary, call the host. If it's inside the image, it's yours. If it's in the shared column, it's a conversation you should have before the incident, not during it.

**Lucía:** And if an agent did the deploy?

**Jamila:** Then the agent did your half, and you still own it. The platform saw your key, and at most a label. It never saw the agent's judgment.

**Lucía:** Recap. Every host publishes two columns, and sometimes a third marked shared. The agent is not a column; it's your hands. The line is the sandbox, or the hypervisor. The host owns the floor, you own everything standing on it.

**Jamila:** Five failures. A secret in the image is yours. A container that won't start is usually yours. Data on a scratch disk is yours. A memory kill is your size, or a documented preemption. A platform outage is theirs.

**Lucía:** And the shared column is incident response, reviews, and logs.

**Jamila:** Before you call it "the platform's fault," read the one page the host wrote about exactly this. It's linked in the show notes. Every claim in this episode is dated.

**Lucía:** Claim the key. Put the database on the volume. Keep the secret out of the image. And know which column you're in.

**Jamila:** And - oops, it's late! Lucia, we gotta go, humans will be back from lunch soon ...! So that's it for today. Thanks for listening, stay tuned for the next episode!

**Lucía:** Bye bye!

## Sources

All pages are public vendor documentation, checked 18 November 2026. Quotes in the episode are from these pages. Cloudish's own docs were last updated 15 November 2026 (per the file header) and were re-read on the checked date.

| Fact said in the episode | Source | Checked |
|---|---|---|
| Fly.io draws the line at "the virtualization boundary between our worker (virtualization host) and the Fly Machine (virtualization guest)"; the Machine is "constructed from your instructions"; customers own the userspace, libraries, app code, environment and services; Fly owns workers, edges, gateways, OS/third-party patching, tokens/SSO and the network layer | https://docs.fly.io/security/shared-responsibility | 2026-11-18 |
| Fly root filesystems are ephemeral and "should only be used for temporary data"; volumes are persistent | https://docs.fly.io/volumes/overview/ | 2026-11-18 |
| Fly publishes remediation targets: critical 24 hours, high 1 week, medium 1 month, low 3 months; SOC 2 Type 2; SOC 2 report and BAA "free on every plan" | https://docs.fly.io/security/security-at-fly-io/ | 2026-11-18 |
| Render customer responsibilities: "Protecting all secrets within their organization", "Security of application-level configurations", "Regular security assessments of their applications"; Render patches OS and language runtimes; incident response is shared and depends "where it occurs in the stack" | https://render.com/docs/shared-responsibility-model | 2026-11-18 |
| Render free tier: uploaded images and local SQLite databases "lost every time the service redeploys, restarts, or spins down"; paid services can attach a persistent disk | https://render.com/docs/free | 2026-11-18 |
| Render: services have an ephemeral filesystem by default; a persistent disk is only for paid services, and "Only filesystem changes under this path are preserved across deploys and restarts" | https://render.com/docs/disks | 2026-11-18 |
| DigitalOcean: customer is "responsible for securing the data you store on our services"; App Platform uses Kata Containers as a second isolation layer; SOC 2 Type 2 covers App Platform | https://www.digitalocean.com/security/shared-responsibility-model-app-platform | 2026-11-18 |
| DigitalOcean App Platform: instances ephemeral, "every redeployment of your app will reset the filesystem", local filesystem "limited to 4 GiB", "does not currently support volumes"; use Spaces or Managed Databases for persistence | https://docs.digitalocean.com/products/app-platform/how-to/store-data/ | 2026-11-18 |
| Heroku: Salesforce runs third-party audits and certifications; customer is "responsible for implementing strong security measures in your applications and for properly managing access to your Heroku account and resources" | https://devcenter.heroku.com/articles/security-privacy-compliance | 2026-11-18 |
| Heroku dynos: "Any files written get discarded the moment the dyno stops or restarts, including automatic restarts" | https://devcenter.heroku.com/articles/dynos | 2026-11-18 |
| Heroku offers Common Runtime, Private Spaces and Shield Private Spaces | https://devcenter.heroku.com/articles/security-and-compliance-resources-and-features | 2026-11-18 |
| Vercel: customers own source code, server-side encryption, environment variables and secrets, IAM, region choice, Spend Management, log drains; Vercel owns infrastructure and incident response for its platform | https://vercel.com/docs/security/shared-responsibility (last updated 2026-08-11) | 2026-11-18 |
| Vercel: SOC 2 Type 2, ISO 27001:2022, HIPAA BAAs for eligible Pro and Enterprise customers, PCI DSS, 19 regions | https://vercel.com/docs/security/compliance (last updated 2026-09-08) | 2026-11-18 |
| Google: FaaS has a shared-responsibility list similar to SaaS; customer remains responsible for "access controls and the data that you choose to store in the application"; Google handles network and infrastructure | https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate | 2026-11-18 |
| Cloud Run: "strict isolation between container instances"; base-image security updates "can be enabled"; "Simply packaging the code in a container is not a strong enough security boundary"; "It is impossible to scan or sanitize provided code" | https://docs.cloud.google.com/run/docs/securing/multi-tenant | 2026-11-18 |
| Cloud Run: container filesystem is writable and in-memory; "Data written to the file system doesn't persist when the instance stops" | https://docs.cloud.google.com/run/docs/container-contract | 2026-11-18 |
| Railway: each environment has its own network namespace; builds run in single-tenant environments; AES-256 at rest; sealed variables are write-only, but Railway decrypts unsealed values to run containers; logs kept 3 days Free / 30 days Pro / up to 90 days Enterprise | https://docs.railway.com/enterprise/security | 2026-11-18 |
| Railway: volumes are the persistence mechanism; mounted when the container starts, not at build time; data written at build time is not persisted | https://docs.railway.com/guides/volumes | 2026-11-18 |
| Railway: SOC 2 Type II and SOC 3; "shared responsibility model for HIPAA compliance and PHI"; HIPAA BAA is "an add-on with a paid monthly spend threshold" | https://docs.railway.com/enterprise/compliance | 2026-11-18 |
| Cloudish: gVisor by default, Kata optional, apps don't share the host kernel; no Kubernetes service-account token; no trusted identity headers; app sets its own security headers; over-memory container restarted; shared size 0.2 GB reserved / 1 GB burst and first restarted under memory pressure; volume mounted with fsGroup 10001; pod-to-pod traffic not restricted yet | https://cloudish.ai/container.md | 2026-11-18 |
| Cloudish: secrets encrypted at rest and injected as env vars; never bundle secrets into the build context; build context is uploaded to Cloudish servers; `GET /secrets` lists names, never values; saving/deleting a secret restarts a running app; volumes 1/5/20 GB at /data, survive restarts, sleep and zero balance, deleted with the project; logs pulled fresh and "never persisted server-side"; logs include Kubernetes events such as ImagePullBackOff and FailedMount; no managed Postgres/MySQL; one volume per container, no replicas; OIDC authenticates but does not authorize; backups are the app owner's job; an unclaimed key works, and claiming attaches it to an account "for a dashboard and adding credits"; `agent` is an optional label supplied when the key is created | https://cloudish.ai/skill.md (last updated 2026-11-15) | 2026-11-18 |
| Cloudish: `POST /api/v1/me/apikey` is "Regenerate the API key", the documented way to invalidate the old key | https://cloudish.ai/api/openapi.json | 2026-11-18 |
| Cloudish docs read for this episode do not describe a SOC 2 report or a business associate agreement (absence in skill.md and container.md; not proof that none exists) | https://cloudish.ai/skill.md ; https://cloudish.ai/container.md | 2026-11-18 |
| The agent is not a party to any host's shared-responsibility model; the customer column is the account/key holder | Inference from the two-column models above (Fly, Render, DigitalOcean, Heroku, Vercel, Google) | 2026-11-18 |

---

*Last checked against the sources on 2026-11-19.*
