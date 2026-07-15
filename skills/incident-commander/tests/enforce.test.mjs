import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const testDir = mkdtempSync(join(tmpdir(), "incident-commander-enforce-"));
const runner = join(dirname(fileURLToPath(import.meta.url)), "..", "graph", "enforce", "RUNNER", "run.mjs");

const digest = `sha256:${"a".repeat(64)}`;
const receipt = `runx:receipt:sha256:${"b".repeat(64)}`;
const roster = [
  { role: "commander", principal: "incident:commander:alex", skill: "ops-desk", scope: ["incident.command"] },
  { role: "responder_lead", principal: "incident:responder:rio", skill: "incident-response", scope: ["incident.respond"] },
  { role: "comms_lead", principal: "incident:comms:morgan", skill: "send-as", scope: ["stakeholder.send"] },
];
const handoff = {
  skill: "send-as",
  runner: "plan",
  principal: "incident:comms:morgan",
  channel: "email",
  audience: { list_ref: "stakeholders:checkout-api", classification: "incident-stakeholders" },
  content_digest: digest,
};
const state = {
  status: "awaiting",
  turn: 4,
  severity: "SEV-2",
  scope: "checkout-api",
  declared: true,
  pending_escalation: {
    status: "awaiting_approval",
    lane: "human:incident-reviewer",
    proposed_handoff: handoff,
  },
};
const priorTurn = {
  status: "awaiting_approval",
  case_id: "inc-sev2-checkout",
  turn: 4,
  named_run: { skill: "send-as", runner: "plan", executable: false, data: handoff },
};
const decision = {
  decision: "dispatch",
  reason: "Roster-matched approval permits the bounded handoff.",
  dispatch: {
    member: "comms_lead",
    skill: "send-as",
    task: "Plan the approved stakeholder update.",
    needed_scope: ["stakeholder.send"],
    consequence: "stakeholder_send_handoff",
    verification: {
      expected_receipt: "runx.receipt.v1",
      readback: "Link the later send-as receipt before recording delivery.",
    },
  },
};

function run(name, overrides = {}) {
  const inputs = {
    case_id: "inc-sev2-checkout",
    driver_id: "driver-primary",
    incident_objective: "send",
    case_state: state,
    roster,
    approval: null,
    member_result: null,
    decision,
    prior_turn: priorTurn,
    ...overrides,
  };
  const inputPath = join(testDir, `${name}.json`);
  writeFileSync(inputPath, `${JSON.stringify(inputs)}\n`, "utf8");
  const result = spawnSync(process.execPath, [runner], {
    encoding: "utf8",
    env: { ...process.env, RUNX_INPUTS_PATH: inputPath },
  });
  assert.equal(result.status, 0, `${name}: ${result.stderr || result.stdout}`);
  return JSON.parse(result.stdout).incident_turn;
}

try {
  const waiting = run("missing-approval");
  assert.equal(waiting.status, "awaiting_approval");
  assert.equal(waiting.named_run.executable, false);

  const approved = run("approved", {
    approval: { principal: "incident:comms:morgan", reason: "Approved reviewed digest." },
  });
  assert.equal(approved.status, "advanced");
  assert.equal(approved.named_run.executable, true);
  assert.equal(approved.delivery_receipt_ref, null);

  const forgedDelivery = run("forged-delivery", {
    approval: { principal: "incident:comms:morgan", reason: "Approved reviewed digest." },
    member_result: { outcome: "delivered", receipt_ref: "not-a-runx-receipt" },
  });
  assert.equal(forgedDelivery.status, "refused");

  const delivered = run("receipt-backed-delivery", {
    approval: { principal: "incident:comms:morgan", reason: "Approved reviewed digest." },
    member_result: { outcome: "delivered", receipt_ref: receipt },
  });
  assert.equal(delivered.status, "advanced");
  assert.equal(delivered.delivery_receipt_ref, receipt);

  const missingOwner = run("missing-owner", {
    incident_objective: "assign",
    case_state: { status: "working", turn: 1, severity: "SEV-3", scope: "search-api", declared: true, named_owner: null },
  });
  assert.equal(missingOwner.status, "needs_agent");

  const scopeEscalation = run("scope-escalation", {
    approval: { principal: "incident:comms:morgan", reason: "Approved reviewed digest." },
    decision: {
      ...decision,
      dispatch: { ...decision.dispatch, needed_scope: ["stakeholder.send", "admin.write"] },
    },
  });
  assert.equal(scopeEscalation.status, "refused");

  console.log(JSON.stringify({ status: "passed", case_count: 6 }, null, 2));
} finally {
  rmSync(testDir, { recursive: true, force: true });
}
