from django.apps import AppConfig


class SpotifyConfig(AppConfig):
    name = 'spotify'

    def ready(self):
        import spotify.signals
