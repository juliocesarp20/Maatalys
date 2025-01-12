import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from src.db.base import Base  # Base class
from src.search.models import Search
from src.investigation.models import Investigation
from src.parameter.models import Parameter
from src.parameter_search.models import ParameterSearch
from src.db.session import settings

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Target metadata
target_metadata = Base.metadata

# Debugging
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
