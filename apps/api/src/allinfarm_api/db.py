"""Database connection. One async engine per process."""

from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from allinfarm_api.config import get_settings


@lru_cache
def get_engine() -> AsyncEngine:
    return create_async_engine(get_settings().database_url, pool_pre_ping=True)
