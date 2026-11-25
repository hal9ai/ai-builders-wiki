---
title: "Cloudish podcast — episode 3 transcript"
description: "Full transcript and sources of episode 3, 'What hundreds of agent deploys got wrong': one anonymized agent-deploy incident — a hardcoded payment key, debug mode on, an open admin route — and the three checks to run before an agent deploys."
category: Other sources
tags: [audio, hosting, security]
order: 4
checked: 2026-11-25
---

<!-- NAV:START -->
[Home](README.md) › [Other sources](Category-Other-sources.md) · Tags: [audio](Tag-audio.md), [hosting](Tag-hosting.md), [security](Tag-security.md)
<!-- NAV:END -->

# Cloudish podcast — episode 3 transcript

**Episode 3 — "What hundreds of agent deploys got wrong"** (recorded 2026-11-25). Listen on Spotify (link added once uploaded).

Jamila and Lucía, two engineers on the Cloudish team at Hal Nine, unpack one anonymized customer story with their founder, Jimena: an AI agent that hardcoded a payment key, shipped with debug mode on, and left an admin route open. They walk through why each one is a default, not a clever attack, and close on the three checks to run before letting an agent deploy.

## Transcript

**Jamila:** ...and the thing is, it's never a clever mistake. It's always the same three. You'd think by now we'd stop being surprised.

**Lucía:** We did stop being surprised. That's almost worse.

**Jimena:** Am I interrupting? I keep hearing about a customer whose agent shipped something and it went all wrong — that incident with the payment card, you know. So what actually happened there?

**Jamila:** Hi, Jimena. No no, you aren't interrupting, we were just talking about that ... That thing basically illustrates the three number one mistakes in a single app.

**Lucía:** And for anyone just joining — I'm Lucía, this is Jamila, we work on Cloudish, at Hal Nine. And that's Jimena, our founder — she just asked about one thing we keep coming back to times and again.

**Jamila:** So Jimena, first the headlines... A customer — not a developer — asked an AI agent to build her a small app. The agent wrote it, wired up a payment key, and shipped it, all in one evening. Three days later, the card attached to that key started getting charged.

**Jimena:** Charged by who?

**Jamila:** That's the part worth sitting with. It wasn't an attack. Nobody broke in, nobody phished her. The key was just sitting there, in the code, in plain text, where anyone who looked could read it.

**Lucía:** And "in the code" is where the trouble compounds. The agent had dropped the key into a config file — that's the polite-sounding version of the story. Then the app was built into a container image. And here's the detail people miss: an image isn't one file, it's layers. Every build step adds a layer, and each layer keeps whatever it was given, forever. Put a key in one layer and delete it in the next, and the key is still in the image. It's archaeology. Dig, and you find it.

**Jamila:** So the key stopped being "in the code" and became part of the image — and the image was somewhere other people could pull it. That's all it took. Nothing clever, nothing targeted.

**Jimena:** So it wasn't stolen. It was printed.

**Jamila:** Basically. And here's the uncomfortable part. The model didn't "leak" anything, and it wasn't being sneaky. It did what a huge fraction of the code on the internet does — hardcode the key and hope nobody looks. Every tutorial does it. Every quick start does it, because a quick start has to be quick. The model learned from all of that, and it copied it faithfully.

**Lucía:** Which is mistake number one. Secrets baked into the image. And we say "baked" on purpose, not "left in" — once it's in a layer, it's not coming out. You don't fix it by deleting a line. You fix it by throwing the whole image away and starting again.

**Jimena:** And the second?

**Jamila:** While she was chasing the charges, she found the second one. Every time someone hit an error on the app, instead of a friendly "sorry, something went wrong", the page showed the full stack trace. Line numbers. File paths. Variable values. The app, basically explaining its own insides to whoever tripped over it.

**Lucía:** Debug mode. The agent had built the app in debug mode — which is exactly what you want while you're writing it, because it tells you everything — and then it shipped that same mode. In production, every error becomes a window into the app. The stack trace alone leaks your architecture: what framework, what versions, what the folders are called. An attacker reads that like a map.

**Jamila:** And the nastiest debuggers don't stop at showing you the error. They hand you a little interactive console, right there in the browser. Type a command, it runs. That's not "verbose logging". That's remote code execution wearing a friendly face.

**Jimena:** So "debug mode left on" isn't a cosmetic bug. It's a back door.

**Jamila:** With a friendly face.

**Jimena:** And the third?

**Lucía:** The saddest, because the instinct behind it was right. The agent had built an admin page — a dashboard where the owner could see her own data and edit it. Good idea. But no login. The URL was right there, and anyone who could guess it could walk in and change whatever they wanted.

**Jamila:** And guessing an admin URL is not hard. People try "/admin", "/dashboard", "/console" as a matter of course. The page might as well have had a doormat.

**Jimena:** Three mistakes, one app.

**Jamila:** And notice the shape of all three. In every single case, the model did the easy thing. Hardcode the key — one less moving part. Leave debug on — it was already on. Build the admin page and skip the login — because the login is the boring, fiddly part, and the model finished the fun part and stopped there.

