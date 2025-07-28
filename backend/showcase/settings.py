import os
import sys
from pathlib import Path

from configurations import Configuration, values
from dj_database_url import config as dj_database_url_config

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


class Common(Configuration):

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_RELATIVE_DIR = os.path.dirname(__file__)
    STATIC_ROOT = os.path.join(BASE_RELATIVE_DIR, "static")
    STATIC_URL = "/static/"

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue() if values.SecretValue() == "None" else "XXX"

    ROOT_URLCONF = "showcase.urls"
    WSGI_APPLICATION = "showcase.wsgi.application"

    LANGUAGE_CODE = "en-us"
    LANGUAGES = [
        ("en", "English"),
        ("es", "Español"),
    ]
    TIME_ZONE = "America/Santiago"  # UTC default
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "showcase",
        "model",
        "marketplace",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "whitenoise.middleware.WhiteNoiseMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            #     "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
            #     "rest_framework_social_oauth2.authentication.SocialAuthentication",
            "rest_framework.authentication.SessionAuthentication",
        ),
        "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
        "PAGE_SIZE": int(os.getenv("REST_FRAMEWORK_PAGE_SIZE", "50")),
        "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
        "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    }


class Development(Common):

    DEBUG = True
    ALLOWED_HOSTS = []
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:5173",
    ]
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "custom_formatter",
                "stream": sys.stdout,
            },
        },
        "formatters": {
            "custom_formatter": {
                "format": "[%(asctime)s][%(name)s] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "loggers": {
            "showcase": {"handlers": ["console"], "level": "INFO"},
        },
    }

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": "postgres",
            "NAME": "showcase_db",
            "USER": "showcase_user",
            "PASSWORD": "showcase_pass",
            "PORT": "5432",  # TODO: CHECK
        }
    }


class Staging(Development):
    """Settings for the staging environment. Not used."""

    DEBUG = False
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "HOST": "localhost",
            "NAME": "gh_action_db",
            "USER": "gh_action_user",
            "PASSWORD": "gh_action_pass",
            "PORT": "5432",
        }
    }


class Production(Staging):

    DEBUG = False
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    DATABASES = {
        "default": {
            **dj_database_url_config(
                env="AWS_POSTGRES_URL",
                default="postgres://user:pass@localhost:5432/dbname",
                conn_max_age=600,
            ),
            "OPTIONS": {
                "sslmode": "require",
                "sslcert": "",
                "sslkey": "",
                "sslrootcert": "",
            },
        }
    }
