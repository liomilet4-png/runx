# Frantic #61 delivery report

## Summary

- Package: `ci-failure-triage`
- Public registry URL: <https://runx.ai/x/liomilet4-png/ci-failure-triage@sha-92622cb44366>
- Upstream PR: <https://github.com/runxhq/runx/pull/153>
- Direct dogfood receipt: `runx:receipt:sha256:abc25f1cc54fde5ae6a88fe4f1e59133e181c557374334e4df764bb0b68389a1`

## Validation

- `runx --version`: see `dogfood-runx-version.txt`
- `runx add liomilet4-png/ci-failure-triage@sha-92622cb44366 --registry https://api.runx.ai`: success
- `runx skill liomilet4-png/ci-failure-triage@sha-92622cb44366 --registry https://api.runx.ai --json`: produced a governed `needs_agent` request
- `runx resume run_agent_task-ci-failure-triage-classify-output dogfood-answers.json --json`: sealed
- `runx verify --receipt dogfood-receipt.json --json`: `valid=true`
- Hosted registry harness: status passed, 2 checks passed, 0 failed

## Dogfood Output

- Verdict: `real-break`
- Confidence: `0.91`
- Recommended lane: `issue-to-pr`
- Receipt id: `sha256:abc25f1cc54fde5ae6a88fe4f1e59133e181c557374334e4df764bb0b68389a1`

## Boundary

The skill is read-only. It classifies supplied CI evidence and emits a typed
triage packet. It does not rerun CI, open issues, mutate repositories, page
operators, or claim that a downstream lane has consumed the output.
