# Frantic #61 delivery report

## Summary

- Package: `ci-failure-triage`
- Public registry URL: <https://runx.ai/x/liomilet4-png/ci-failure-triage@sha-92622cb44366>
- Upstream PR: <https://github.com/runxhq/runx/pull/153>
- Public source: <https://github.com/liomilet4-png/ci-failure-triage-runx-skill/tree/44476c32d79002b38b08ef2cc3e61cd9d0d855f9>

## What to inspect first

- `SKILL.md` for the read-only CI failure triage contract.
- `X.yaml` for the typed `classify` runner and the two required harness cases.
- `harness-evidence/evidence.json` for the Ubuntu GitHub Actions evidence summary.
- `harness-evidence/verification.json` for `valid=true` receipt verification.

## Validation

- `runx --version`: `runx-cli 0.6.13`
- `runx skill inspect ./skills/ci-failure-triage --json`: `status=ok`
- `runx harness ./skills/ci-failure-triage -R "$RUNX_RECEIPTS" --json`: `status=passed`
- Hosted registry harness: `status=passed`, `checks_passed=2`, `checks_failed=0`
- Harness cases: `real_break_clear_logs`, `ambiguous_truncated_logs`
- Harness assertion errors: `0`
- `runx verify <harness-receipt-id> --receipt-dir "$RUNX_RECEIPTS" --json`: `valid=true`
- Hosted harness receipt: `runx:receipt:sha256:e7c373b1e7bb676d1d8b28429ed8a24b4f1259eb64aba36e080d8f8ee1cd11b6`
- Clean install: `runx add liomilet4-png/ci-failure-triage@sha-92622cb44366 --registry https://api.runx.ai`

## Boundary

The direct dogfood run returns `needs_agent` because `classify` is an
`agent-task` runner and the direct command does not supply seeded harness
answers. The governed harness supplies those answers for the required happy and
stop cases and produces the verified receipt.

The hosted registry package was published after `runx login --for publish`
issued a purpose-scoped publish credential. Windows local `runx registry publish`
is blocked on this machine by the runx receipt-store filename issue with
`sha256:` receipt ids, so the same hosted publish endpoint used by the CLI was
called directly. The server-side hosted registry harness passed and is visible
at <https://runx.ai/x/liomilet4-png/ci-failure-triage@sha-92622cb44366#harness>.
