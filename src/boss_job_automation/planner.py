from __future__ import annotations

from .models import AutoGreetPlan, JobRecord
from .rules import can_auto_greet


def build_auto_greet_plan(
    jobs: dict[str, JobRecord],
    *,
    new_ids: list[str],
    improved_ids: list[str],
    include_backlog: bool,
    backlog_limit: int = 0,
) -> AutoGreetPlan:
    selected: set[str] = set()
    plan = AutoGreetPlan()

    def add(job_ids: list[str], bucket: list[str]) -> None:
        for job_id in job_ids:
            record = jobs.get(job_id)
            if job_id in selected or not can_auto_greet(record):
                continue
            bucket.append(job_id)
            selected.add(job_id)

    add(new_ids, plan.new_ids)

    if not include_backlog:
        return plan

    add(improved_ids, plan.improved_ids)

    backlog = [
        job_id
        for job_id, record in jobs.items()
        if job_id not in selected and can_auto_greet(record)
    ]
    backlog.sort(
        key=lambda job_id: (
            jobs[job_id].first_seen_at or "9999-12-31T00:00:00+08:00",
            -jobs[job_id].score,
        )
    )
    if backlog_limit > 0:
        backlog = backlog[:backlog_limit]
    plan.backlog_ids.extend(backlog)
    return plan
