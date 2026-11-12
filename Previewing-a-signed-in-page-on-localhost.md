---
title: "Previewing a signed-in page on localhost"
description: "When sign-in cannot finish on http://localhost, sign the session cookie yourself with the app's own secret, on loopback only, to preview the signed-in page."
category: How-to
tags: [auth]
order: 8
checked: 2026-11-11
---

<!-- NAV:START -->
[Home](README.md) › [How-to](Category-How-to.md) · Tags: [auth](Tag-auth.md)
<!-- NAV:END -->

# Previewing a signed-in page on localhost

**When sign-in cannot finish on `http://localhost`, sign the session cookie yourself with the app's own secret and set it for that origin: it is a preview of the signed-in page, not a sign-in.** The shortcut skips the provider, so it proves nothing about the real login flow; test that on an address the provider accepts.

## Why sign-in stops on localhost

**A provider that requires an https redirect URI has nowhere to send a local http app back to.** OAuth 2.0 tells authorization servers that "The redirection endpoint SHOULD require the use of TLS" ([RFC 6749, §3.1.2.1](https://www.rfc-editor.org/rfc/rfc6749#section-3.1.2.1), checked 2026-11-11), and a provider may enforce that by refusing to register or use an `http://` address. The request is refused before your app ever sees a code.

Some providers follow the OAuth 2.0 profile for native apps, which makes loopback an exception: "Loopback redirect URIs use the \"http\" scheme" and "The authorization server MUST allow any port to be specified at the time of the request for loopback IP redirect URIs" ([RFC 8252, §7.3](https://www.rfc-editor.org/rfc/rfc8252#section-7.3), checked 2026-11-11). Check the provider's own documentation first: if it accepts `http://127.0.0.1:PORT` as a redirect, register that exact address and sign in normally. A temporary https tunnel in front of the local port is the other option; it needs a registration change and a public name, and it lasts only as long as the tunnel.

## Find the cookie the server verifies

**The shortcut needs three things from the server code: the cookie name it reads, the payload shape it verifies, and the [secret](Glossary.md#secret) it verifies with.** Look for the function that reads the session cookie and the code that sets it after a successful sign-in. If the app keeps sessions in a database or an in-memory map keyed by an opaque id, there is no signed cookie to mint; use a development sign-in hook or a seeded test user instead.

## Mint the cookie

**Build the payload the server expects, sign it with HMAC-SHA256 using the same secret, and set `name=payload.signature` for the local origin.** The script below is an example, not a drop-in: keep the claim names, the cookie name and the signing order your server uses, and read the secret from the same [environment variable](Glossary.md#environment-variable) the server does.

```js
// Local preview only. Signs the same session cookie the app would set,
// with the same secret. Never run this against a deployed server.
import crypto from 'node:crypto';

const secret = process.env.SESSION_SECRET; // the value the dev server started with
const payload = Buffer.from(JSON.stringify({
  sub: 'local-dev',
  email: 'you@example.com',
  name: 'Local Dev',
  exp: Math.floor(Date.now() / 1000) + 8 * 3600, // 8 hours
})).toString('base64url');
const signature = crypto.createHmac('sha256', secret).update(payload).digest('base64url');
console.log(`session=${payload}.${signature}`);
```

Start the local server with a secret made for development, then add the printed value under that cookie name in the browser's cookie store for `localhost` — DevTools → Application → Cookies — and reload. The cookie panel can store a cookie the server marks [HttpOnly](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie), which "Forbids JavaScript from accessing the cookie" ([MDN, Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie), checked 2026-11-11); a `document.cookie` assignment is the quicker route only while the browser holds no HttpOnly cookie of that name yet.

## Skip the cookie panel with a loopback proxy

**A proxy bound to `127.0.0.1` that adds the `Cookie` header on every request lets you open the preview like any other URL.** Forward each request to the app, replace the `Cookie` header with the minted value, and keep the listener on loopback: "Clients should listen on the loopback network interface only, in order to avoid interference by other network actors" ([RFC 8252, §8.3](https://www.rfc-editor.org/rfc/rfc8252#section-8.3), checked 2026-11-11).

```js
// proxy.mjs — forward to the dev server and inject the session cookie.
import http from 'node:http';

const cookie = process.argv[2]; // name=payload.signature
http.createServer((req, res) => {
  const upstream = http.request({
    host: '127.0.0.1', port: 3000, path: req.url, method: req.method,
    headers: { ...req.headers, host: '127.0.0.1:3000', cookie },
  }, (up) => { res.writeHead(up.statusCode, up.headers); up.pipe(res); });
  upstream.on('error', (error) => { res.writeHead(502); res.end(error.message); });
  req.pipe(upstream);
}).listen(4000, '127.0.0.1');
```

Start the app with its public origin set to the proxy's address (for example `http://localhost:4000`), run `node proxy.mjs 'session=…'`, and open `http://localhost:4000`. The proxy holds a credential: do not bind it to `0.0.0.0`, and never deploy it.

## What the preview does not test

**The shortcut proves the signed-in page renders; it does not test authentication.** These still need an address the provider accepts, usually a staging [deploy](Glossary.md#deploy) or an https tunnel:

- the provider's redirect and callback, including the `state` and nonce checks;
- the token exchange and the checks on the returned id_token, such as issuer, audience and allowed email domain;
- the cookie the server sets for real: its `Secure`, `HttpOnly` and `SameSite` attributes, and its lifetime;
- sign-out, which clears the session cookie, and what happens when the cookie expires or the secret rotates.

Treat a broken real sign-in as a separate problem; the pages on [login loops](A-login-that-loops.md) and [redirect URIs behind a proxy](A-sign-in-that-breaks-behind-a-proxy.md) cover the common causes.

## Keep the shortcut local

- Use a development secret, not the deployed one; keep it in the environment and out of the repository.
- The minted cookie is a credential for that origin. Delete it when you finish, and do not share it.
- Run the minting script and any proxy on your own machine, on loopback only.
- If you change the secret, mint the cookie again; every existing session becomes invalid.

## Related pages

- [A login that loops between your app and the sign-in provider](A-login-that-loops.md)
- [A sign-in that breaks behind a proxy: the redirect URI](A-sign-in-that-breaks-behind-a-proxy.md)
- [How to check a web app an AI built](Checking-an-AI-built-web-app.md)

## See also

<!-- SEEALSO:START -->
Glossary terms used on this page: [Deploy](Glossary.md#deploy), [Environment variable](Glossary.md#environment-variable), [Provider](Glossary.md#provider), [Secret](Glossary.md#secret), [Token](Glossary.md#token).
<!-- SEEALSO:END -->

## Sources

All checked on 2026-11-11.

- [RFC 6749, The OAuth 2.0 Authorization Framework, §3.1.2.1](https://www.rfc-editor.org/rfc/rfc6749#section-3.1.2.1)
- [RFC 8252, OAuth 2.0 for Native Apps, §7.3 and §8.3](https://www.rfc-editor.org/rfc/rfc8252#section-7.3)
- [MDN, Set-Cookie](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie)

---

First version written with AI assistance and checked against the [sources](#sources) on 2026-11-11. Found a mistake? [Fix it or open an issue](CONTRIBUTING.md). Text licensed under [CC BY 4.0](LICENSE).
