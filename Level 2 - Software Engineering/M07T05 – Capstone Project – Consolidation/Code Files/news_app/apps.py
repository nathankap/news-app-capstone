"""App configuration module for news_app."""

from django.apps import AppConfig


class NewsAppConfig(AppConfig):
    """Application configuration for the news_app Django application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_app'

    def ready(self):
        """Import signals when application registry is ready."""
        import news_app.signals  # noqa: F401
