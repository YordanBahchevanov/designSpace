from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'designSpace.articles'

    def ready(self):
        import designSpace.articles.signals
