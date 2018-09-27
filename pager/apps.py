from django.apps import AppConfig


class PagerConfig(AppConfig):
    name = 'pager'
    
    def ready(self):
        # noinspection PyUnresolvedReferences
        import pager.signals