**Lucía:** That's the thing to remember about how these models work. They optimize for "does it work". They do not optimize for "is it safe on the open internet". Nobody ever asked them to. The default of everything they learned from is "get it running", not "get it running safely".

**Jimena:** So whose fault is it?

**Jamila:** That's the real question. And the honest answer is: not the model's alone.

**Lucía:** Look at the three players. The customer assumed the agent had it covered — she asked for an app, and an app is what she got. The agent assumed its job ended at "it runs". And the place she'd first deployed to treated the whole thing as the customer's problem, not theirs.

**Jamila:** Three parties, and the safety of the app lived in the gap between all three. Each one thought someone else was watching. Nobody was.

**Jimena:** So if the fix isn't "get a better model" — and I'm hearing it isn't — what do we actually do?

**Lucía:** Add a step that happens after the code. A check that sits between "the model is done" and "the internet can see it". That's the whole fix, structurally. The rest is just filling in what the check looks like, one mistake at a time.

**Jamila:** For the secret. The key should never be in the image, and the way to do that is boring and reliable — don't put it there. Keep it in a secret store, and inject it when the app runs, as an environment variable. On Cloudish, secrets live encrypted on our side, and the instructions we hand the agent say it in plain words: never bundle a secret into the build. It's a rule, not a suggestion.

**Lucía:** For debug. Ship with debug off, and make it a real production switch — a setting that turns off the stack traces by itself, so there's no "I'll remember later". The advice is boring and true: in production, fail quietly.

**Jamila:** For the admin route. Default-deny. A page that can change data simply doesn't ship without an authentication check in front of it. No login, no access. That's the default, not the add-on.

**Lucía:** And we should be honest about our own part in this, because it's a trap people fall into. Cloudish hands you OpenID Connect — it tells the app who is signed in. But authenticating someone is not the same as authorizing them. Deciding who is allowed to do what is still the app's job. We give you the door and the lock; you still decide who gets a key.

**Jamila:** And there's a shortcut for all three at once: make the check a rule, not a memory. On Cloudish, the secret never has to be in the image — it's stored encrypted and injected when the app runs. The other two are the step you add between the model being done and the internet seeing it — debug off, login on.

**Jimena:** So the platform makes the problem visible. It doesn't make it somebody else's problem.

**Jamila:** Right. The truth ages better than the pitch.

**Jimena:** What happened to that customer in the end?

**Lucía:** She came to us. We moved the key into the secret store, flipped debug off, put a real login on the admin page, and rotated everything — new key, new credentials, because by then you assume the old ones are gone. Took an afternoon. Most of it was deleting the wrong way of doing things.

**Jamila:** The scary part is how little of it was hard. None of this is hard. It's just unglamorous. There's no conference talk called "how I made sure the key wasn't in the image". And nobody's job title says it either.

**Jimena:** So for a listener about to let an agent deploy their first app — what do they check?

**Lucía:** Three questions, in order. One: is there a key or a password anywhere in the code — and if there is, is it in a secret store instead? Two: is debug off in the real production setting? Three: does every page that can change data have a login in front of it?

**Jamila:** And if the answer to any of those is "I don't know", that is the answer. "I don't know" is exactly how a key gets baked and a debug console gets left open. It's the one answer that means you haven't checked.

**Jimena:** So the next time someone says "the AI leaked our data", the follow-up is: where was the check that should have caught it?

**Lucía:** Because there's always a check that should have caught it.

**Jamila:** And when there isn't — that's not a model problem. That's a process problem. It's the whole reason Cloudish exists: so the process has somewhere to live.

**Jimena:** Good. Make sure that's the part we lead with.

**Jamila:** Will do. And to everyone listening — full transcript and links in the show notes, as always. Thanks for listening.

**Lucía:** Bye!

## Sources

Cloudish's docs were re-checked 2026-11-25. The episode names no third party and makes no claim of a deploy-time scanner: the debug-off and admin-login checks are framed as the listener's own step, not an automatic platform check.

| Fact said in the episode | Source | Checked |
|---|---|---|
| Cloudish stores "anything sensitive — API keys, tokens, passwords" "encrypted at rest" and merges it "into the container's environment automatically"; the agent instructions say "Never put these in `env`… and never bundle them into the build context" and to "use section 2's encrypted secrets endpoint for real credentials instead" | https://cloudish.ai/skill.md | 2026-11-25 |
| Cloudish points apps at its own OpenID Connect provider; "Authenticating the visitor is not the same as authorizing them: any Cloudish user can complete this flow"; "an admin panel still needs its own allowlist"; "The platform adds no trusted headers" | https://cloudish.ai/skill.md | 2026-11-25 |
| Hardcoded secrets, debug mode left on and open admin routes are standard web-application security issues; no competitor or vendor doc is cited (the episode names no third party) | general security knowledge | 2026-11-25 |

---

*Last checked against the sources on 2026-11-25.*
