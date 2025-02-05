from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'addressBook.users'

    def ready(self):
        import addressBook.users.signals
