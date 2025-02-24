from django.apps import AppConfig

class ReviewFeedbackSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ReviewFeedbackSystem'

class RRSConfig(AppConfig):
    name = 'RRS'

    def ready(self):
        import RRS.signals
