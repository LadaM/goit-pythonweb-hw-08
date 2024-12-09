from logging.config import fileConfig

from alembic import context

from app.db import models  # noqa
from app.db.database import Base, engine

fileConfig(context.config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online():
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
