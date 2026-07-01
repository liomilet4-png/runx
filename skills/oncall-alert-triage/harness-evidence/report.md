# oncall-alert-triage Evidence Report

This report documents the `oncall-alert-triage` runx skill for Frantic bounty #64.

## Package

- Package: `liomilet4-png/oncall-alert-triage@sha-0c991037ca07`
- Registry URL: https://runx.ai/x/liomilet4-png/oncall-alert-triage@sha-0c991037ca07
- Hosted harness URL: https://runx.ai/x/liomilet4-png/oncall-alert-triage@sha-0c991037ca07#harness
- Source PR: https://github.com/runxhq/runx/pull/199
- Package path: `skills/oncall-alert-triage/`

## What The Skill Does

- Reads an alert with `id`, `service`, `severity`, and signal evidence.
- Resolves a sealed `runbook_ref` with page and incident-PR targets.
- Applies the declared `oncall_policy` for service and severity.
- Emits a single `runx.oncall.triage.v1` packet only when escalation or remediation is allowed.
- Refuses unsafe cases by returning `needs_agent` instead of inventing page targets or remediation steps.
- Never pages anyone, opens a PR, applies a fix, or mints authority.

## Validation

- `runx --version` returned `runx-cli 0.6.13`.
- `runx skill inspect ./skills/oncall-alert-triage/SKILL.md --json` passed.
- `runx harness ./skills/oncall-alert-triage -R $RUNX_RECEIPTS --json` passed with two cases.
- Hosted registry harness passed with two checks and zero failures.
- Dogfood run first returned `needs_agent`, then resumed with bounded answers and sealed.
- `runx verify --receipt ./skills/oncall-alert-triage/harness-evidence/dogfood-receipt.json --json` returned `valid=true`.

## Harness Cases

- `sealed_escalate_eligible_alert`: sealed runbook, declared service, and eligible sev2 alert. Expected status: `sealed`.
- `missing_runbook_stop`: unsealed runbook. Expected status: `needs_agent`.

## Dogfood Output

- Decision action: `escalate`.
- Decision reason: `checkout-api` is declared in policy, the runbook is sealed, and `8.2%` 5xx for `16m` exceeds the `2% for 10m` threshold.
- Page target: `team-checkout-primary`.
- Incident PR target: `example/checkout-api`, branch `incident/checkout-5xx-alert-checkout-2026-06-30-dogfood`.
- Review note body: include error-rate graph, deploy sha `4f21c9e`, rollback candidate, and customer-impact note.
- Escalation lane: `human_approval`.
- Dogfood receipt: `runx:receipt:sha256:dd2e65e6bd67dab2a5fa8a99a93c82af87f55ef1df9d7987ca5c73678d3b3639`.

## How To Reproduce

1. Install the package:
   `runx add liomilet4-png/oncall-alert-triage@sha-0c991037ca07 --registry https://api.runx.ai`
2. Inspect the source files in PR #199 under `skills/oncall-alert-triage/`.
3. Run the local harness:
   `runx harness ./skills/oncall-alert-triage --json`
4. Run the skill with the dogfood alert, sealed runbook, and oncall policy from `harness-evidence/`.
5. Resume the generated run with `dogfood-answers.json`.
6. Verify `dogfood-receipt.json` with `runx verify --receipt ... --json`.

## Safety Boundary

- The skill is read-only.
- The skill emits a packet for downstream governed runs; it does not dispatch those runs itself.
- Page sends, issue-to-PR work, and PR review comments remain separate governed actions.
- Missing or unsealed runbooks produce `needs_agent`.
- Undeclared services are refused.
- No credentials, tokens, private customer data, or local machine paths are included in these artifacts.
