from boss_job_automation.dedupe import build_job_identity
from boss_job_automation.models import JobRecord, ReplyEvent
from boss_job_automation.planner import build_auto_greet_plan
from boss_job_automation.rules import (
    can_auto_greet,
    is_greet_platform_rejection,
    mark_platform_rejected,
    should_generate_resume_on_reply,
)
from boss_job_automation.state import sync_runtime_blocked_jobs


def test_identity_prefers_security_id():
    identity = build_job_identity(
        {
            "security_id": "sec_123",
            "canonical_source_url": "https://www.zhipin.com/job_detail/abc123.html",
            "title": "AI测试开发",
            "company": "Example",
            "district": "朝阳",
        }
    )
    assert identity["stable_id"] == "sec_123"


def test_identity_falls_back_to_detail_id():
    identity = build_job_identity(
        {
            "canonical_source_url": "https://www.zhipin.com/job_detail/abc123.html",
            "title": "AI测试开发",
            "company": "Example",
            "district": "朝阳",
        }
    )
    assert identity["stable_id"] == "abc123"


def test_platform_rejection_blocks_auto_greet():
    job = JobRecord(stable_id="job-1")
    assert can_auto_greet(job) is True
    mark_platform_rejected(job, code="1", reason="platform", error="开聊提醒 (code=1)", blocked_at="2026-03-28T18:00:00+08:00")
    assert can_auto_greet(job) is False


def test_code_1_detection():
    assert is_greet_platform_rejection("开聊提醒 (code=1)")
    assert not is_greet_platform_rejection("session expired (code=36)")


def test_first_reply_generates_resume_once():
    job = JobRecord(stable_id="job-1", greeted_at="2026-03-28T10:00:00+08:00")
    reply = ReplyEvent(fingerprint="r1", recruiter_message="方便发下简历吗", trigger="any_reply")
    assert should_generate_resume_on_reply(job, reply) is True
    job.reply_last_fingerprint = "r1"
    assert should_generate_resume_on_reply(job, reply) is False


def test_reply_requires_prior_greet():
    job = JobRecord(stable_id="job-1")
    reply = ReplyEvent(fingerprint="r1", recruiter_message="你好", trigger="any_reply")
    assert should_generate_resume_on_reply(job, reply) is False


def test_auto_greet_plan_excludes_blocked_and_greeted():
    jobs = {
        "new-ok": JobRecord(stable_id="new-ok", first_seen_at="2026-03-28T10:00:00+08:00", score=90),
        "blocked": JobRecord(stable_id="blocked", greet_blocked_at="2026-03-28T11:00:00+08:00"),
        "greeted": JobRecord(stable_id="greeted", greeted_at="2026-03-28T12:00:00+08:00"),
        "backlog": JobRecord(stable_id="backlog", first_seen_at="2026-03-27T10:00:00+08:00", score=80),
    }
    plan = build_auto_greet_plan(
        jobs,
        new_ids=["new-ok", "blocked", "greeted"],
        improved_ids=[],
        include_backlog=True,
        backlog_limit=10,
    )
    assert plan.new_ids == ["new-ok"]
    assert plan.backlog_ids == ["backlog"]


def test_runtime_block_sync_marks_unsent_failures():
    jobs = {"job-1": JobRecord(stable_id="job-1")}
    synced = sync_runtime_blocked_jobs(
        jobs,
        [
            {
                "job_id": "job-1",
                "failed_at": "2026-03-28T18:00:00+08:00",
                "code": "1",
                "reason": "platform_rejected",
                "error": "开聊提醒 (code=1)",
            }
        ],
    )
    assert synced == 1
    assert jobs["job-1"].greet_blocked_code == "1"
