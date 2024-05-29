from django.apps import AppConfig


class admin_customDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_dashboard'

    def ready(self) -> None:
        import admin_dashboard.signals
