from django.apps import AppConfig


class MyschoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myschool'

    def ready(self) -> None:
        import myschool.signals