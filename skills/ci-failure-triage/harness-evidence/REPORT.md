# ci-failure-triage evidence report

## What changed

- Added the `ci-failure-triage` runx skill package.
- Added a typed `classify` runner that emits a `runx.ci.triage.v1` packet.
- Added two required harness cases:
  - `real_break_clear_logs`
  - `ambiguous_truncated_logs`

## Validation

- `runx --version`: `runx-cli 0.6.13`
- `runx skill inspect ./skills/ci-failure-triage --json`: status `ok`
- `runx harness ./skills/ci-failure-triage -R "$RUNX_RECEIPTS" --json`: status `passed`
- Harness case count: `2`
- Harness assertion error count: `0`
- `runx verify <harness-receipt-id> --receipt-dir "$RUNX_RECEIPTS" --json`: `valid=true`

## Evidence files

- `evidence.json`: summary of the runx version, inspect, harness, dogfood, and verification observations.
- `verification.json`: receipt verification output with `valid=true`.
- `harness.json`: harness result and receipt id.
- `dogfood.json`: direct `runx skill` execution result against the clear CI failure fixture.
- `skill-inspect.json`: package inspection result.
- `runx-version.txt`: exact CLI version used.

## Notes

- The direct dogfood run returns `needs_agent` because the skill runner is an `agent-task` and no seeded harness answer is supplied in that direct run.
- The sealed and verified receipt is produced by the governed harness run, where the required fixture answers are supplied through `X.yaml`.
- The skill is read-only and does not rerun CI, open issues, page operators, or mutate repositories.
