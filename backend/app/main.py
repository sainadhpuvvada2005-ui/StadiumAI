import logging
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import init_database

logger = logging.getLogger("stadiumai")
logging.basicConfig(level=logging.INFO, format='{"level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}')


def create_app() -> FastAPI:
    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_database()
        yield

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="AI-powered smart stadium operations platform for FIFA World Cup 2026",
        lifespan=lifespan,
    )
    
    @app.middleware("http")
    async def security_headers_rate_limit_and_timing(request: Request, call_next):
        started = time.perf_counter()
        # Skip rate limiting for OPTIONS requests (CORS preflight)
        if request.method != "OPTIONS":
            client = request.client.host if request.client else "unknown"
            bucket = getattr(app.state, "rate_limit_bucket", {})
            now = int(time.time() // 60)
            key = f"{client}:{now}"
            bucket[key] = bucket.get(key, 0) + 1
            app.state.rate_limit_bucket = {k: v for k, v in bucket.items() if k.endswith(f":{now}")}
            if bucket[key] > settings.rate_limit_per_minute:
                return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("request_failed method=%s path=%s", request.method, request.url.path)
            raise
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        response.headers["X-Request-Duration-Ms"] = str(duration_ms)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(self), geolocation=(self)"
        logger.info("request_completed method=%s path=%s status=%s duration_ms=%s", request.method, request.url.path, response.status_code, duration_ms)
        return response
    
    # Add middleware stack (order matters - added in reverse)
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(SessionMiddleware, secret_key=settings.jwt_secret, https_only=settings.environment == "production", same_site="lax")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": settings.app_name}

    @app.get("/liveness")
    def liveness() -> dict[str, str]:
        return {"status": "alive"}

    @app.get("/readiness")
    def readiness() -> dict[str, str]:
        init_database()
        return {"status": "ready", "database": "ok"}

    @app.get("/metrics")
    def metrics() -> dict[str, int | str]:
        return {"service": settings.app_name, "rate_limit_per_minute": settings.rate_limit_per_minute}

    @app.options("/{path_name:path}")
    async def preflight_handler(path_name: str):
        return {}

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
