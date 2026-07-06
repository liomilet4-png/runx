# Frantic #76 Meeting Followup

- Package: `liomilet4-png/meeting-followup@sha-408dfab19c54`.
- Public URL: `https://runx.ai/x/liomilet4-png/meeting-followup@sha-408dfab19c54`.
- PR URL: `https://github.com/runxhq/runx/pull/252`.
- Source path: `skills/meeting-followup` on `liomilet4-png:codex/frantic-meeting-followup`.
- Raw profile: `https://raw.githubusercontent.com/liomilet4-png/runx/codex/frantic-meeting-followup/skills/meeting-followup/X.yaml`.
- Raw skill: `https://raw.githubusercontent.com/liomilet4-png/runx/codex/frantic-meeting-followup/skills/meeting-followup/SKILL.md`.
- CLI used for Linux evidence: `runx-cli 0.6.15`.
- Linux evidence run: `https://github.com/liomilet4-png/runx/actions/runs/28762624754`.
- Local harness on Linux passed both cases: `product_sync_followup` and `missing_transcript_stop`.
- Clean install was checked with `runx add liomilet4-png/meeting-followup@sha-408dfab19c54 --registry https://api.runx.ai`.
- Dogfood used the published registry package and the product-sync transcript fixture.
- Dogfood output includes two decisions, three action items, and three approval-gated `n8n-handoff` task proposals.
- The missing transcript case refuses with `needs_agent` and no live task creation.
- The skill does not send messages, create tasks, call n8n, edit calendars, or infer missing commitments.
- Verification JSON records `valid=true`, `signature.status=valid`, and receipt id `sha256:76d372df1520ea91c24f8048006c3e8699be36a1a301b161dd28ef227925d7a2`.
- New users can install with `runx add liomilet4-png/meeting-followup@sha-408dfab19c54 --registry https://api.runx.ai`, run with `runx skill liomilet4-png/meeting-followup@sha-408dfab19c54 --registry https://api.runx.ai --json`, and inspect the verifier result in `harness-evidence/verification.json`.
