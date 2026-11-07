"""Health check: shows that the API, the engine and the database see each other."""

from typing import Literal

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from allinfarm_api import __version__
from allinfarm_api.db import get_engine
from allinfarm_engine import engine_info

router = APIRouter()


class DatabaseHealth(BaseModel):
    status: Literal["ok", "error"]
    postgres: str | None = None
    postgis: str | None = None
    error: str | None = None


class Health(BaseModel):
    status: Literal["ok", "degraded"]
    version: str
    engine: dict[str, str]
    database: DatabaseHealth


async def check_database() -> DatabaseHealth:
    try:
        async with get_engine().connect() as conn:
            postgres = (await conn.execute(text("SHOW server_version"))).scalar_one()
            postgis = (
                await conn.execute(
                    text("SELECT extversion FROM pg_extension WHERE extname = 'postgis'")
                )
            ).scalar_one_or_none()
    except (SQLAlchemyError, OSError) as exc:
        return DatabaseHealth(status="error", error=type(exc).__name__)
    return DatabaseHealth(status="ok", postgres=str(postgres).split()[0], postgis=postgis)


@router.get("/health", response_model=Health)
async def health(response: Response) -> Health:
    database = await check_database()
    ok = database.status == "ok" and database.postgis is not None
    if not ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return Health(
        status="ok" if ok else "degraded",
        version=__version__,
        engine=engine_info(),
        database=database,
    )
