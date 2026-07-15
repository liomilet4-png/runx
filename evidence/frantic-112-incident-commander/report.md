# Incident commander publication and dogfood report

- **Package:** manifest version `0.1.1` was published as immutable registry ref `liomilet4-png/incident-commander@sha-af08d8fac7af` under the exact `incident-commander` name with digest `sha256:049b1f45b5fee3af58c91a7e0357cb8a5329a56356d2140795c5a2917804a4c2`.
- **CLI versions:** publication used `runx-cli 0.6.15`; clean install, registry dogfood, and receipt verification used `runx-cli 0.7.2`. Both are newer than the required `0.6.14` minimum.
- **Public surfaces:** the [registry listing](https://runx.ai/x/liomilet4-png/incident-commander), [source branch](https://github.com/liomilet4-png/runx/tree/codex/frantic-112-incident-commander/skills/incident-commander), and [runxhq/runx PR #330](https://github.com/runxhq/runx/pull/330) describe the same package.
- **Harness:** `runx harness ./skills/incident-commander --json` passed both inline cases with zero assertion errors. `incident-send-awaits-then-approves` sealed; `incident-assign-missing-owner` stopped as `needs_agent` without inventing an owner. The hosted registry accepted and published the same inline-harness package.
- **Approval gate:** a declared `SEV-2` checkout incident first returned `awaiting_approval` and a non-executable `send-as` plan bound to the stakeholder audience and content digest. After `incident:comms:morgan` matched the fixed `comms_lead` roster entry, the turn advanced and became executable without performing a provider send.
- **Dogfood:** a direct `runx skill liomilet4-png/incident-commander@sha-af08d8fac7af advance --registry https://api.runx.ai --json` run produced receipt `runx:receipt:sha256:698755f06556247d4e7226a42e2906e903df0d848d43fd5a1d76742d63f90025`.
- **Verification:** `runx verify --receipt sha256-698755f06556247d4e7226a42e2906e903df0d848d43fd5a1d76742d63f90025.json --json` completed with exit code `0`. The submitted receipt belongs to the incident-commander registry run, not the harness seal or downstream `send-as` plan.
- **Why install it:** operators can obtain a typed, replayable incident decision that stays inside a fixed commander/responder/comms roster, preserves the human approval lane, and names a governed communications handoff without claiming delivery.
- **Install:** `runx add liomilet4-png/incident-commander@sha-af08d8fac7af --registry https://api.runx.ai --json`.
- **Run:** `runx skill liomilet4-png/incident-commander@sha-af08d8fac7af advance --registry https://api.runx.ai --json` with a declared folded case state, fixed roster, objective, and optional approval/member result.
- **Verify:** locate the sealed receipt emitted by the run and execute `runx verify --receipt <receipt.json> --json`.
- **Safety boundary:** the skill does not persist agency state, mint authority, send messages, authenticate approvals, or invent roster members or resolution evidence. Provider delivery remains a separate governed run.

Machine-readable proof is in [`evidence.json`](./evidence.json), [`verification.json`](./verification.json), and [`harness-results.json`](./harness-results.json).
