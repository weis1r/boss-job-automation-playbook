# Workflows

## New Job Flow

1. Search adapter returns raw jobs.
2. Identity layer computes stable IDs.
3. State merge classifies jobs as:
   - `new`
   - `improved`
   - `existing`
4. Planner picks greetable jobs.
5. Greeter attempts outreach.
6. Success writes `greeted_at`.
7. Platform rejection writes `greet_blocked_*`.

## Recruiter Reply Flow

1. Reply poller sees a new recruiter message.
2. Match the reply back to a `stable_id`.
3. Skip if:
   - job was never greeted
   - reply fingerprint already processed
   - resume already sent
4. Generate tailored resume bundle.
5. Generate reply draft.
6. Attempt browser send.
7. If success:
   - write `resume_sent_at`
   - write `resume_send_status=sent`
8. If failure:
   - write `resume_send_status=manual_fallback`
   - notify operator

## Backlog Greet Flow

You may optionally include backlog jobs that were previously discovered but never greeted.

Guardrails:

- keep a per-scan limit
- exclude blocked jobs
- exclude already greeted jobs
- summarize in batch instead of one notification per job
