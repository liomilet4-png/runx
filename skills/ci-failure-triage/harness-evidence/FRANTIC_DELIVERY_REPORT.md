# Frantic #61 delivery report

## Summary

- Package: `ci-failure-triage`
- Public registry URL: <https://runx.ai/x/liomilet4-png/ci-failure-triage@sha-92622cb44366>
- Upstream PR: <https://github.com/runxhq/runx/pull/153>
- Direct dogfood receipt: `runx:receipt:sha256:221e4d741c64374e622fa4defa9dcd1c332f5966b2d33b181267051db3bbc87b`

## Validation

- `runx --version`: see `dogfood-runx-version.txt`
- `runx add liomilet4-png/ci-failure-triage@sha-92622cb44366 --registry https://api.runx.ai`: success
- `runx skill liomilet4-png/ci-failure-triage@sha-92622cb44366 --registry https://api.runx.ai --json`: produced a governed `needs_agent` request
- `runx resume run_agent_task-ci-failure-triage-classify-output dogfood-answers.json --json`: sealed
- `runx verify --receipt dogfood-receipt.json --json`: `valid=true`
- Hosted registry harness: status passed, 2 checks passed, 0 failed
- This report is attached from PR head evidence so reviewers can fetch the raw package files and evidence from the same public commit.

## Dogfood Output

- Verdict: `real-break`
- Confidence: `0.91`
- Recommended lane: `issue-to-pr`
- Receipt id: `sha256:221e4d741c64374e622fa4defa9dcd1c332f5966b2d33b181267051db3bbc87b`

## Boundary

The skill is read-only. It classifies supplied CI evidence and emits a typed
triage packet. It does not rerun CI, open issues, mutate repositories, page
operators, or claim that a downstream lane has consumed the output.
