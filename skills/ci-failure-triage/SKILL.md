---
name: ci-failure-triage
description: Classify CI failures as flake, infra, real-break, or dependency break and emit an evidence-backed routing packet.
runx:
  category: code
---

# CI Failure Triage

Classify a CI failure before an incident lane opens. This skill reads the
provided CI logs, commit context, repository state, and escalation policy. It
returns a typed `runx.ci.triage.v1` packet for a downstream issue-intake,
issue-to-pr, or pr-review-note run.

The skill is read-only. It does not rerun CI, open issues, page operators,
modify repositories, or claim that any downstream lane has consumed its output.
It only emits a classification and a draft routing decision when the supplied
evidence supports one.

## Verdicts

- `flake`: transient failure evidence with a read-only rerun verdict.
- `infra`: runner, network, cache, service, or platform failure with a read-only
  operator-page note.
- `real-break`: source or test change likely caused a deterministic failure,
  routed to `issue-to-pr`.
- `dep`: dependency, lockfile, registry, or toolchain drift, routed to
  `issue-to-pr` unless the repository policy names another lane.
- `needs_agent`: ambiguous or truncated evidence, contradictory signals, or
  confidence below `escalation_policy.min_confidence`.

## Inputs

- `ci_failure.logs`: raw or summarized CI logs.
- `ci_failure.commit`: commit SHA, changed files, and commit message.
- `ci_failure.repo_state`: workflow, provider, baseline status, retry evidence,
  or known incident context.
- `repo_config`: optional repository routing rules and protected branch policy.
- `escalation_policy.min_confidence`: minimum confidence required before any
  recommendation is emitted.

## Output

The default runner returns:

- `classification.verdict`: one of `flake`, `infra`, `real-break`, `dep`, or
  `needs_agent`.
- `classification.confidence`: numeric confidence in the supplied evidence.
- `classification.evidence_refs`: exact log, commit, or repo-state references
  supporting the verdict.
- `triage_packet`: exactly one of `read_only_rerun_verdict`,
  `read_only_operator_page_note`, or
  `routing_decision{recommended_lane,rationale}` when confidence is high enough.
- `operator_note`: the human-readable next step and boundaries.

For real-break or dependency failures, the routing decision names a downstream
issue-intake / issue-to-pr / pr-review-note run. That downstream run is a
separate governed step issued by an operator or venue driver.

## Refusal Rules

- Do not assert a root cause that is not visible in the supplied logs, commit,
  or repository state.
- Do not classify above `escalation_policy.min_confidence` without cited
  evidence.
- Do not invent a recommended lane when logs are truncated, signals conflict,
  the baseline is unknown, or the failure cannot be grounded.
- Do not open a tracking item, rerun CI, page anyone, or mutate any repository.
- Return `needs_agent` when a human needs to fetch full logs, inspect secrets,
  decide release priority, or approve a downstream lane.

## Harness Cases

- `real_break_clear_logs`: clear deterministic test failure after retry, tied to
  a changed source file. Expected verdict is `real-break` with recommended lane
  `issue-to-pr`.
- `ambiguous_truncated_logs`: truncated failure with no grounding evidence.
  Expected status is `needs_agent` and no routing packet.
