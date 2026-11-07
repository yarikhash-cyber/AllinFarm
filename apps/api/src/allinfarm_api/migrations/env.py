"""Alembic environment. Migrations run with the same DATABASE_URL as the API."""

from alembic import context
from sqlalchemy import create_engine, pool

from allinfarm_api.config import get_settings

target_metadata = None


def run_migrations() -> None:
    engine = create_engine(get_settings().database_url, poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    context.configure(url=get_settings().database_url, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    run_migrations()
