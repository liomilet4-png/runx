---
name: flaky-test-judge
description: Decide whether a supplied flaky-test history justifies a temporary quarantine packet, an ignore decision, or a stop for more evidence.
runx:
  category: testing
---

# Flaky Test Judge

Use this skill when a release owner has run history for one test and needs a
read-only quarantine decision. The skill reads supplied test-run history,
metadata, and a release policy. It computes the pass-rate, identifies failure
modes from the supplied logs, and returns a typed disposition.

The skill never edits a repository, disables a test, opens an issue, creates a
pull request, or fires another run. When quarantine is justified it emits a
bounded `runx.flaky.test_triage.v1` packet that names the downstream
`issue-to-pr` inputs. A separate governed issue-to-pr run drafts the change, and
the human merge gate on that draft is the only path to a live disable.

## Inputs

- `test_run_history.sample_size`: number of runs considered.
- `test_run_history.runs[]`: each run has `status`, `duration`, and `logs`.
- `test_metadata.test_path`: exact test path or test id.
- `test_metadata.suite`: owning test suite.
- `test_metadata.tags[]`: supplied tags such as `e2e`, `payment`, or
  `quarantine-candidate`.
- `release_policy.flake_threshold_pct`: minimum pass-rate required to avoid a
  quarantine decision.
- `release_policy.min_sample_size`: minimum run count before a quarantine
  decision is allowed.
- `release_policy.max_quarantine_days`: upper bound for any temporary quarantine.

## Output

The default runner returns a `runx.flaky.test_triage.v1` packet with:

- `disposition.decision`: `quarantine`, `ignore`, `fix_now`, or `refuse`.
- `disposition.confidence`: confidence derived from sample size and failure-mode
  concentration.
- `disposition.reason`: cites the pass-rate, run count, policy threshold, and
  observed failure modes.
- `quarantine_packet`: contains the bounded quarantine details when quarantine is justified; otherwise it is an explicit `{ present: false, reason: ... }` object. When present, it includes
  `test_path`, `duration_days`, `fix_template`, and `exclusion_marker`.
- `dispatch_target`: names the offline downstream `issue-to-pr` lane when quarantine is justified; otherwise it is an explicit `{ present: false, reason: ... }` object. For quarantine decisions it names the
  offline downstream `issue-to-pr` lane.
- `escalation`: the human or evidence lane that should handle the decision.

## Decision Rules

- Refuse when no run history is provided.
- Refuse when `sample_size` is below `release_policy.min_sample_size`.
- Do not quarantine a test passing at or above `release_policy.flake_threshold_pct`.
- Never exceed `release_policy.max_quarantine_days`.
- Never invent a failure mode absent from the supplied logs.
- Treat near-threshold or mixed failure evidence as a human review lane, not an
  automatic quarantine packet.
- Route quarantine packets by naming `issue-to-pr` typed inputs only; do not
  consume the packet as an effect inside this skill.

## Harness Cases

- `quarantine_justified`: a 20-run history with a 65% pass-rate, 7 failures, and
  timeouts in 6 of those failures against a 70% policy threshold. Expected
  disposition is `quarantine`; the packet is bounded to 7 days and routes to
  `issue-to-pr` behind a human merge gate.
- `missing_run_history`: no run history and sample size 0. Expected disposition
  is `refuse` with a missing-evidence stop reason and explicit non-present quarantine and dispatch objects.

## Quality Profile

- Purpose: produce one bounded, read-only flaky-test quarantine judgment.
- Audience: release owners deciding whether to quarantine or investigate a test.
- Evidence bar: every decision cites supplied run count, pass-rate, policy, and
  failure-mode evidence.
- Safety bar: no repository mutation, no live disable, no PR creation, no
  authority mint, and no operational proposal.
- Stop conditions: missing history, undersized sample, contradictory evidence,
  or policy fields that are absent.
