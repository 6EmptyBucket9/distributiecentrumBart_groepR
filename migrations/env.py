import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context
from app import create_app, db  # Ensure you have a create_app() function in your app

# Alembic Config object
config = context.config

# Set up logging
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Create the Flask app using the factory function
app = create_app()  # Replace with your app factory if needed

# Ensure that app context is pushed properly
# You can use 'with app.app_context():' to automatically manage the app context
with app.app_context():
    # Set target metadata for Alembic to detect models
    target_metadata = db.metadata

    # Configure database URL
    def get_engine_url():
        return app.config.get('SQLALCHEMY_DATABASE_URI').replace('%', '%%')

    # Set the sqlalchemy URL in the Alembic config
    config.set_main_option('sqlalchemy.url', get_engine_url())

    def run_migrations_offline():
        """Run migrations in 'offline' mode."""
        url = config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=target_metadata,
            literal_binds=True
        )

        with context.begin_transaction():
            context.run_migrations()

    def run_migrations_online():
        """Run migrations in 'online' mode."""

        def process_revision_directives(context, revision, directives):
            if getattr(config.cmd_opts, 'autogenerate', False):
                script = directives[0]
                if script.upgrade_ops.is_empty():
                    directives[:] = []
                    logger.info('No changes in schema detected.')

        connectable = db.engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                process_revision_directives=process_revision_directives
            )

            with context.begin_transaction():
                context.run_migrations()

    # Run migrations in either offline or online mode
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()