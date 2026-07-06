---
name: meeting-followup
description: Turn a bounded meeting transcript and attendee list into decisions, owners, dates, and gated n8n task proposals without inventing missing facts.
runx:
  category: ops
---

# Meeting Followup

Use this skill when an operator has a meeting transcript plus an attendee list
and needs a read-only follow-up packet. The skill extracts a concise summary,
decisions, owned action items, and optional gated `task_proposals` that a
separate `n8n-handoff` run may dispatch after approval.

The skill never creates tasks, sends messages, edits calendars, opens tickets,
or calls n8n. It only emits a bounded `runx.meeting.followup.v1` packet that
names the downstream handoff lane when the transcript contains enough evidence.

## Inputs

- `meeting.id`: stable meeting identifier.
- `meeting.title`: human-readable meeting title.
- `meeting.date`: ISO date for the meeting.
- `transcript.source_path`: fixture path or source label for the transcript.
- `transcript.text`: bounded transcript text.
- `attendees[]`: supplied people with `name`, `role`, and optional `email`.
- `followup_policy.allowed_task_targets[]`: downstream targets the packet may
  name, such as `n8n-handoff`.
- `followup_policy.default_timezone`: timezone used only when dates are already
  present in the transcript or meeting metadata.

## Output

The default runner returns:

- `summary`: concise factual summary of what was discussed.
- `decisions[]`: decisions explicitly stated in the transcript, with evidence.
- `action_items[]`: owned follow-up items with owner, due date or null, and
  evidence. Missing owners or dates stay null; the skill does not guess.
- `task_proposals[]`: gated proposals for downstream `n8n-handoff`. Each
  proposal includes target, title, owner, due date, evidence, and
  `requires_approval: true`.
- `escalation`: stop or review lane when transcript evidence is missing.

## Decision Rules

- Refuse when the transcript text is missing or empty.
- Refuse when the attendee list is missing.
- Never invent an owner, decision, due date, or task from context alone.
- Do not emit a `task_proposal` unless the owner and action are both explicit.
- Do not emit any proposal for a target absent from
  `followup_policy.allowed_task_targets`.
- Treat ambiguous dates as null and explain the ambiguity in the item evidence.
- Keep all task proposals approval-gated; this skill is not allowed to create or
  send tasks directly.

## Harness Cases

- `product_sync_followup`: a fixture transcript for a product sync contains two
  decisions and three action items. Expected status is sealed, with three
  approval-gated task proposals for `n8n-handoff`.
- `missing_transcript_stop`: the attendee list is supplied but transcript text is
  empty. Expected status is `needs_agent`, with no decisions, action items, or
  task proposals.

## Quality Profile

- Purpose: produce a source-grounded, read-only meeting follow-up packet.
- Audience: operators and teams that need auditable follow-up extraction before
  a separate automation step.
- Evidence bar: every decision and action item cites transcript wording or line
  evidence supplied in the input.
- Safety bar: no external calls, no task creation, no email, no calendar edits,
  no n8n webhook send, and no inferred commitments.
- Stop conditions: missing transcript, missing attendees, unsupported target, or
  transcript evidence that does not bind action and owner.
