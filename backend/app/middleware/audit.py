"""HTTP middleware that attaches a request-scoped correlation ID and logs
every request's method/path/status/duration as structured JSON (consumed by
the ELK/OpenSearch pipeline). Business-level audit entries (who changed
what resource) are written explicitly by routers via AuditService — this
middleware provides the surrounding request-level trail."""
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logging import get_logger

logger = get_logger("http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        start = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 2)
        response.headers["x-correlation-id"] = correlation_id
        logger.info(
            "http_request",
            correlation_id=correlation_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
            client_ip=request.client.host if request.client else None,
        )
        return response
