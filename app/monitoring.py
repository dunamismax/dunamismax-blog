"""Performance monitoring utilities for the blog."""

from __future__ import annotations

import os
from typing import Any

import httpx

PSI_API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


async def monitor_core_web_vitals(
    url: str, strategy: str = "mobile"
) -> dict[str, float]:
    """Return core web vitals metrics for a URL using PageSpeed Insights."""
    params = {
        "url": url,
        "strategy": strategy,
        "category": "performance",
        "key": os.getenv("GOOGLE_API_KEY", ""),
    }
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(PSI_API, params=params)
        response.raise_for_status()
        audits: dict[str, Any] = (
            response.json().get("lighthouseResult", {}).get("audits", {})
        )
        return {
            "LCP": audits.get("largest-contentful-paint", {}).get("numericValue", 0.0),
            "INP": audits.get("interactive", {}).get("numericValue", 0.0),
            "CLS": audits.get("cumulative-layout-shift", {}).get("numericValue", 0.0),
        }
