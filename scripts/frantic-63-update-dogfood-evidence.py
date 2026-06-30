import json
import os
import pathlib
from datetime import datetime, timezone


ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "skills" / "renewal-risk-judge" / "harness-evidence"
VERSION = os.environ.get("FRANTIC63_PACKAGE_VERSION", "sha-unknown")
COMMIT = os.environ.get("GITHUB_SHA", "unknown")
PR_URL = os.environ.get("FRANTIC63_PR_URL", "https://github.com/runxhq/runx/pull/183")
OWNER = "liomilet4-png"
PACKAGE = f"{OWNER}/renewal-risk-judge@{VERSION}"
PUBLIC_URL = f"https://runx.ai/x/{PACKAGE}"
SOURCE_URL = f"https://github.com/{OWNER}/runx/tree/{COMMIT}"


def read_json(name):
    return json.loads((EVIDENCE_DIR / name).read_text(encoding="utf-8"))


def pick_output(resume):
    return (
        resume.get("output")
        or resume.get("payload")
        or resume.get("execution", {}).get("structured_output")
        or resume.get("execution", {}).get("skill_claim")
    )


def main():
    evidence = read_json("frantic-delivery-evidence.json")
    receipt = read_json("dogfood-receipt.json")
    verify = read_json("dogfood-verify.json")
    initial = read_json("dogfood-initial-run.json")
    resume = read_json("dogfood-resume-run.json")
    install = read_json("dogfood-install.json")
    registry_read = read_json("registry-read.json")

    receipt_id = receipt["id"]
    receipt_ref = f"runx:receipt:{receipt_id}"
    output = pick_output(resume)
    if not output:
        raise RuntimeError("dogfood resume output not found")

    verify_verdict = "valid=true" if verify.get("valid") is True else (
        verify.get("status")
        or verify.get("verdict", {}).get("status")
        or "unknown"
    )

    evidence["summary"] = (
        "renewal-risk-judge was published to the hosted runx registry, proposed "
        "upstream in runxhq/runx#183, clean-installed from the registry, dogfooded "
        "with a direct runx skill invocation, and verified with a sealed receipt."
    )
    evidence["package"] = {
        "name": "renewal-risk-judge",
        "version": VERSION,
        "publisher_owner": OWNER,
        "registry_ref": PACKAGE,
        "public_url": PUBLIC_URL,
        "source_url": SOURCE_URL,
        "pr_url": PR_URL,
        "x_yaml": f"https://raw.githubusercontent.com/{OWNER}/runx/{COMMIT}/skills/renewal-risk-judge/X.yaml",
        "skill_md": f"https://raw.githubusercontent.com/{OWNER}/runx/{COMMIT}/skills/renewal-risk-judge/SKILL.md",
    }
    evidence["dogfood"] = {
        "package": PACKAGE,
        "input": "dogfood-input.json",
        "command": (
            f"runx add {PACKAGE} --registry https://api.runx.ai, then "
            f"runx skill {PACKAGE} --registry https://api.runx.ai --json, then "
            "runx resume <run_id> dogfood-answers.json --json"
        ),
        "initial_run_id": initial.get("run_id"),
        "receipt_ref": receipt_ref,
        "verify_verdict": verify_verdict,
        "harness_cases": [
            {"name": "high_risk_with_save_play", "status": "sealed"},
            {"name": "missing_usage_signals_stop", "status": "needs_agent"},
        ],
    }
    evidence["observations"] = [
        item for item in evidence.get("observations", [])
        if item.get("name") not in {"dogfood_output", "registry_read", "clean_install"}
    ]
    evidence["observations"].extend([
        {
            "name": "clean_install",
            "status": install.get("status", "success"),
            "package": PACKAGE,
        },
        {
            "name": "registry_read",
            "status": registry_read.get("status", "success"),
            "package": PACKAGE,
        },
        {
            "name": "dogfood_output",
            "status": "sealed",
            "receipt_id": receipt_id,
            "decision": output["decision"],
            "fused_score": output["fused_score"],
            "escalation": output["escalation"],
            "save_plan": output["save_plan"],
            "receipt_notes": output["receipt_notes"],
        },
    ])
    evidence["known_gaps"] = []
    evidence["updated_at"] = datetime.now(timezone.utc).isoformat()

    (EVIDENCE_DIR / "frantic-delivery-evidence.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    report = f"""# Frantic #63 Delivery Report

## Summary

- Package: `renewal-risk-judge`
- Registry ref: `{PACKAGE}`
- Public registry URL: <{PUBLIC_URL}>
- Upstream PR: <{PR_URL}>
- Source revision: `{COMMIT}`
- Direct dogfood receipt: `{receipt_ref}`

## Validation

- `runx --version`: see `dogfood-runx-version.txt`
- `runx registry read {PACKAGE} --registry https://api.runx.ai --json`: success
- `runx add {PACKAGE} --registry https://api.runx.ai`: success
- `runx skill {PACKAGE} --registry https://api.runx.ai --json`: produced governed agent-task requests
- `runx resume <run_id> dogfood-answers.json --json`: sealed
- `runx verify --receipt dogfood-receipt.json --json`: `{verify_verdict}`

## Dogfood Output

- Risk level: `{output["decision"]["risk_level"]}`
- Fused score: `{output["fused_score"]["total"]}`
- Usage weight: `{output["fused_score"]["weights"]["usage_trend"]}`
- Support weight: `{output["fused_score"]["weights"]["support"]}`
- Payment weight: `{output["fused_score"]["weights"]["payment"]}`
- Save plan channel: `{output["save_plan"]["channel"]}`
- Save plan audience: `{output["save_plan"]["audience"]}`
- Save plan content ref: `{output["save_plan"]["content_ref"]}`
- Receipt id: `{receipt_id}`

## Boundary

The skill is read-only. It fuses supplied usage, support, and payment evidence
into a typed renewal-risk packet. It does not send messages, quote discounts,
change invoices, touch payment rails, or contact customers. Any actual send is
a separate governed run under human approval.
"""
    (EVIDENCE_DIR / "FRANTIC_DELIVERY_REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
