"""Aggregates all v1 routers into a single APIRouter mounted in main.py."""
from fastapi import APIRouter

from app.api.v1.routers import admin, analytics, auth, files, notifications, oauth, patients, reports, samples

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(oauth.router)
api_router.include_router(patients.router)
api_router.include_router(samples.router)
api_router.include_router(reports.router)
api_router.include_router(files.router)
api_router.include_router(notifications.router)
api_router.include_router(admin.router)
api_router.include_router(analytics.router)
