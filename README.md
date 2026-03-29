# BOSS Job Automation Playbook

A sanitized, open-source playbook for building a BOSS-style job discovery and outreach pipeline.

This repository is distilled from a private automation system that handled:

- multi-keyword job polling
- stable deduplication across changing `security_id` / listing aliases
- job scoring and queueing
- auto-greet planning
- "first recruiter reply" detection
- tailored resume generation triggers
- platform rejection handling such as `code=1` no-retry blocking
- notification and browser-send handoff patterns

This repo does not include private assets or live account integrations:

- no personal resume content
- no WeChat account IDs
- no cookies or login state
- no absolute local paths
- no private OpenClaw runtime state

Instead, it provides a reusable reference architecture, data model, rules engine, and config examples so you can rebuild the automation safely in your own environment.

## What Is Included

- `src/boss_job_automation/`
  - stable job identity helpers
  - queue / greet planning logic
  - reply trigger rules
  - no-retry blocking for platform-rejected greetings
- `examples/`
  - example config
  - example candidate profile markdown
- `docs/`
  - architecture and workflow notes
- `tests/`
  - tests for the critical automation rules

## System Design

The original private system had four layers:

1. Search layer
   - polls multiple cities and keywords
   - normalizes raw listing payloads
2. Decision layer
   - computes a stable job ID
   - deduplicates repeated listings
   - scores and prioritizes openings
3. Action layer
   - greets real new jobs
   - watches for recruiter replies
   - generates a tailored resume package
   - sends the first-reply follow-up only once
4. Delivery layer
   - pushes summaries to chat tools
   - falls back to human takeover when browser automation fails

This open-source repo focuses on layers 2 and 3, with layer 4 exposed as adapter interfaces.

## Core Rules Preserved

- A job should not be treated as new just because `security_id` changed.
- The first stable ID should come from the best available identity source:
  - `security_id`
  - canonical job detail URL / job detail ID
  - fallback `title + company + district`
- `code=1` greeting failures should be marked as platform rejected and excluded from future retries.
- Auto-greet should only target records that are:
  - not skipped
  - not already greeted
  - not blocked by platform rejection
- Resume auto-send should only trigger once:
  - after a job has been greeted
  - after the first new recruiter reply
  - before `resume_sent_at` is set

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
```

## Example Integration Shape

Your private implementation can plug these rules into adapters like:

- `BossSearchAdapter`
- `BossChatAdapter`
- `ResumeRenderer`
- `Notifier`

The adapters should handle platform-specific details such as:

- `boss-cli`
- browser cookie refresh
- Playwright / Camoufox chat sending
- OpenClaw / WeChat / Telegram delivery

## Suggested Private Extensions

- add a real search adapter backed by `boss-cli`
- add a real browser sender for chat + attachment upload
- connect a notifier to WeChat / Telegram / email
- persist runtime logs as JSONL
- add cron wrappers or workflow jobs

## Repo Notes

This repository is intentionally documentation-first and safety-first. It captures the automation logic and state transitions without publishing private credentials, personal job materials, or environment-specific glue.
