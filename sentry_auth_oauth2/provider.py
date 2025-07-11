from __future__ import annotations

from sentry.auth.exceptions import IdentityNotValid
from sentry.auth.providers.oauth2 import OAuth2Callback, OAuth2Login, OAuth2Provider
from sentry.auth.view import AuthView

from .client import GenericApiError, GenericClient
from .constants import ACCESS_TOKEN_URL, AUTHORIZE_URL, CLIENT_ID, CLIENT_SECRET, SCOPE
from .views import FetchUser


class GenericOAuth2Provider(OAuth2Provider):
    access_token_url = ACCESS_TOKEN_URL
    authorize_url = AUTHORIZE_URL
    name = 'OWL'
    key = 'oauth2'

    def get_client_id(self):
        return CLIENT_ID

    def get_client_secret(self):
        return CLIENT_SECRET

    def __init__(self, org=None, **config) -> None:
        super().__init__(**config)
        self.org = org

    def get_auth_pipeline(self) -> list[AuthView]:
        return [
            OAuth2Login(
                authorize_url=self.authorize_url, 
                client_id=self.get_client_id(),
                scope=SCOPE,
            ),
            OAuth2Callback(
                access_token_url=self.access_token_url,
                client_id=self.get_client_id(),
                client_secret=self.get_client_secret(),
            ),
            FetchUser(
                client_id=self.get_client_id(),
                client_secret=self.get_client_secret(),
                org=self.org,
            ),
        ]

    def get_setup_pipeline(self) -> list[AuthView]:
        pipeline = self.get_auth_pipeline()
        return pipeline

    def get_refresh_token_url(self) -> str:
        return ACCESS_TOKEN_URL

    def build_config(self, state):
        return {
        }

    def build_identity(self, state):
        data = state['data']
        user_data = state['user']
        return {
            'type': 'owl',
            'id': user_data['id'],
            'email': user_data['email'],
            'name': user_data['name'],
            'data': self.get_oauth_data(data),
            'email_verified': True,
        }
