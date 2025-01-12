import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from src.db.base import Base
from src.db.session import settings
from src.investigation.models import Investigation
from src.parameter.models import Parameter
from src.parameter_search.models import ParameterSearch
from src.search.models import Search

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

print("Loaded tables:", target_metadata.tables.keys())


def run_migrations_offline():
    url = settings.SQLALCHEMY_DATABASE_URI
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = create_async_engine(
        settings.SQLALCHEMY_DATABASE_URI, poolclass=pool.NullPool
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
