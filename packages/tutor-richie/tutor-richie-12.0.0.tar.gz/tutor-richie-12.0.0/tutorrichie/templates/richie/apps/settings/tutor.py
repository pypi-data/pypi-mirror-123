from configurations import values
from settings import Development, Production

class TutorSettingsMixin:
    RICHIE_COURSE_RUN_SYNC_SECRETS = values.ListValue(["{{ RICHIE_HOOK_SECRET }}"])
    # Restore error logging, which is disabled by default
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    }


class TutorProduction(TutorSettingsMixin, Production):
    """
    Tutor-specific settings for production.
    """
    {% if not ENABLE_HTTPS %}
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SESSION_COOKIE_SECURE = False
    {% endif %}

    # TODO language settings?
    # TODO compatible with profile/account mfe?

    {{ patch("richie-settings-production")|indent(4) }}


class TutorDevelopment(TutorSettingsMixin, Development):
    """
    Tutor-specific settings for development.
    """
    {{ patch("richie-settings-development")|indent(4) }}
