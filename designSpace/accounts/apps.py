from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'designSpace.accounts'

    def ready(self):
        import designSpace.accounts.signals