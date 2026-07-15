from fastapi import APIRouter
from app.api.routes import admin, ai, auth, dashboards, incidents, realtime

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(dashboards.router, prefix="/dashboards", tags=["dashboards"])
api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(realtime.router, prefix="/realtime", tags=["realtime"])
