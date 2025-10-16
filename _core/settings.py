from pathlib import Path

# python-decouple
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("DJANGO_SECRET_KEY", default="default-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "mathew-storm-site-6sz7p.ondigitalocean.app",
    "mathewstorm.ca",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",  # Added for SEO sitemap
    "taggit",
    "django_htmx",
    "django_spellbook",
    "analytics",
    "A_base",
    "projects",
    "tutorials",
    "blog",
    "notes",
    "questions",
    "philo",
    "writing",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "analytics.middleware.PageViewMiddleware",
    "A_base.middleware.ThemeMiddleware",  # Theme switching support
]

ROOT_URLCONF = "_core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "analytics.context_processors.analytics_context",
            ],
        },
    },
]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Keep Django's default loggers
    "formatters": {
        "verbose": {
            "format": "\n{levelname} {asctime} {module} {name}:\n{message}",
            "style": "{",
        },
        "simple": {
            "format": "\n{levelname} {name}:\n{message}",
            "style": "{",
        },
        "none": {
            "format": "{message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",  # Set the overall handler level to DEBUG to allow debug messages through
            "class": "logging.StreamHandler",  # Outputs to console (stderr by default)
            "formatter": "simple",  # You can choose 'simple' or 'verbose'
        },
        "console-none": {
            "level": "DEBUG",  # Set the overall handler level to DEBUG to allow debug messages through
            "class": "logging.StreamHandler",  # Outputs to console (stderr by default)
            "formatter": "none",  # You can choose 'simple' or 'verbose'
        },
    },
    "loggers": {
        "django": {  # Configure Django's internal loggers
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "questions": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "questions.tests": {
            "handlers": ["console-none"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    # Root logger (optional, catches anything not caught by specific loggers)
    # '': {
    #     'handlers': ['console'],
    #     'level': 'INFO', # Default level for other modules
    # },
}

WSGI_APPLICATION = "_core.wsgi.application"

STATIC_ROOT = BASE_DIR / "staticfiles"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom Earthtone Theme Configuration
EARTHTONE_THEME = {
    'name': 'earthtone',
    'modes': {
        'light': {
            'colors': {
                # Main brand colors from the palette
                'primary': '#466b5d',      # Forest green
                'secondary': '#587a84',    # Blue-grey
                'accent': '#be9167',       # Warm golden
                'neutral': '#8f897b',      # Neutral brown-grey
                
                # Status colors (keeping semantic)
                'error': '#9c525a',        # Muted red from palette
                'warning': '#ab6c2c',      # Orange-brown from palette
                'success': '#466b5d',      # Using forest green
                'info': '#418791',         # Teal from palette
                
                # UI colors
                'background': '#e8e8df',   # Off-white
                'surface': '#dbdbd0',      # Light grey
                'text': '#29323b',         # Dark blue-grey
                'text-secondary': '#5e5d5d', # Medium grey
                
                # Extended colors from palette
                'emphasis': '#8f422c',     # Strong red-brown
                'subtle': '#b3b09f',       # Light brown-grey
                'distinct': '#9e6a55',     # Terra cotta
                'aether': '#6f6d76',       # Purple-grey
                'artifact': '#a67c23',     # Deep gold
                'sylvan': '#364f33',       # Deep forest green
                'danger': '#8f422c',       # Deep red-brown
            },
            'generate_variants': True
        },
        'dark': {
            'colors': {
                # Main brand colors - sleek professional palette
                'primary': '#4f8fba',      # Cool professional blue
                'secondary': '#75a743',    # Calming green
                'accent': '#de9e41',       # Warm golden accent
                'neutral': '#394a50',      # Neutral blue-grey
                
                # Status colors - muted but clear
                'error': '#cf573c',        # Muted red-orange
                'warning': '#e8c170',      # Soft golden warning
                'success': '#468232',      # Success green
                'info': '#73bed3',         # Light blue info
                
                # UI colors - deep professional dark theme
                'background': '#090a14',   # Deep dark blue-black
                'surface': '#151d28',      # Slightly lighter surface
                'text': '#d7b594',         # Warm light text for readability
                'text-secondary': '#73bed3', # Cool blue-grey secondary text
                
                # Extended colors from palette
                'emphasis': '#df84a5',     # Soft pink emphasis
                'subtle': '#202e37',       # Subtle dark blue
                'distinct': '#c65197',     # Distinct purple-pink
                'aether': '#7a367b',       # Deep purple
                'artifact': '#be772b',     # Bronze-gold artifact
                'sylvan': '#25562e',       # Deep forest green
                'danger': '#a53030',       # Clear danger red
            },
            'generate_variants': True
        }
    }
}

# Set default theme - can be overridden by session
SPELLBOOK_THEME = EARTHTONE_THEME['modes']['dark']

SPELLBOOK_MD_PATH = [
    BASE_DIR / "projects_content",
    BASE_DIR / "tutorials_content",
    BASE_DIR / "blog_content",
    BASE_DIR / "notes_content",
    BASE_DIR / "philo_content",
]

SPELLBOOK_MD_APP = [
    "projects",
    "tutorials",
    "blog",
    "notes",
    "philo",
]

SPELLBOOK_MD_URL_PREFIX = [
    "proj",
    "tuts",
    "blog",
    "note",
    "philo",
]

SPELLBOOK_MD_BASE_TEMPLATE = "A_base/sb_base.html"

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


ANALYTICS_EXCLUDED_PATHS = ["/main.mjs"]

ANALYTICS_EXCLUDED_PREFIXES = [
    "/hidden",
    "/prop",
]

QUESTION_DATA_DIRECTORIES = [
    BASE_DIR / "tutorials_content/git-for-beginners",
    BASE_DIR / "tutorials_content/django-webdev-fundamentals",
    BASE_DIR / "notes_content/classes/IPC144/textbook",
]
