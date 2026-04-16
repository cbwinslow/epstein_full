"""Sentry error tracking configuration for Epstein data project.

Usage:
    from config.sentry_config import init_sentry
    init_sentry()

Environment variables needed:
    SENTRY_DSN - The Sentry project DSN (required)
    SENTRY_ENVIRONMENT - Environment name (default: development)
    SENTRY_RELEASE - Release version (optional)
"""

import logging
import os

logger = logging.getLogger(__name__)


def init_sentry():
    """Initialize Sentry SDK for error tracking."""
    sentry_dsn = os.getenv("SENTRY_DSN")

    if not sentry_dsn:
        logger.warning("SENTRY_DSN not set - Sentry error tracking disabled")
        return

    try:
        import sentry_sdk
        from sentry_sdk.integrations.logging import LoggingIntegration

        # Configure Sentry
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
            release=os.getenv("SENTRY_RELEASE"),
            # Performance monitoring (optional)
            traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.1")),
            # Profiling (optional, requires sentry-sdk[profiling])
            profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.0")),
            # Enable logging integration
            integrations=[
                LoggingIntegration(
                    level=logging.INFO,
                    event_level=logging.ERROR,
                )
            ],
            # Data scrubbing - IMPORTANT for Epstein project
            before_send=scrub_sensitive_data,
            # Don't send PII
            send_default_pii=False,
        )

        logger.info(
            f"Sentry initialized - environment: {os.getenv('SENTRY_ENVIRONMENT', 'development')}"
        )

    except ImportError:
        logger.warning("sentry-sdk not installed - run: pip install sentry-sdk")
    except Exception as e:
        logger.error(f"Failed to initialize Sentry: {e}")


def scrub_sensitive_data(event, hint):
    """Remove sensitive data from Sentry events before sending.

    This is CRITICAL for the Epstein project to avoid leaking:
    - Database credentials
    - File paths containing sensitive info
    - API keys
    """
    # Scrub exception messages that might contain SQL
    if "exception" in event:
        for exception in event["exception"].get("values", []):
            if "stacktrace" in exception:
                for frame in exception["stacktrace"].get("frames", []):
                    # Scrub vars that might contain sensitive data
                    vars_dict = frame.get("vars", {})
                    for key in list(vars_dict.keys()):
                        if any(
                            sensitive in key.lower()
                            for sensitive in [
                                "password",
                                "secret",
                                "token",
                                "key",
                                "auth",
                                "database_url",
                                "db_url",
                                "connection_string",
                            ]
                        ):
                            vars_dict[key] = "[REDACTED]"

    # Scrub breadcrumbs
    if "breadcrumbs" in event:
        for crumb in event["breadcrumbs"].get("values", []):
            message = crumb.get("message", "")
            if message:
                # Redact potential SQL queries or file paths
                if any(
                    sensitive in message
                    for sensitive in ["SELECT", "INSERT", "UPDATE", "DELETE", "password", "secret"]
                ):
                    crumb["message"] = "[REDACTED - potential sensitive data]"

    return event


def capture_exception(func):
    """Decorator to automatically capture exceptions in Sentry.

    Usage:
        @capture_exception
        def process_data():
            ...
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            try:
                import sentry_sdk

                sentry_sdk.capture_exception(e)
            except ImportError:
                pass
            raise

    return wrapper
