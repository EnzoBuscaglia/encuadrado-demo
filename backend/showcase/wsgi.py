"""
WSGI config for showcase project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

# from django.core import management

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()
if ENVIRONMENT == "STAGING":
    settings = "staging"
elif ENVIRONMENT == "PRODUCTION":
    settings = "production"
else:
    settings = "development"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "showcase.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", settings.title())

from configurations.wsgi import get_wsgi_application  # noqa

# management.call_command("compilemessages")
application = get_wsgi_application()
