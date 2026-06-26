---
name: renewal-risk-judge
description: Fuse usage, support, and payment signals into a read-only renewal risk verdict with a bounded save-plan recommendation that requires human approval before any downstream send.
runx:
  category: support
---

# Renewal Risk Judge

Judge whether a renewing account needs intervention and, when the evidence
supports high or critical risk, emit a bounded save-plan recommendation as data.

This skill is read-only. It does not send messages, apply discounts, quote
prices, change invoices, access payment rails, or contact customers. It emits a
`runx.support.renewal_risk.v1` verdict that a human or a separately approved
downstream send-as lane can inspect.

## Inputs

- `usage_signals` (required): object with `trend` and `mau_pct_change`.
- `support_history` (required): object with `volume` and
  `ticket_severity_avg`.
- `payment_snapshot` (required): object with `days_late` and `churn_flag`.
- `account_ref` (optional): stable account label for the verdict.
- `operator_context` (optional): constraints, renewal timing, or approval notes.

## Output

The default runner returns one `runx.support.renewal_risk.v1` packet:

```yaml
decision:
  risk_level: low | moderate | high | critical
  justification: string
fused_score:
  total: number
  weights:
    usage_trend: number
    support: number
    payment: number
escalation:
  lane: human_approval | monitor | no_action
  reason: string
save_plan:
  channel: string
  audience: string
  content_ref: string
receipt_notes:
  recommendation_only: true
  sends_message: false
  touches_money: false
  dispatch_by_naming: string
```

`save_plan` is present only when `decision.risk_level` is `high` or
`critical`. It names a channel, audience, and `content_ref`; it must not include
discount amounts, currencies, payment counterparties, or an instruction to send.

## Procedure

1. Qualify the packet before scoring. Refuse when `usage_signals.trend` or
   `usage_signals.mau_pct_change` is missing.
2. Refuse contradictory evidence, such as strong usage decline paired with a
   payment snapshot that explicitly marks no renewal risk and no late payment.
3. Normalize the numeric signals:
   - usage trend and `mau_pct_change`;
   - support volume and average severity;
   - days late and churn flag.
4. Fuse the score with visible weights:
   - usage trend;
   - support;
   - payment.
5. Map the score to a risk level. Low and moderate risk produce no `save_plan`.
6. For high or critical risk, include one bounded `save_plan` that names the
   channel, audience, and a content reference for a human-approved message.
7. Route moderate, edge-case, contradictory, or incomplete accounts to human
   review without authorizing a downstream send-as run.
8. Record that the verdict is a recommendation only and that delivery requires a
   separate governed send-as run under human approval.

## Stop Conditions

- Missing usage trend data.
- Missing support or payment evidence needed for the requested judgment.
- Contradictory signals that cannot be resolved from the input.
- Request to send, discount, quote, change billing, or touch money.
- Request to invent usage decline, payment lateness, churn, or customer facts.
- Private credentials, raw payment details, or unnecessary personal data in the
  input.

## Harness Cases

- `high_risk_with_save_play`: usage decline, high support volume, severe tickets,
  and late payment produce a sealed high-risk verdict with one bounded
  save-plan recommendation.
- `missing_usage_signals_stop`: missing usage signals block the qualify step, no
  save plan is emitted, and the reason names `usage_signals`.

## Example

Input:

```json
{
  "account_ref": "acct_renewal_042",
  "usage_signals": {"trend": "declining", "mau_pct_change": -32},
  "support_history": {"volume": 9, "ticket_severity_avg": 4.2},
  "payment_snapshot": {"days_late": 8, "churn_flag": true}
}
```

Expected result:

- `risk_level: high`
- visible fused weights for usage, support, and payment
- `save_plan.channel: email`
- `save_plan.audience: account_owner`
- `receipt_notes.sends_message: false`
