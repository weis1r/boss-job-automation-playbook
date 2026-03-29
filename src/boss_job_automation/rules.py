from __future__ import annotations

from .models import JobRecord, ReplyEvent


def is_platform_rejected(job: JobRecord) -> bool:
    return bool(job.greet_blocked_at)


def can_auto_greet(job: JobRecord | None) -> bool:
    return bool(job) and not job.skipped and not job.greeted_at and not is_platform_rejected(job)


def mark_platform_rejected(job: JobRecord, *, code: str, reason: str, error: str, blocked_at: str) -> None:
    job.greet_blocked_at = blocked_at
    job.greet_blocked_code = code
    job.greet_blocked_reason = reason
    job.greet_blocked_error = error


def clear_platform_rejected(job: JobRecord) -> None:
    job.greet_blocked_at = ""
    job.greet_blocked_code = ""
    job.greet_blocked_reason = ""
    job.greet_blocked_error = ""


def is_greet_platform_rejection(error_text: str) -> bool:
    text = str(error_text or "")
    return "(code=1)" in text or "code=1" in text


def should_generate_resume_on_reply(job: JobRecord, reply: ReplyEvent) -> bool:
    if not job.greeted_at:
        return False
    if job.resume_sent_at:
        return False
    if not reply.fingerprint:
        return False
    if reply.fingerprint == job.reply_last_fingerprint:
        return False
    if reply.trigger not in {"any_reply", "resume_only", "resume_request"}:
        return False
    if reply.trigger == "resume_only":
        text = reply.recruiter_message.lower()
        return any(token in text for token in ["resume", "cv", "简历", "附件", "pdf"])
    return True
