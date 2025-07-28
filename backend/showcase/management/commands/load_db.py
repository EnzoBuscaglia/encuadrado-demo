import logging
import os
import subprocess

from django.core.management.base import BaseCommand

logger = logging.getLogger("model")


class Command(BaseCommand):
    help = "Load database from db/dump.json"

    def handle(self, *args, **options):
        environment = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()
        if environment != "DEVELOPMENT":
            logger.error(
                "This command can only be run in development environment. "
                "Check your .env environment."
            )
            return
        dump_path = "db/dump.json"
        if not os.path.exists(path=dump_path):
            logger.error("Dump file %s does not exist.", dump_path)
            return
        try:
            logger.info("Running database migrations")
            subprocess.run(
                args=["python", "manage.py", "migrate"],
                check=True,
                capture_output=True,
                text=True,
            )
            logger.info("Loading database from %s", dump_path)
            subprocess.run(
                args=["python", "manage.py", "loaddata", dump_path],
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info("Successfully loaded database from %s", dump_path)
        except subprocess.CalledProcessError as e:
            logger.error("An error occurred during migration or data loading: %s", e.stderr)
        except Exception as e:
            logger.exception("An unexpected error occurred during database loading: %s", e)
