from django.apps import AppConfig

class RepositoriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'repositories'

    # Schedule repository updater task when app is run
    def ready(self):
      from repositories import updater
      updater.start()