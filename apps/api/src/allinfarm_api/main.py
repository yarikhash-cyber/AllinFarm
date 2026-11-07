"""FastAPI application. All routes live under /api; Caddy proxies them."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from allinfarm_api import __version__, health
from allinfarm_api.db import get_engine


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    yield
    await get_engine().dispose()


app = FastAPI(
    title="AllinFarm API",
    version=__version__,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None,
    lifespan=lifespan,
)
app.include_router(health.router, prefix="/api", tags=["system"])
