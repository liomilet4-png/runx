# Harness evidence

This directory stores non-secret local harness evidence for Frantic bounty #66.

Latest local source harness result: passed.

Command:

```powershell
cargo run --manifest-path crates\Cargo.toml -p runx-cli -- harness .\skills\flaky-test-judge --receipt-dir receipts_66_after_needs_agent_signed --json
```

Result summary:

- status: passed
- case_count: 2
- assertion_error_count: 0
- case_names: quarantine_justified, missing_run_history
- stop/error coverage: missing_run_history returns needs_agent

Notes:

- Receipt IDs remain canonical `sha256:<digest>` values.
- On Windows the receipt store writes safe filenames as `sha256-<digest>.json`.
- This folder intentionally excludes receipt JSON files and signing material.
- Do not place secrets, agent tokens, cookies, private keys, or payment data here.

## Post-publish evidence

- `evidence.json`: public package, harness, clean inspect, dogfood, and verification summary.
- `verification.json`: machine-readable verification verdict summary.
- `report.md`: human-readable evidence report for Frantic bounty #66.