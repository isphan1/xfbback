from django.apps import AppConfig


class FbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fb'

    def ready(self) -> None:
        import fb.signals
