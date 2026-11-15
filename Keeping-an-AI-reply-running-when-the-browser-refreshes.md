---
title: "How to keep an AI reply running when the browser refreshes"
description: "Make the server own the turn, buffer its events and let a reloaded page reattach — instead of tying the model call to one HTTP response."
category: How-to
tags: [hosting, basics]
order: 14
checked: 2026-11-15
---

<!-- NAV:START -->
<!-- NAV:END -->

# How to keep an AI reply running when the browser refreshes

**Keep the turn on the server and let the browser reattach; the HTTP response must not be the thing that owns the work.** A chat reply streams for seconds or minutes, and the socket carrying it disappears whenever the page reloads, the tab closes or the network drops. If the handler cancels the model call when that socket closes, a refresh truncates the answer. Move ownership to a run the server keeps in memory, buffer its events, and give the page a way to replay them.

## 1. Why a refresh kills the reply

**A streamed reply normally lives inside one request, so reloading the page closes the connection that is producing it.** The browser reads text events from the response as they arrive. On reload it tears down the old document and its connection. A server that treats "the response closed" as "the user stopped" then aborts the model call — the most common cause of a reply that ends halfway at exactly the moment someone refreshes.

The connection closing is not the same as the user wanting to stop. Separate the two in the server before anything else.

## 2. Give the run its own lifetime

**Create a run object first, then start the work detached from the request.** The run holds its own id, the chat it belongs to, an `AbortController`, and the browser subscribers currently watching it. The request handler starts the model call without awaiting it, then subscribes the response to the run.

Two rules keep the lifetime honest:

- Closing the response unsubscribes only. It never calls `abort()`.
- One explicit endpoint, such as `POST /chats/:id/stop`, is the only thing that aborts. Make it idempotent so a second tab, a double click or a late request is harmless.

`AbortController` is the standard way to cancel the underlying request or tool call ([MDN, AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController), checked 2026-11-15). Keep its signal on the run, not on the HTTP response.

## 3. Buffer events and replay them

**Every event gets a sequence number, so a new subscriber can ask for everything after the last one it saw.** The run appends each event to an in-memory buffer and fans it out to the subscribers attached at that moment.

The subscribe step must be atomic: replay buffered events, then add the subscriber, without an `await` in between. In a single-threaded server nothing can be appended during that block, so an event is either fully replayed or delivered live — never both, never neither. This is the detail that prevents a reloaded page from duplicating or skipping a sentence.

**Coalesce token deltas before assigning a sequence number.** A reply arrives as many tiny text fragments; merging them into chunks (for example at 1 KB or every 60 ms, whichever comes first) keeps the buffer small and makes a replay produce exactly the same text the live stream did. Assign the sequence number to the merged chunk, not to each token.

Replay and live delivery can share one server-sent events connection. Server-sent events are a way for a server to send a stream of text events to a page over one HTTP connection ([MDN, Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events), checked 2026-11-15). The built-in `EventSource` reconnects on its own and sends the last event id back, which a hand-written `fetch` reader does not do — if you read the stream with `fetch`, implement replay and reconnection yourself.

## 4. One active run per chat, and persist before you say done

**Allow one run per chat, and write the finished message before publishing the `done` event.** A second send while a reply is running should be refused with a conflict that names the active run, not started in parallel. Do the check and the reservation in one synchronous step, before any upload or database `await`, or two requests can both pass it.

When the run ends, save the assistant message and record the charge first, then publish `done`. A page that reloads in that window otherwise finds no active run and no saved message, and shows nothing.

Treat a disconnect as an opportunity to detach, not a reason to discard work: record it in the logs as a client disconnect, separately from an abort.

## 5. Let a second tab and the Stop button find the same run

**Expose a small endpoint that answers "is a run active in this chat?" and have idle tabs poll it.** That is enough for a second browser to attach to work started elsewhere: when the poll finds a run, it opens the replay endpoint, rebuilds the in-progress bubble and follows it live. A check on tab focus catches up immediately after a background tab wakes up.

The Stop button should call the stop endpoint and then keep reading its existing stream until the `done` event arrives with the partial answer. Closing the reader as the way to stop only works while the reader is the thing that owns the run — after this change it just means "stop watching".

## 6. What this does not survive

**An in-memory run is lost when the server process restarts.** The buffered events, the subscribers and the abort handle are gone, so a deploy or crash mid-reply leaves the user message without an answer. That may be acceptable; if it is not, persist a checkpoint of the partial answer and the request, and on boot either mark the run interrupted or restart it from the checkpoint, accepting that the model call itself starts over.

The registry is also process-local. Run one process, or send each chat to the same process every time (sticky sessions); a second worker has no idea the first one is streaming.

Bound the buffer while you are here. Cap the number of events and bytes per run, drop the oldest when the cap is hit, and delete finished runs after a few minutes. A long agent run that writes a lot of tool output will otherwise sit in memory long after anyone is watching.

## Checklist

| Check | What you should see |
|---|---|
| Refresh mid-answer | The earlier text reappears, streaming continues, one assistant message at the end |
| Close the tab | Logs show a client disconnect, no abort, then a normal finish and one charge |
| Second browser | It attaches within a poll interval and ends on the same single message |
| Stop | A partial answer is saved once, and the run disappears from the active list |
| Two sends at once | The second gets a conflict naming the active run, and its text is not lost |

## Related pages

- [Where an AI-built app keeps its data](Where-an-AI-built-app-keeps-its-data.md)
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md)
- [How to tell whether a deploy actually worked](Checking-whether-a-deploy-worked.md)

## See also

<!-- SEEALSO:START -->
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-15.

- MDN, [Server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- MDN, [AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-15. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
