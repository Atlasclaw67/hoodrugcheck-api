# Changelog

Releases of this companion repo. The API itself is versioned separately: see `info.version` in [openapi.json](openapi.json).

## v0.3.7 (2026-11-12)

- Site: the limit message now says "Reports scanned in the last few minutes stay free", which matches the 10-minute window.
- Site: the per-browser id used for the free-scan limit is set only when a web page is loaded, not on files such as /openapi.json.
- No API change; `openapi.json` is unchanged (API version 1.3.1). Scores and checks are unchanged.

## v0.3.6 (2026-11-12)

- Site: free-scan limits are fairer on shared connections. A visitor's daily free scans are now counted per browser first, so a phone on a shared mobile or home connection is no longer blocked by other people's scans. A separate daily ceiling per connection still stops abuse.
- Site: a token report scanned in the last 10 minutes is free for anyone to open. It shows "Scanned N min ago" with a Rescan button. The limit message is plainer: "This connection has used today's free new scans. Reports already scanned stay free. Log in for 3 a day."
- No API change; `openapi.json` is unchanged (API version 1.3.1). Scores and checks are unchanged.

## v0.3.5 (2026-11-12)

- Site: every token report page on hoodrugcheck.com now has a separate "Team check (via HEY)" box beside the safety score. It comes from HEY Research Lab (https://heyresearch.xyz) and shows who builds the token and whether they ship: HEY's status, verified builder yes/no, whether the project names this contract, the last ship, and a link to the HEY page. A token HEY has no record of shows HEY's own wording. It is not part of the safety score and never changes it. If HEY is unavailable the box is hidden.
- Website token pages only. The API, the x402 endpoint and snapshot pages are unchanged; `openapi.json` is copied from https://hoodrugcheck.com/openapi.json and unchanged (API version 1.3.1).

## v0.3.4 (2026-11-11)

- README: "Docs" and "OpenAPI" links, plus a link to this changelog, at the top.
- Site: every hoodrugcheck.com page now links "API docs" (/docs) and "OpenAPI spec" (/openapi.json) in its footer and carries `<link rel="service-desc" type="application/json" href="/openapi.json">` and `<link rel="help" href="/docs">` in its `<head>`. No API change; `openapi.json` is unchanged (API version 1.3.1).

## v0.3.3 (2026-11-09)

- `openapi.json` copied from https://hoodrugcheck.com/openapi.json; unchanged (API version 1.3.1). No schema change: the fields are the same, the trading hook check's results and headlines are what changed.
- Scanner v7. The trading hook check scores a registered hook's fee: a fee locked per pool (Pons graduations) is scored at the pool's actual fee, an adjustable fee at the most it can be raised to. 5% or less earns full points, over 5% to 10% is a caution with partial points, over 10% a caution with a heavy deduction. An adjustable fee with no cap fails, and a fee that can't be read is unknown with no points. The check's headline names the case, e.g. "Fee locked at 3% per trade" or "Adjustable fee, max 20% per trade". `scanner_version` in paid responses is now 7.
- Site: report pages carry the real score in the server HTML (no more "0/100" without JavaScript), and the share buttons work in mobile and in-app browsers. /radar keeps scanner v6's record as its own frozen box.

## v0.3.2 (2026-11-06)

- `openapi.json` copied from https://hoodrugcheck.com/openapi.json (API version 1.3.1).
- Scanner v6 and detector v6: a sell simulation that hits a transport failure (timeout, connection error, 5xx, rate limit, an RPC error that isn't an execution revert) now reads as unknown, not as blocked. Any execution revert the node reports is still a blocked sell. `scanner_version` in paid responses is now 6.
- Site: /radar lists Called It cards again, and scanner v5 has its own frozen record next to v4's.

## v0.3.1 (2026-11-06)

- `openapi.json` copied from https://hoodrugcheck.com/openapi.json (API version 1.3.0): every check response has a `degraded` boolean, true when 3 or more of the 8 checks couldn't run because a read failed. `POST /api/v1/x402/check`, the Wafermap route and `POST /api/snapshots` answer 503 with `Retry-After` for a degraded scan, and nothing is charged.

## v0.3.0 (2026-11-05)

- `openapi.json` copied from https://hoodrugcheck.com/openapi.json (API version 1.2.0): adds `POST /api/snapshots`.
- README: snapshot links, frozen copies of one scan result at `/s/{id}`.

## v0.2.2 (2026-11-05)

- `openapi.json` copied from https://hoodrugcheck.com/openapi.json (API version 1.1.1): `GET /api/v1/x402/check` answers the same 402 as an unpaid POST, for probes. It sells nothing; pay with POST.

## v0.2.1 (2026-11-05)

- Site: /radar now has a "scanner v4, frozen record" box. No API change; `openapi.json` is unchanged (API version 1.1.0).

## v0.2.0 (2026-11-05)

- `openapi.json` copied from https://hoodrugcheck.com/openapi.json (API version 1.1.0): adds `POST /api/v1/x402/check`.
- README: x402 section, pay per call at $0.02 in USDC on Base or USDG on Robinhood Chain.

## v0.1.1 (2026-11-04)

- README: linked the Wafermap listing at https://wafermap.xyz/v1/m/hoodrugcheck.
- README: quick starts now use a placeholder token address.

## v0.1.0 (2026-11-04)

First public release.

- `openapi.json` copied from https://hoodrugcheck.com/openapi.json (API version 1.0.0, scanner v5).
- README with API key instructions, quick starts and MCP setup.
- `examples/`: curl, JavaScript and Python scripts for `GET /api/v1/check/{address}`.
