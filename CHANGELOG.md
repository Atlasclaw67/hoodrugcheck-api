# Changelog

Releases of this companion repo. The API itself is versioned separately: see `info.version` in [openapi.json](openapi.json).

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
