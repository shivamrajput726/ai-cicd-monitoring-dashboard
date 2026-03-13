from contextlib import asynccontextmanager
import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api import routes_auth, routes_pipelines, routes_insights, routes_events
from app.core.config import get_settings
from app.db import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
                }
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["default"],
            },
        }
    )


def create_app() -> FastAPI:
    configure_logging()
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routes_auth.router)
    app.include_router(routes_pipelines.router)
    app.include_router(routes_insights.router)
    app.include_router(routes_events.router)

    Instrumentator().instrument(app).expose(app, include_in_schema=False)

    @app.get("/health", tags=["health"])
    async def health():
        return {"status": "ok"}

    return app


app = create_app()

