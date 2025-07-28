import logging
import os
import subprocess

from django.core.management.base import BaseCommand

logger = logging.getLogger("model")


class Command(BaseCommand):
    help = "Dump entire database to db/dump.json"

    def handle(self, *args, **options):
        environment = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()
        if environment != "DEVELOPMENT":
            logger.error(
                "This command can only be run in development environment. "
                "Check your .env environment."
            )
            return
        try:
            logger.info("Starting database dump process")
            result = subprocess.run(
                args=["python", "manage.py", "dumpdata", "--indent=2"],
                capture_output=True,
                text=True,
                check=True,
            )
            dump_path = "db/dump.json"
            os.makedirs(os.path.dirname(dump_path), exist_ok=True)
            with open(file=dump_path, mode="w", encoding="utf-8") as f:
                f.write(result.stdout)
            logger.info("Successfully dumped entire database to %s", dump_path)
        except subprocess.CalledProcessError as e:
            logger.error("Error during dumpdata: %s", e.stderr)
        except Exception as e:
            logger.exception("An unexpected error occurred during data dump: %s", e)
