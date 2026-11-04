// Check a Robinhood Chain (chain ID 4663) token with HoodRugCheck. Node 18+, no dependencies.
//
//   node check.mjs 0xTOKEN_ADDRESS
//
// Optional: export HOODRUGCHECK_API_KEY=... to use a Pro key (full evidence, 120 requests/hour).
// Without a key: 10 requests/hour per IP, with evidence_locked: true.

const MAX_ATTEMPTS = 10;

export async function checkToken(address, apiKey = process.env.HOODRUGCHECK_API_KEY) {
  const url = `https://hoodrugcheck.com/api/v1/check/${address}`;
  const headers = apiKey ? { Authorization: `Bearer ${apiKey}` } : {};

  for (let attempt = 0; attempt < MAX_ATTEMPTS; attempt++) {
    const res = await fetch(url, { headers });
    const body = await res.json();
    if (res.status === 200) return body;
    if (res.status !== 202) throw new Error(`HTTP ${res.status}: ${body.error} (${body.code})`);

    // A cold scan answers 202 while it runs. Wait, then repeat the same GET.
    console.error(`Still scanning, retrying in ${body.retry_after} seconds...`);
    await new Promise((resolve) => setTimeout(resolve, body.retry_after * 1000));
  }
  throw new Error('Scan did not finish in time. Try again shortly.');
}

const address = process.argv[2];
if (!address) {
  console.error('usage: node check.mjs 0xTOKEN_ADDRESS');
  process.exit(2);
}

try {
  const result = await checkToken(address);
  // score is null when status is "incomplete": there is no verdict to trust.
  console.log(`${result.symbol ?? address}: score ${result.score ?? 'none'}, status ${result.status}`);
  console.log(result.verdict);
  for (const check of result.checks) {
    console.log(`  ${check.result.padEnd(8)}${check.label}`);
    for (const line of check.evidence) console.log(`          ${line}`);
  }
  if (result.evidence_locked) console.log(`Evidence locked. Upgrade: ${result.upgrade_url}`);
  console.log(`Report: ${result.report_url}`);
} catch (err) {
  console.error(err.message);
  process.exit(1);
}
