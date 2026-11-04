#!/usr/bin/env bash
# Check a Robinhood Chain (chain ID 4663) token with HoodRugCheck.
#
#   ./check.sh 0xTOKEN_ADDRESS
#
# Optional: export HOODRUGCHECK_API_KEY=... to use a Pro key (full evidence, 120 requests/hour).
# Without a key: 10 requests/hour per IP, with evidence_locked: true.
set -euo pipefail

address="${1:?usage: ./check.sh 0xTOKEN_ADDRESS}"
url="https://hoodrugcheck.com/api/v1/check/${address}"
body="$(mktemp)"
trap 'rm -f "$body"' EXIT

auth=()
if [ -n "${HOODRUGCHECK_API_KEY:-}" ]; then
  auth=(-H "Authorization: Bearer ${HOODRUGCHECK_API_KEY}")
fi

# A cold scan can answer 202 ("scanning"). Wait, then repeat the same GET.
for _ in 1 2 3 4 5 6 7 8 9 10; do
  code="$(curl -sS -m 40 -o "$body" -w '%{http_code}' ${auth[@]+"${auth[@]}"} "$url")"
  if [ "$code" != "202" ]; then
    cat "$body"
    echo
    [ "$code" = "200" ] && exit 0
    echo "HTTP $code" >&2
    exit 1
  fi
  echo "Still scanning, retrying in 5 seconds..." >&2
  sleep 5
done

echo "Scan did not finish in time. Try again shortly." >&2
exit 1
