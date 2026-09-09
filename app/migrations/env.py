import sys
from logging.config import fileConfig
from os.path import dirname, abspath

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.database import Base

# УБРАЛИ прямые импорты моделей — они не нужны

# Если без этой строки Alembic не видит модули в Docker, лучше настроить PYTHONPATH,
# а не менять sys.path здесь.
# sys.path.insert(0, dirname(dirname(abspath(__file__))))

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL_SYNC)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # NullPool здесь уместен, потому что мы не делаем реальных запросов к БД
        poolclass=pool.NullPool,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        # В онлайн-режиме используем обычный пул
        poolclass=None,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
