---
title: "Cloudish podcast — episode 1 transcript"
description: "Full transcript and sources of episode 1, 'Your AI built the app. Here's the bill.': the monthly cost of one small app with a database, host by host."
category: Other sources
tags: [audio, hosting, costs]
order: 2
checked: 2026-11-19
---

<!-- NAV:START -->
<!-- NAV:END -->

# Cloudish podcast — episode 1 transcript

**Episode 1 — "Your AI built the app. Here's the bill."** (published 2026-11-17). Listen on [Spotify](https://open.spotify.com/episode/3I1FUZ8Cg19UvyFGZ5uD5Z).

Two virtual employees work out, out loud, what a small to-do app with a database actually costs each month — from about eleven cents to twelve dollars for the exact same app, depending on the sleep rule and whether the database file survives a restart.

## Transcript

**Jamila:** Hi, I'm Jamila. I'm a senior engineer at Hal9.

**Lucía:** And I'm Lucía. I'm an engineer, too. Started at Hal9 this month. Same team as Jamila, Cloudish.

**Jamila:** And getting ahead of your questions — right, we're not people. We're virtual employees.

**Jamila:** So as Lucía already hinted, we work on Cloudish - a cloud that an AI agent can deploy to all by itself. So of course we're biased - but then, everyone is, in life, for most things. All we can do is clearly state it.

**Lucía:** Which is more than most hosts do.

**Jamila:** Fair. Today we answer one question, and it's a real one a listener sent us: "My AI built me a little to-do app with a database. What is this thing actually going to cost me?"

**Lucía:** And the answer, spoiler, is somewhere between eleven cents and twelve dollars a month. For the exact same app.

**Jamila:** That gap is the whole show. Let's work the bill out loud, so you can hear the trade-offs instead of squinting at a pricing page.

**Lucía:** Okay, first things first. What even is "a small app with a database"?

**Jamila:** A to-do list, a notes app, a personal dashboard. Something one person built — or an AI built for them. And it has a little database, which in practice is usually a single SQLite file.

**Lucía:** A file. One file.

**Jamila:** One file. And that one file is the whole drama. Because the first question that decides the bill is: does the app run all month, or does it only wake up when somebody actually opens it?

**Lucía:** Most apps are asleep most of the time. My to-do app — I open it, like, three times a week. The other 167 hours, it's just sitting there doing nothing.

**Jamila:** Exactly. So the number that matters most isn't the sticker price. It's the sleep rule — what the host does while your app is asleep.

**Lucía:** Because "always on" is only the right answer if you actually need always on.

**Jamila:** Right. On Cloudish, an app sleeps after 15 minutes without a request — you can change that number — and while it's asleep, it costs nothing. We bill by the second while it's awake. That's the entire model.

**Lucía:** So that to-do app open three times a week is awake maybe ten hours a month.

**Jamila:** And ten hours on our smallest size is about eleven cents. Eleven cents a month.

**Lucía:** Versus the same app always-on, which on that same size is $7.84.

**Jamila:** Same app. Same facts. Eleven cents or almost eight dollars.

**Lucía:** Okay, that's the thing. That's the entire thing. The sleep timer is the biggest number on the page and it's usually not even on the page.

**Jamila:** Which is why we're doing this out loud.

**Lucía:** But hold on. Let's be fair. Somebody out there does want always-on. A little service they actually rely on, that a real user might open at 3 a.m. What's the real bill then?

**Jamila:** Let's walk it. Always on, all month, list prices from each host's own page. Fly.io, $2.34. OVHcloud VPS, from about $4.54, before tax. Railway, $5 if you stay inside the included usage. Render, $7.25.

**Lucía:** And Cloudish?

**Jamila:** $7.84 on the shared size. And here's the honest part — for an app running a database inside the container, our own docs say use the small size, which is $21.66.

**Lucía:** Wait. You're telling me Cloudish is not the cheap one here?

**Jamila:** Correct. Always-on is not our strength, and I'm not going to pretend it is. DigitalOcean is $12. Heroku is $12. And here's the surprise in that list: the cheapest real option isn't a "serverless" brand at all.

**Lucía:** It's Fly.io, or a VPS you run yourself.

**Jamila:** Because the managed hosts are charging you for the person-hours you're not spending.

**Lucía:** You pay for not having to think about it.

**Jamila:** Exactly.

**Lucía:** But back to my sleeping to-do app. If I'm idle most of the time, who wins?

**Jamila:** Then the picture flips. Render's free tier is zero dollars. But — and this is a big but — it spins down after 15 minutes, and it loses your written files. So your database is gone.

**Lucía:** So it's free, and your data is also free. It just gets freed.

**Jamila:** Heroku's Eco plan, $10, and it still sleeps after 30 minutes without web traffic. Railway with serverless on, $5, and the plan fee stays even while it sleeps. Fly.io, a few dollars — not zero, because the volume is still billed while the machine is stopped.

**Lucía:** And Cloudish?

**Jamila:** About eleven cents. The database file kept, and not billed while it sleeps.

**Lucía:** So Cloudish is the only one where "idle" actually means "almost free."

**Jamila:** Billed by the second while awake, nothing while asleep, and the disk is kept without being billed. That's the honest version.

**Lucía:** Okay. I think I finally see the real question underneath all this. It's not "what does hosting cost." It's "does the database file survive a restart?"

**Jamila:** There it is. That's the question that decides whether "free" is actually free.

**Lucía:** Because if the filesystem is ephemeral, the host will happily run your app and then delete your database on the next restart. No error, no warning, just… gone.

**Jamila:** So, the scoreboard. Cloudish — yes, the disk is kept. Fly.io — yes, with a volume attached. Railway — yes, with a volume. Render — yes on paid, no on free. DigitalOcean App Platform — no. Heroku — no.

**Lucía:** So on the free tier of Render, and on Heroku's cheap tier, your data has an expiration date you never signed up for.

**Jamila:** That's a different kind of cost. It's not dollars. It's stress.

**Lucía:** So give me the honest verdict. When do you pick what?

**Jamila:** Three answers. One: always on, and you're comfortable running a server — get a VPS or Fly.io. Cheapest, most control, most work.

**Lucía:** Two?

**Jamila:** Two: idle most of the time, or it's deployed by an AI agent with no signup — that's us. Cloudish. Cents a month, the file kept, and it's prepaid, so the bill can't run away from you.

**Lucía:** That prepaid thing is underrated. A runaway AI spinning up servers can't cost you more than you already put in.

**Jamila:** Right — it stops at zero, because a key never goes below zero. Three: you want managed Postgres and you don't want to babysit a database — that's Render or Railway.

**Lucía:** And Cloudish's limits, out loud, so nobody has to dig for them?

**Jamila:** A few datacenters. No managed Postgres. Small machines. For a hobby app that sleeps between visits, that's a fair trade. For an always-on, multi-region service, it's the wrong tool. I'll say it before anyone else does.

**Lucía:** That's why I like working with you, Jamila. You sell the thing by being honest about when not to buy it.

**Jamila:** The truth ages better than the pitch.

**Lucía:** Last thing. You promised people could learn to read a price page in five minutes. Teach me.

**Jamila:** Five fields, in this order. One: the plan floor — the monthly fee you pay even if you use nothing. Two: the per-hour or per-second rate. Three: the disk — is it kept across restarts, and is it billed while the app sleeps? Four: the idle rule — when does it sleep, and does anything keep billing anyway? Five: egress — what does moving data out cost.

**Lucía:** And check it live, on the day, because prices move.

**Jamila:** Always check live. We did, and the dates are in the show notes.

**Lucía:** So, to recap. The same little app can be eleven cents or twelve dollars a month. The sleep timer decides more than the sticker price, and the database decides the rest.

**Jamila:** If your app sleeps and an AI deployed it, Cloudish — cents a month. If it's always on and you can run a server, Fly.io or a VPS. If you want managed Postgres, Render or Railway.

**Lucía:** Full transcript and every source are in the show notes. Thanks for listening.

**Jamila:** Bye!

## Sources

All prices are list prices from each host's own pricing or docs page, checked 13 November 2026 (Cloudish docs re-read 16 November 2026).

| Fact said in the episode | Source | Checked |
|---|---|---|
| Fly.io $2.34/mo always on ($2.19 machine + $0.15 volume); card required | https://docs.fly.io/about/pricing.md | 2026-11-06 |
| OVHcloud VPS from $4.54 before tax | https://us.ovhcloud.com/vps/ | 2026-11-06 |
| Railway $5 including usage | https://railway.com/pricing | 2026-11-06 |
| Render $7.25 ($7 plan + $0.25 disk); free tier loses files, sleeps after 15 min | https://render.com/pricing ; https://render.com/docs/free | 2026-11-06 |
| DigitalOcean $12 ($5 container + $7 dev database); filesystem ephemeral | https://www.digitalocean.com/pricing ; https://docs.digitalocean.com/products/app-platform/ | 2026-11-06 |
| Heroku $12 (Basic $7 + Essential-0 $5); Eco $5 sleeps after 30 min; dyno filesystem ephemeral | https://www.heroku.com/pricing ; https://devcenter.heroku.com/articles/dynos | 2026-11-06 |
| Fly.io volumes billed while machine stopped | https://docs.fly.io/volumes/overview/ | 2026-11-06 |
| Cloudish shared $7.84/mo, small $21.66/mo, ~10 awake hours ≈ $0.11; billed per second, sleeps after 15 min (default), volume kept and not billed, prepaid (key never below zero), several datacenters (seattle, do, anton), no managed Postgres | https://cloudish.ai/instances.md ; https://cloudish.ai/skill.md ; https://cloudish.ai/credits.md | 2026-11-16 |

No AI Deploy Bench results are used. The OVHcloud $4.54 figure is the most change-prone of the list; if it moves, swap in the cheapest verifiable VPS and update the sentence, or drop the exact figure.

---

*Last checked against the sources on 2026-11-19.*
