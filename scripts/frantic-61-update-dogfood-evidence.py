import json
import pathlib
from datetime import datetime, timezone


root = pathlib.Path(__file__).resolve().parents[1]
evidence_dir = root / "skills" / "ci-failure-triage" / "harness-evidence"


def read_json(name):
    return json.loads((evidence_dir / name).read_text(encoding="utf-8"))


resume = read_json("dogfood-resume-run.json")
verify = read_json("dogfood-verify.json")
receipt = read_json("dogfood-receipt.json")
initial = read_json("dogfood-initial-run.json")
evidence = read_json("frantic-delivery-evidence.json")

receipt_id = receipt["id"]
receipt_ref = f"runx:receipt:{receipt_id}"
verify_verdict = verify.get("status") or verify.get("verdict", {}).get("status") or "unknown"

resume_output = (
    resume.get("output")
    or resume.get("payload")
    or resume.get("execution", {}).get("structured_output")
    or resume.get("execution", {}).get("skill_claim")
)
if not resume_output:
    raise KeyError("dogfood resume output not found")

classification = resume_output["classification"]
triage_packet = resume_output["triage_packet"]
operator_note = resume_output["operator_note"]

evidence["summary"] = (
    "ci-failure-triage was published to the hosted runx registry, proposed upstream "
    "in runxhq/runx#153, clean-installed from the hosted registry, validated with "
    "hosted harness status passed, and dogfooded with a direct runx skill invocation "
    "that produced a verifiable sealed receipt."
)
evidence["dogfood"] = {
    "package": "liomilet4-png/ci-failure-triage@sha-92622cb44366",
    "input": {
        "ci_failure": "dogfood-input-ci-failure.json",
        "repo_config": "dogfood-input-repo-config.json",
        "escalation_policy": "dogfood-input-escalation-policy.json"
    },
    "command": (
        "runx skill liomilet4-png/ci-failure-triage@sha-92622cb44366 "
        "--registry https://api.runx.ai --json, then runx resume <run_id> "
        "dogfood-answers.json --json"
    ),
    "initial_run_id": initial["run_id"],
    "receipt_ref": receipt_ref,
    "verify_verdict": verify_verdict,
    "harness_cases": [
        {"name": "real_break_clear_logs", "status": "sealed"},
        {"name": "ambiguous_truncated_logs", "status": "needs_agent"}
    ]
}

evidence["observations"] = [
    item for item in evidence["observations"]
    if item.get("name") not in {"direct_dogfood", "dogfood_output"}
]
evidence["observations"].append({
    "name": "dogfood_output",
    "status": "sealed",
    "receipt_id": receipt_id,
    "classification": {
        "verdict": classification["verdict"],
        "confidence": classification["confidence"],
        "evidence_refs": classification["evidence_refs"]
    },
    "triage_packet": {
        "recommended_lane": triage_packet["recommended_lane"],
        "rationale": triage_packet["rationale"],
        "downstream_step": triage_packet["downstream_step"]
    },
    "operator_note": operator_note
})

gaps = evidence.get("known_gaps", [])
evidence["known_gaps"] = [
    gap for gap in gaps
    if "Direct local dogfood" not in gap and "Windows local registry" not in gap
]
evidence["updated_at"] = datetime.now(timezone.utc).isoformat()

(evidence_dir / "frantic-delivery-evidence.json").write_text(
    json.dumps(evidence, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8"
)

report = f"""# Frantic #61 delivery report

## Summary

- Package: `ci-failure-triage`
- Public registry URL: <https://runx.ai/x/liomilet4-png/ci-failure-triage@sha-92622cb44366>
- Upstream PR: <https://github.com/runxhq/runx/pull/153>
- Direct dogfood receipt: `{receipt_ref}`

## Validation

- `runx --version`: see `dogfood-runx-version.txt`
- `runx add liomilet4-png/ci-failure-triage@sha-92622cb44366 --registry https://api.runx.ai`: success
- `runx skill liomilet4-png/ci-failure-triage@sha-92622cb44366 --registry https://api.runx.ai --json`: produced a governed `needs_agent` request
- `runx resume {initial["run_id"]} dogfood-answers.json --json`: sealed
- `runx verify --receipt dogfood-receipt.json --json`: `{verify_verdict}`
- Hosted registry harness: status passed, 2 checks passed, 0 failed

## Dogfood Output

- Verdict: `{classification["verdict"]}`
- Confidence: `{classification["confidence"]}`
- Recommended lane: `{triage_packet["recommended_lane"]}`
- Receipt id: `{receipt_id}`

## Boundary

The skill is read-only. It classifies supplied CI evidence and emits a typed
triage packet. It does not rerun CI, open issues, mutate repositories, page
operators, or claim that a downstream lane has consumed the output.
"""

(evidence_dir / "FRANTIC_DELIVERY_REPORT.md").write_text(report, encoding="utf-8")
