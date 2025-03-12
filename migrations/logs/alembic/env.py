from logging.config import fileConfig
import asyncio
from alembic import context

from src.models.logs_models import logging_base
from src.database.logs_database import LOGGING_DATABASE_URL
from src.database.logs_database import logging_async_engine

config = context.config

section = config.config_ini_section
config.set_section_option(section, 'LOGGING_DATABASE_URL', LOGGING_DATABASE_URL)


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = logging_base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = f"sqlite+aiosqlite:///{LOGGING_DATABASE_URL}"
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = logging_async_engine

    async def do_run_migrations():
        async with connectable.begin() as connection:
            await connection.run_sync(do_migrations)

    def do_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
    