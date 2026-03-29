from __future__ import annotations

import re
from urllib.parse import urlparse


def _normalize_text(value: str) -> str:
    text = " ".join(str(value or "").split())
    return text.strip()


def _slug(value: str) -> str:
    text = _normalize_text(value).lower()
    text = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", text)
    return text.strip("-")


def _detail_id_from_url(url: str) -> str:
    parsed = urlparse(_normalize_text(url))
    if not parsed.path:
        return ""
    match = re.search(r"/job_detail/([A-Za-z0-9]+)", parsed.path)
    if match:
        return match.group(1)
    return ""


def build_job_identity(job: dict[str, str]) -> dict[str, str]:
    security_id = _normalize_text(job.get("security_id", ""))
    canonical_url = _normalize_text(job.get("canonical_source_url", "") or job.get("job_url", ""))
    detail_id = _detail_id_from_url(canonical_url) or _normalize_text(job.get("job_detail_id", ""))
    fallback = "::".join(
        [
            _slug(job.get("title", "")),
            _slug(job.get("company", "")),
            _slug(job.get("district", "")),
        ]
    ).strip(":")

    stable_id = security_id or detail_id or canonical_url or fallback
    return {
        "stable_id": stable_id,
        "security_id": security_id,
        "detail_id": detail_id,
        "canonical_source_url": canonical_url,
        "fallback_id": fallback,
    }
