"""Unit test for the aggregation layer using a monkeypatched DB call, so
this test doesn't require a live Postgres instance."""
import pytest

from analytics_service import aggregations


@pytest.mark.asyncio
async def test_build_overview_computes_completion_rate(monkeypatch):
    async def fake_fetch_counts():
        return {
            "total_patients": 10, "total_samples": 4, "total_reports": 2,
            "samples_by_status": {"analyzed": 2, "registered": 2},
            "samples_by_type": {"urinalysis": 4},
        }

    monkeypatch.setattr(aggregations, "fetch_counts", fake_fetch_counts)
    result = await aggregations.build_overview()
    assert result["analysis_completion_rate"] == 0.5
