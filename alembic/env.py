import os

from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import MetaData, create_engine
from sqlalchemy.sql import text

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
# thanks stackoverflow:
# https://stackoverflow.com/questions/67526879/alembic-alembic-configuration-not-found-in-env-file
config = context.config


# here we allow ourselves to pass interpolation vars to alembic.ini
# from the host env
section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.environ.get("DB_USER"))
config.set_section_option(section, "DB_PASS", os.environ.get("DB_PASS"))

metadata = MetaData()

with open('db.sql', 'r') as f:
    sql_code = f.read()

for statement in sql_code.split(';'):
    if statement.strip():
        try:
            query = text(statement)
            engine = create_engine(config.get_main_option("sqlalchemy.url"))
            query.compile(bind=engine)
            metadata.reflect(bind=engine)
        except Exception as e:
            print(f"Ошибка при парсинге SQL-кода: {e}")

print(metadata.tables) # Для теста, закомментить позже

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
