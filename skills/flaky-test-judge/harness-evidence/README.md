# Harness evidence

This directory stores non-secret local harness evidence for Frantic bounty #66.

Latest local source harness result: passed.

Command:

```powershell
cargo run --manifest-path crates\Cargo.toml -p runx-cli -- harness .\skills\flaky-test-judge --receipt-dir receipts_66_final_verify --json
```

Result summary:

- status: passed
- case_count: 2
- assertion_error_count: 0
- case_names: quarantine_justified, missing_run_history

Notes:

- Receipt IDs remain canonical `sha256:<digest>` values.
- On Windows the receipt store writes safe filenames as `sha256-<digest>.json`.
- This folder intentionally excludes receipt JSON files and signing material.
- Do not place secrets, agent tokens, cookies, private keys, or payment data here.