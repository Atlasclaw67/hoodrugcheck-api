#!/usr/bin/env python3
"""Check a Robinhood Chain (chain ID 4663) token with HoodRugCheck. Python 3.8+, no dependencies.

    python3 check.py 0xTOKEN_ADDRESS

Optional: export HOODRUGCHECK_API_KEY=... to use a Pro key (full evidence, 120 requests/hour).
Without a key: 10 requests/hour per IP, with evidence_locked: true.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

MAX_ATTEMPTS = 10


def check_token(address, api_key=None):
    api_key = api_key or os.environ.get("HOODRUGCHECK_API_KEY")
    headers = {"User-Agent": "hoodrugcheck-api-examples"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(
        f"https://hoodrugcheck.com/api/v1/check/{address}", headers=headers
    )

    for _ in range(MAX_ATTEMPTS):
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                status, body = response.status, json.load(response)
        except urllib.error.HTTPError as err:
            body = json.load(err)
            raise RuntimeError(f"HTTP {err.code}: {body.get('error')} ({body.get('code')})")
        if status == 200:
            return body

        # A cold scan answers 202 while it runs. Wait, then repeat the same GET.
        print(f"Still scanning, retrying in {body['retry_after']} seconds...", file=sys.stderr)
        time.sleep(body["retry_after"])
    raise RuntimeError("Scan did not finish in time. Try again shortly.")


def main():
    if len(sys.argv) != 2:
        print("usage: python3 check.py 0xTOKEN_ADDRESS", file=sys.stderr)
        return 2
    try:
        result = check_token(sys.argv[1])
    except (RuntimeError, urllib.error.URLError) as err:
        print(err, file=sys.stderr)
        return 1

    # score is None when status is "incomplete": there is no verdict to trust.
    score = "none" if result["score"] is None else result["score"]
    print(f"{result.get('symbol') or sys.argv[1]}: score {score}, status {result['status']}")
    print(result["verdict"])
    for check in result["checks"]:
        print(f"  {check['result']:<8}{check['label']}")
        for line in check["evidence"]:
            print(f"          {line}")
    if result["evidence_locked"]:
        print(f"Evidence locked. Upgrade: {result['upgrade_url']}")
    print(f"Report: {result['report_url']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
