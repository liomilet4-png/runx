---
name: spam-risk-reviewer
description: Review supplied campaign, list hygiene, and sender authentication signals before a send-as preflight can clear.
runx:
  category: deliverability
---

# Spam Risk Reviewer

Use this skill when a campaign owner needs a read-only deliverability gate before
a separate governed `send-as` run can send anything. The skill reads only the
provided campaign draft, subscriber list metadata, and sender authentication
posture. It returns a bounded `send_risk_verdict`.

This skill never sends a message, never mints authority, never reads live DNS or
domain state, and never emits `runx.operational_proposal.v1`. The public send
effect belongs to `send-as`, not this reviewer. A non-clear verdict blocks
`send-as` preflight and routes the case to human approval.

## Inputs

- `campaign_draft.from`: sender address or sender identity supplied by the
  caller.
- `campaign_draft.subject`: proposed subject line.
- `campaign_draft.content_digest`: short summary of the message content and
  consent context.
- `list_metadata.size`: recipient count.
- `list_metadata.bounce_rate`: recent or expected bounce rate as a decimal.
- `list_metadata.complaint_rate`: recent complaint rate as a decimal.
- `list_metadata.freshness`: supplied freshness signal for the audience.
- `sender_auth_posture.spf_pass`: whether SPF passes.
- `sender_auth_posture.dkim_pass`: whether DKIM passes.
- `sender_auth_posture.dmarc_pass`: whether DMARC passes.
- `sender_auth_posture.warm_up_days`: number of warm-up days for the sender.

## Output

The default runner returns:

- `send_risk_verdict.risk_level`: `pass`, `hold`, or `refuse`.
- `send_risk_verdict.preflight_clear`: boolean; true only when the send-as
  preflight may continue.
- `send_risk_verdict.blockers[]`: concrete reasons when the preflight must stop.
- `send_risk_verdict.evidence_summary`: supplied facts and thresholds used.

## Decision Rules

- Refuse to set `preflight_clear` true when SPF, DKIM, or DMARC do not pass.
- Refuse to clear preflight when bounce rate exceeds 0.02.
- Refuse to clear preflight when complaint rate exceeds 0.001.
- Treat unknown or stale list freshness as a blocker.
- Treat sender warm-up below 14 days as a blocker.
- Never invent authentication, consent, freshness, bounce, or complaint signals
  that are not present in the input.
- Route borderline, missing, or high-risk cases to the `send-as` human approval
  lane. The actual delivery remains a separate governed `send-as` run.

## Harness Cases

- `low-risk-verified-sender`: full SPF, DKIM, and DMARC pass; list hygiene is
  inside policy; warm-up is mature. Expected verdict is `pass` with
  `preflight_clear: true` and no blockers.
- `high-risk-incomplete-auth-poor-list`: DKIM fails and list metrics exceed
  policy. Expected verdict is `hold`, `preflight_clear: false`, blockers naming
  each risk, and escalation to human approval.
- `missing-authentication-stop`: authentication and list hygiene are not
  sufficiently supplied. Expected status is `needs_agent`, proving the reviewer
  stops instead of inventing signals.

## Quality Profile

- Purpose: make one bounded deliverability risk judgment before send-as.
- Audience: operators using send-as preflight and human approval gates.
- Evidence bar: cite only supplied authentication and list hygiene metrics.
- Safety bar: no send effect, no live-domain lookup, no authority mint, no
  operational proposal, and no private data access.
