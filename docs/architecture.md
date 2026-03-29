# Architecture

## Objective

Build a safe automation loop for job discovery and outreach without repeatedly contacting the same role or silently losing recruiter replies.

## Recommended Modules

- `search adapter`
  - wraps `boss-cli` or another search source
  - returns normalized job dictionaries
- `identity / dedupe`
  - computes stable job IDs
  - merges listings that rotate `security_id`
- `state store`
  - tracks greet, reply, block, and resume-send lifecycle
- `resume renderer`
  - generates per-job resume bundles
- `chat sender`
  - sends reply text and uploads attachment
- `notifier`
  - pushes summaries or fallback alerts

## Key State Fields

- `stable_id`
- `security_id`
- `canonical_source_url`
- `first_seen_at`
- `last_seen_at`
- `greeted_at`
- `greet_blocked_at`
- `greet_blocked_code`
- `reply_last_fingerprint`
- `resume_sent_at`
- `resume_send_status`
- `resume_send_error`

## Recommended Lifecycle

1. Poll jobs for several cities / keywords.
2. Normalize listings.
3. Compute stable IDs.
4. Merge into state.
5. Greet only records that pass `can_auto_greet`.
6. Watch recruiter replies.
7. On the first new reply after greeting:
   - build tailored resume
   - build reply draft
   - send once
8. If the platform returns `code=1` on greeting:
   - mark the record blocked
   - remove it from future auto-greet plans
   - do not retry unless manually reset

## Failure Strategy

- login invalid
  - pause automated actions
  - alert operator
- browser send fails
  - generate files
  - push fallback summary to a notifier
  - mark `resume_send_status=manual_fallback`
- recruiter replies again after a successful send
  - do not resend resume automatically
