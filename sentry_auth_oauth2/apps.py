from django.apps import AppConfig


class Config(AppConfig):
    name = "sentry_auth_oauth2"

    def ready(self) -> None:
        from sentry import auth
        
        from .provider import GenericOAuth2Provider

        auth.register(GenericOAuth2Provider)
