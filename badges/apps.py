# badges/apps.py
from django.apps import AppConfig

class BadgesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'badges'

    def ready(self):
        import badges.signals  # ← Dòng này QUAN TRỌNG! Load signals