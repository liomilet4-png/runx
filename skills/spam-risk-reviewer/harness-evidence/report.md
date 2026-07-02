# spam-risk-reviewer delivery report

## Summary

This delivery adds `spam-risk-reviewer`, a bounded read-only deliverability gate for
reviewing supplied campaign, list hygiene, and sender authentication signals
before a separate governed `send-as` run can continue.

The skill does not send messages, does not read live DNS or private domain state,
does not mint authority, and does not emit an operational proposal.

## Public artifacts

- Registry ref: `liomilet4-png/spam-risk-reviewer@sha-659d3bb2acbd`
- Registry page: <https://runx.ai/x/liomilet4-png/spam-risk-reviewer>
- PR: <https://github.com/runxhq/runx/pull/213>
- Source commit: `659d3bb2acbd8c7ba970fad8fb616086bd127d20`
- Skill source: <https://github.com/liomilet4-png/runx/tree/659d3bb2acbd8c7ba970fad8fb616086bd127d20/skills/spam-risk-reviewer>

## Harness coverage

The registry publish harness passed with three cases:

- `low-risk-verified-sender`
- `high-risk-incomplete-auth-poor-list`
- `missing-authentication-stop`

The third case verifies the required stop behavior when authentication and list
hygiene inputs are missing instead of inventing signals.

## Verification

- `runx registry read` using `@runxhq/cli@0.6.15`: passed.
- Clean install using `@runxhq/cli@0.6.15`: passed.
- Registry publish harness: passed, `case_count=3`, `assertion_error_count=0`.
- Dogfood with synthetic low-risk input: sealed with receipt
  `sha256:3fa99e0f7d51a886cac4e6611763d44e12e55a7d36500d766fcc17a01e5e53a7`.

## Windows note

The released Windows CLI `@runxhq/cli@0.6.15` can read the registry and cleanly
install the package. A follow-up `resume` on Windows currently hits the existing
receipt-store directory sync error (`os error 5`). This PR includes the minimal
runtime fix in `crates/runx-runtime/src/receipts/store.rs`: on Windows it skips
directory `fsync` while preserving receipt file `sync_all` and index rebuilds.

Using the PR-patched Windows CLI, the same dogfood flow seals successfully.

## Safety boundaries

- Synthetic fixture inputs only.
- No real recipient list, customer data, DNS lookup, or private service access.
- No `public_send` or equivalent send effect.
- The skill only returns `send_risk_verdict` and optional escalation guidance.
