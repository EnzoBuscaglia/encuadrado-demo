"""
ASGI config for showcase project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from configurations.asgi import get_asgi_application

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()
if ENVIRONMENT == "STAGING":
    settings = "staging"
elif ENVIRONMENT == "PRODUCTION":
    settings = "production"
else:
    settings = "development"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showcase.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", settings.title())
application = get_asgi_application()
