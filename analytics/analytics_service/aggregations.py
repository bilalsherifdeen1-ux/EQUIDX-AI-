"""Aggregation/business-logic layer for the analytics dashboard. Kept
separate from the FastAPI route handlers so aggregation logic is unit
testable without spinning up the HTTP app."""
from analytics_service.db import fetch_counts


async def build_overview() -> dict:
    counts = await fetch_counts()
    total_samples = counts["total_samples"] or 1  # avoid div-by-zero
    analyzed = counts["samples_by_status"].get("analyzed", 0)
    counts["analysis_completion_rate"] = round(analyzed / total_samples, 4)
    return counts
