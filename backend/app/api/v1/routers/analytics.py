"""Analytics dashboard proxy endpoints — delegates aggregation logic to the
standalone `analytics` microservice, keeping heavy query/rollup logic out
of the core transactional API."""
from fastapi import APIRouter, Depends, HTTPException

from app.application.services.analytics_service import AnalyticsClient
from app.core.deps import CurrentUser, get_current_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview")
async def analytics_overview(current_user: CurrentUser = Depends(get_current_user)):
    client = AnalyticsClient()
    try:
        return await client.get_overview()
    except Exception:
        raise HTTPException(status_code=502, detail="Analytics service unavailable")
