---
name: oncall-alert-triage
description: Classify on-call alerts against a sealed runbook and policy, then emit a bounded escalation packet only when evidence supports it.
runx:
  category: planning
---

# On-call Alert Triage

Use this skill when an operator needs a read-only first pass on an alert before
opening an incident lane. The skill reads an alert, a runbook reference, and an
on-call policy. It returns a bounded decision and, only when the policy and
runbook support escalation, one `runx.oncall.triage.v1` packet for downstream
page, incident PR, and PR review-note runs.

The skill never pages anyone, opens incidents, edits runbooks, creates PRs,
mints authority, or emits an `AttenuationRequest`. It only names the downstream
governed runs that a separate operator or driver may dispatch.

## Inputs

- `alert.id`: stable alert identifier.
- `alert.service`: service named by the alert.
- `alert.severity`: alert severity, such as `sev2` or `sev3`.
- `alert.signal`: bounded signal packet with metric, threshold, observed value,
  duration, and recent change context.
- `runbook_ref`: sealed runbook reference containing digest, status, page
  target, incident PR target, and review-note body.
- `oncall_policy.services`: declared services that this skill may judge.
- `oncall_policy.escalation_rules`: allowed actions by severity and service.

## Output

The default runner returns:

- `decision.action`: `acknowledge`, `escalate`, `auto_remediate`, or
  `suppress`.
- `decision.reason`: concise explanation citing the policy and runbook evidence.
- `packet`: a single `runx.oncall.triage.v1` packet only when the action is
  `escalate` or `auto_remediate`.
- `escalation`: the human approval or dispatch lane that must handle the packet.

## Packet Boundaries

The packet is not consumed as an effect by this skill. A downstream driver or
operator dispatches by naming separate governed runs:

- `live-page-send` for the page target.
- `issue-to-pr` for an incident PR behind a human merge gate.
- `pr-review-note` for the review-note body.

If a runbook is unsealed, missing, contradictory, or does not bind both page and
incident PR targets, the skill returns `needs_agent` and emits no packet.

## Refusal Rules

- Refuse services that are not declared in `oncall_policy.services`.
- Refuse escalation paths not listed in the sealed runbook.
- Refuse to invent remediation, page targets, incident PR targets, or review
  note text.
- Refuse if the supplied signal lacks metric, threshold, observed value, or
  duration evidence.
- Refuse if no page or incident PR target can be bound.

## Harness Cases

- `sealed_escalate_eligible_alert`: a declared checkout service emits sustained
  error-rate burn; the runbook is sealed and binds page and incident PR targets.
  Expected status is sealed, with decision action `escalate` and one
  `runx.oncall.triage.v1` packet.
- `missing_runbook_stop`: the service is declared but the runbook is missing and
  no caller answers are supplied for the packet step. Expected status is
  `needs_agent`, with no packet.

