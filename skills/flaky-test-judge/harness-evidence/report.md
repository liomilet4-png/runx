# Frantic bounty #66 evidence report

Bounty #66 implements `liomilet4-png/flaky-test-judge`, a runx skill that judges flaky-test history and emits a quarantine packet, an ignore decision, or a stop state when required evidence is missing.

## Public package

- PR: https://github.com/runxhq/runx/pull/201
- Published package: `liomilet4-png/flaky-test-judge@sha-d9cd53adcfae`
- Public page: https://runx.ai/x/liomilet4-png/flaky-test-judge@sha-d9cd53adcfae
- Install: `runx add liomilet4-png/flaky-test-judge@sha-d9cd53adcfae --registry https://api.runx.ai`
- Run: `runx skill liomilet4-png/flaky-test-judge@sha-d9cd53adcfae --registry https://api.runx.ai`
- Registry digest: `sha256:8d1fab2a5d073501e0804b021fb19a8c0d5bde3d77fbddb80a8208b8e5abdb07`
- Profile digest: `sha256:d369683ba8b8992966ebec943dfc38bad4c11a82105745907fdc5a009767d087`
- CLI version evidence: `runx-cli 0.6.13`

## Hosted publish harness

- Publish HTTP status: 201
- Publish status: published
- Harness status: passed
- Cases: `quarantine_justified`, `missing_run_history`
- Assertion errors: 0
- Hosted harness receipt: `sha256:f7bfaf490987778937062710e05df7687ccad0ec07d84616c097fb2f9b607e09`
- Hosted harness evidence: https://runx.ai/x/liomilet4-png/flaky-test-judge#harness

## Local source harness

The local source harness passed two cases:

- `quarantine_justified`: validates the expected quarantine packet and `issue-to-pr` dispatch target.
- `missing_run_history`: validates the stop path by returning `needs_agent` when run history is absent instead of fabricating a result.

## Clean install and inspect

A clean `RUNX_HOME` installed and inspected the published registry package successfully.

- Inspect status: ok
- Registry trust state: trusted
- Registry key id: `runx-registry-ed25519-v1`
- Runner: `triage`

## Post-publish dogfood receipt

A post-publish dogfood run was started from the installed registry package, resumed with the operator answer payload, and sealed.

- Run id: `run_agent_task-flaky-test-judge-triage-output`
- Skill status: sealed
- Receipt id: `sha256:284ea73e089fe945831a426060ba0338da5fcfbfaf8cc50fe3fa411152219ed0`
- Closure: closed
- Decision: quarantine
- Dispatch target: `issue-to-pr`
- Escalation lane: `human_merge_gate`

The official npm CLI `runx-cli 0.6.13` was also checked directly. On this Windows host it can start the registry dogfood run and produce the `needs_agent` state, but `resume` reproducibly hit `receipt store is unreadable: os error 87`; the sealed dogfood receipt above was produced and verified with the local Windows debug runx binary from the same PR worktree.

## Receipt verification

`runx verify` verified the post-publish dogfood receipt using the matching Ed25519 verifier public key.

- Verdict valid: true
- Digest: valid
- Content address: valid
- Signature: valid (production)
- Findings: 0

## Privacy boundary

This evidence folder intentionally excludes raw receipt JSON files, signing seed material, agent tokens, cookies, payment data, and account credentials. Public files contain only hashes, receipt ids, package metadata, and validation summaries.