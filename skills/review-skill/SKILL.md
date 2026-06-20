---
name: review-skill
description: Assess a skill package for capability, trust, and operator readiness.
runx:
  category: authoring
---

# Review Skill

Judge whether a skill is ready to trust, adopt, or publish.

This skill evaluates one bounded capability. It should identify what the skill
does well, where it is incomplete, what evidence supports the trust level, and
what tests or governance gaps block adoption.

Avoid generic praise. The output should help an operator decide whether to
adopt, publish, sandbox, or reject the skill.

## Quality Profile

- Purpose: decide whether a bounded skill package is trustworthy and useful
  enough for adoption, publication, sandboxing, or rejection.
- Audience: operators and maintainers responsible for capability trust.
- Artifact contract: capability profile, trust assessment, test matrix, and
  recommendation report.
- Evidence bar: base trust on the skill contract, execution profile, fixtures,
  receipts, source notes, and known failure evidence. Do not infer trust from
  a confident README alone.
- Voice bar: direct review notes with concrete blockers and residual risk. No
  generic praise, marketing language, or "looks good" summaries.
- Strategic bar: explain whether the skill strengthens the catalog, fills a
  real operator need, duplicates existing capability, or carries unacceptable
  trust risk.
- Public value bar: a skill is not publication-ready merely because it parses or
  runs once. It should solve a real operator or user problem, be something the
  catalog would stand behind, and produce evidence a stranger can verify. A
  wrapper, placeholder, toy, or copied example with no credible adoption path is
  a reject or sandbox-only recommendation.
- Stop conditions: return `needs_more_evidence` when receipts or harness proof
  are missing, and `reject` when the skill cannot be bounded or audited.

## Review Gates

Check these before recommending adoption or publication:

- The `SKILL.md` states a bounded capability and does not promise more than the
  execution profile implements.
- The execution profile declares typed inputs, outputs, side-effect posture,
  allowed refs/tools, authority or approval posture, receipt mapping when a
  domain act occurs, and harness cases.
- At least one meaningful happy path and one error or stop path are covered by
  harness evidence or receipts. Local assertions without captured output are not
  enough.
- Any published URL, registry listing, docs site, or repo is durable and public.
  Placeholder hosts, private previews, unrelated parent domains, and dead links
  lower trust or block publication.
- The evidence pack contains no secrets, private tokens, customer data, private
  inbox content, or provider dumps.
- The recommendation states who would use or trust the skill and why. If that
  answer is weak, recommend rejection, sandboxing, or a narrower redesign.

## Output

- `capability_profile`: what the skill appears to do and how it executes.
- `trust_assessment`: trust tier, caveats, and missing evidence.
- `test_matrix`: concrete checks the skill should pass.
- `recommendation_report`: adoption or publication recommendation.

## Inputs

- `skill_ref` (required): skill package path, registry id, or marketplace id.
- `objective` (optional): what the operator wants to know about this skill.
- `evidence_pack` (optional): receipts, docs, harness output, or source notes.
- `test_constraints` (optional): time, environment, or safety limits.
