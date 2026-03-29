from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class JobRecord:
    stable_id: str
    security_id: str = ""
    lid: str = ""
    canonical_source_url: str = ""
    title: str = ""
    company: str = ""
    district: str = ""
    city: str = ""
    score: int = 0
    skipped: bool = False
    greeted_at: str = ""
    first_seen_at: str = ""
    last_seen_at: str = ""
    greet_blocked_at: str = ""
    greet_blocked_code: str = ""
    greet_blocked_reason: str = ""
    greet_blocked_error: str = ""
    reply_last_fingerprint: str = ""
    resume_sent_at: str = ""
    resume_send_status: str = ""
    resume_send_error: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class ReplyEvent:
    fingerprint: str
    recruiter_message: str
    trigger: str = "any_reply"


@dataclass
class AutoGreetPlan:
    new_ids: list[str] = field(default_factory=list)
    improved_ids: list[str] = field(default_factory=list)
    backlog_ids: list[str] = field(default_factory=list)

    @property
    def all_ids(self) -> list[str]:
        return [*self.new_ids, *self.improved_ids, *self.backlog_ids]
