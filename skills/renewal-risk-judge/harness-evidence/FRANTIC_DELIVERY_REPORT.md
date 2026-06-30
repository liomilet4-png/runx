# Frantic #63 Delivery Report

## Summary

- Package: `renewal-risk-judge`
- Scope: read-only renewal risk judgment over usage, support, and payment signals.
- Boundary: the skill emits a recommendation packet only. It does not send messages, quote discounts, change invoices, touch payment rails, or contact customers.
- PR source: pending public PR against `runxhq/runx`.
- Registry package: pending `runx registry publish` after publish login.

## Acceptance Coverage

- Uses exact package name `renewal-risk-judge`.
- Declares typed inputs `usage_signals`, `support_history`, and `payment_snapshot`.
- Declares output packet `runx.support.renewal_risk.v1`.
- Includes one sealed high-risk inline harness case.
- Includes one stop case for missing `usage_signals`.
- Documents dispatch-by-naming: any actual send must occur in a separate governed run with human approval.
- Refuses to invent missing usage decline, payment lateness, churn, or customer facts.

## Pending Validation

- `runx --version`: `runx-cli 0.6.13`
- `runx skill inspect ./skills/renewal-risk-judge --json`: passed locally.
- `runx harness ./skills/renewal-risk-judge`: pending Linux/hosted harness because the Windows receipt store cannot write `sha256:` receipt filenames.
- `runx registry publish ./skills/renewal-risk-judge/SKILL.md --registry https://api.runx.ai`: pending publish login.
- Post-publish `runx add`, dogfood `runx skill`, and `runx verify`: pending registry publish.

## Human Value

Operators can use this skill to separate high-risk renewal accounts from low-risk or incomplete cases without granting the skill authority to send messages or alter money-related records.
