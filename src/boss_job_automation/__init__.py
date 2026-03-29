"""Reference rules and models for BOSS-style job automation."""

from .dedupe import build_job_identity
from .models import JobRecord, ReplyEvent
from .planner import AutoGreetPlan, build_auto_greet_plan
from .rules import can_auto_greet, should_generate_resume_on_reply

__all__ = [
    "AutoGreetPlan",
    "JobRecord",
    "ReplyEvent",
    "build_auto_greet_plan",
    "build_job_identity",
    "can_auto_greet",
    "should_generate_resume_on_reply",
]
