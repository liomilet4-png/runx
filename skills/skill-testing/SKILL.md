---
name: skill-testing
description: Evaluate a skill, draft the trust audit, and package the approved recommendation.
runx:
  category: authoring
---

# Skill Testing

This graph is the public-facing trust-audit lane.

It evaluates one skill, turns the findings into a concise report, and then
packages the approved output for publication or operator handoff.

## Quality Profile

- Purpose: produce a reviewable trust audit for one skill.
- Audience: operators, catalog maintainers, and users deciding whether to trust
  or adopt the skill.
- Artifact contract: review-skill assessment, trust audit draft, approval
  decision, and publish or handoff packet.
- Evidence bar: base recommendations on receipts, harness output, source notes,
  and the skill contract. Missing evidence lowers trust; it does not invite
  optimistic language.
- Voice bar: audit report, not marketing copy. Name risks, caveats, and test
  gaps directly.
- Strategic bar: make adoption, sandboxing, rejection, or further testing
  easier.
- Public value bar: test whether the skill has a credible user, operator,
  maintainer, or catalog reason to exist. Passing harnesses do not rescue a
  placeholder, toy, duplicate, or low-value package.
- Stop conditions: stop at review when trust evidence is insufficient or the
  skill cannot be bounded.

## Trust Audit Checks

Before packaging a recommendation, confirm:

- The skill contract is bounded and matches the execution profile.
- The execution profile declares typed inputs and outputs, side-effect posture,
  allowed refs/tools, approval or authority posture, receipt mapping where
  relevant, and harness cases.
- Harness or receipt evidence covers a meaningful happy path and at least one
  stop or error path.
- Published artifacts are durable and public. Private previews, localhost,
  placeholder hosts, unrelated parent domains, or dead links block a publication
  recommendation.
- The audit names the concrete user-visible value: who would use, link, install,
  trust, or maintain the skill.
- The evidence pack contains no secrets, raw credentials, private customer data,
  private email bodies, wallet private keys, or provider response dumps.

## Inputs

- `skill_ref` (required): skill package or registry reference to assess.
- `objective` (optional): decision the audit should support.
- `channel` (optional): final report channel; defaults to `trust-audit`.
- `evidence_pack` (optional): receipts, docs, or source notes that should anchor
  the evaluation.
- `test_constraints` (optional): environment or safety limits for evaluation.
