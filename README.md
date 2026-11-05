# HoodRugCheck API

Public API docs, examples and MCP setup for [HoodRugCheck](https://hoodrugcheck.com), the token safety scanner for **Robinhood Chain** (EVM, chain ID 4663).

Give it a Robinhood Chain token address and it runs 8 on-chain checks against live chain state: mint authority, admin control, liquidity, holder concentration, sellability, contract verification, token age and trading hooks. You get back a score, a tradeability status and the result of each check. It's built for AI agents and apps that need a go/no-go signal before trading or recommending a token.

Informational only, not financial advice.

- Website: https://hoodrugcheck.com
- API docs: https://hoodrugcheck.com/docs
- OpenAPI spec: https://hoodrugcheck.com/openapi.json (copy in [openapi.json](openapi.json))
- MCP endpoint: `https://hoodrugcheck.com/mcp`

This repo holds docs and examples only. The scanner itself isn't here.

## API keys

A key is optional.

| | Rate limit | Evidence behind each check |
|---|---|---|
| No key | 10 requests/hour per IP | Locked (`evidence_locked: true`) |
| Pro key | 120 requests/hour | Full |

The score, status, verdict and every check's result are included either way.

To get a key, [upgrade to Pro](https://hoodrugcheck.com/pricing), then generate one on your [account page](https://hoodrugcheck.com/account). The key is shown once, at creation. Send it as `Authorization: Bearer <key>` or `X-API-Key: <key>`.

The examples read the key from an environment variable, so it stays out of your code:

```bash
export HOODRUGCHECK_API_KEY="your-key-here"
```

## Quick start

`GET /api/v1/check/{address}` takes a token contract address on Robinhood Chain. In these examples, replace `0xYOUR_TOKEN_ADDRESS` with the address you want to check: `0x` followed by 40 hex characters.

### curl

```bash
curl https://hoodrugcheck.com/api/v1/check/0xYOUR_TOKEN_ADDRESS \
  -H "Authorization: Bearer $HOODRUGCHECK_API_KEY"
```

Leave out the `-H` line to call it without a key.

### JavaScript

```js
const address = '0xYOUR_TOKEN_ADDRESS';
const apiKey = process.env.HOODRUGCHECK_API_KEY;

const res = await fetch(`https://hoodrugcheck.com/api/v1/check/${address}`, {
  headers: apiKey ? { Authorization: `Bearer ${apiKey}` } : {},
});
const result = await res.json();
console.log(res.status, result.score, result.status, result.verdict);
```

### Python

```python
import json, os, urllib.request

address = "0xYOUR_TOKEN_ADDRESS"
headers = {"User-Agent": "hoodrugcheck-api-examples"}
if os.environ.get("HOODRUGCHECK_API_KEY"):
    headers["Authorization"] = f"Bearer {os.environ['HOODRUGCHECK_API_KEY']}"

request = urllib.request.Request(
    f"https://hoodrugcheck.com/api/v1/check/{address}", headers=headers
)
with urllib.request.urlopen(request) as response:
    result = json.load(response)
    print(response.status, result.get("score"), result.get("status"), result.get("verdict"))
```

### Runnable scripts

The scripts in [examples/](examples) also wait and retry on `202` and report errors:

```bash
./examples/check.sh 0xYOUR_TOKEN_ADDRESS
```

```bash
node examples/check.mjs 0xYOUR_TOKEN_ADDRESS
```

```bash
python3 examples/check.py 0xYOUR_TOKEN_ADDRESS
```

## Reading the response

```json
{
  "version": "1",
  "address": "0x...",
  "name": "Example Token",
  "symbol": "EX",
  "score": 0,
  "raw_score": 0,
  "cap_reason": null,
  "status": "tradeable",
  "verdict": "One-line summary",
  "checks": [
    { "id": "liquidity", "label": "Liquidity", "result": "pass", "evidence": [] }
  ],
  "creator": "0x...",
  "red_flags": [],
  "info_flags": [],
  "evidence_locked": true,
  "upgrade_url": "https://hoodrugcheck.com/pricing",
  "report_url": "https://hoodrugcheck.com/token/0x...",
  "scanned_at": "2026-11-04T00:00:00.000Z",
  "disclaimer": "..."
}
```

The field values above are placeholders. [openapi.json](openapi.json) has the full schema.

Three things to handle in your integration:

- **A `null` score isn't a clean token.** `status: "incomplete"` means pool discovery failed or couldn't finish, so `score` and `raw_score` are `null` and there's no verdict to trust. Retry shortly.
- **`unknown` isn't a pass.** A check's `result` is `pass`, `warn`, `fail` or `unknown`. `unknown` means the answer couldn't be established.
- **`202` means still scanning.** A cold scan still running after 18 seconds answers `202` with `retry_after`. Wait that many seconds and repeat the same GET. Results are cached for 2 minutes.

| Status code | Meaning |
|---|---|
| `200` | Scan complete |
| `202` | Still scanning; retry after `retry_after` seconds |
| `400` | Invalid address, wrong chain or not a token contract |
| `401` | The API key is malformed, unknown or revoked. It doesn't fall back to anonymous access |
| `429` | Rate limit exceeded |
| `502` | The chain didn't answer in time; safe to retry |

Every response carries `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers.

`GET /api/v1/wallet/{address}` returns what the chain shows about a wallet, with the same keys and limits. See the [API docs](https://hoodrugcheck.com/docs).

## MCP setup

The same checks are available as MCP tools at `https://hoodrugcheck.com/mcp` (Streamable HTTP, stateless):

- `check_token`: the token check above
- `check_wallet`: the wallet lookup

The limits are the same as the REST API, and a key is optional. If `check_token` reports that a scan is still running, call it again after the number of seconds it gives.

**Claude Code**

```bash
claude mcp add --transport http hoodrugcheck https://hoodrugcheck.com/mcp
```

With a Pro key:

```bash
claude mcp add --transport http hoodrugcheck https://hoodrugcheck.com/mcp --header "Authorization: Bearer $HOODRUGCHECK_API_KEY"
```

**Cursor** (`~/.cursor/mcp.json`)

```json
{
  "mcpServers": {
    "hoodrugcheck": {
      "url": "https://hoodrugcheck.com/mcp",
      "headers": { "Authorization": "Bearer ${env:HOODRUGCHECK_API_KEY}" }
    }
  }
}
```

Remove `headers` to use it without a key. Other MCP clients that support Streamable HTTP can use the same URL and header.

## Wafermap

The token check is also on the Wafermap marketplace as [HoodRugCheck Token Check](https://wafermap.xyz/v1/m/hoodrugcheck), where agents pay per call instead of using an API key.

## x402 (pay per call)

Agents can also pay per call with no API key. `POST https://hoodrugcheck.com/api/v1/x402/check` is a native x402 v2 endpoint at **$0.02 per call**, paid in USDC on Base or USDG on Robinhood Chain.

```bash
curl -i -X POST https://hoodrugcheck.com/api/v1/x402/check \
  -H 'content-type: application/json' \
  -d '{"address":"0xYOUR_TOKEN_ADDRESS"}'
```

Without a payment it answers `402` with the offers in the body and the `PAYMENT-REQUIRED` header. An x402 v2 client signs one and resends the call. You get the same 8 checks as the API, with full evidence.

`GET` on the same URL answers the same 402, for probes. It sells nothing; pay with POST.

A call is settled only after a complete result. A scan still running (`503` + `Retry-After: 30`), a failed scan or an incomplete scan (`score: null`) is not charged. Manifest: https://hoodrugcheck.com/.well-known/x402

## License

[MIT](LICENSE). This covers the docs and examples in this repo.
