from django.apps import AppConfig


class FoldersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'designSpace.folders'

    def ready(self):
        import designSpace.folders.signals
