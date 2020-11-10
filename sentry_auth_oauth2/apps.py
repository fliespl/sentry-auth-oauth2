from __future__ import absolute_import
from django.apps import AppConfig


class Config(AppConfig):
    name = "sentry_auth_oauth2"

    def ready(self):
        from sentry import auth
        from .provider import GenericOAuth2Provider

        auth.register('oauth2', GenericOAuth2Provider)
