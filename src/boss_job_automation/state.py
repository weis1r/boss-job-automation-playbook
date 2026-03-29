from __future__ import annotations

from .models import JobRecord


def sync_runtime_blocked_jobs(
    jobs: dict[str, JobRecord],
    failures: list[dict[str, str]],
) -> int:
    synced = 0
    for item in failures:
        job_id = str(item.get("job_id", "")).strip()
        if not job_id or job_id not in jobs:
            continue
        job = jobs[job_id]
        if job.greeted_at and item.get("failed_at", "") <= job.greeted_at:
            continue
        if job.greet_blocked_at:
            continue
        job.greet_blocked_at = str(item.get("failed_at", "")).strip()
        job.greet_blocked_code = str(item.get("code", "1")).strip() or "1"
        job.greet_blocked_reason = str(item.get("reason", "platform_rejected")).strip()
        job.greet_blocked_error = str(item.get("error", "")).strip()
        synced += 1
    return synced
