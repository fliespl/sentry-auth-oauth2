from __future__ import annotations

from sentry.auth.view import AuthView
from sentry.models import AuthIdentity

from .client import GenericClient


def _get_name_from_email(email):
    """
    Given an email return a capitalized name. Ex. john.smith@example.com would return John Smith.
    """
    name = email.rsplit("@", 1)[0]
    name = " ".join(n_part.capitalize() for n_part in name.split("."))
    return name


class FetchUser(AuthView):
    def __init__(self, client_id, client_secret, org=None, *args, **kwargs) -> None:
        self.org = org
        self.client = GenericClient(client_id, client_secret)
        super().__init__(*args, **kwargs)

    def handle(self, request: HttpRequest, pipeline):
        access_token = pipeline.fetch_state('data')['access_token']

        user = self.client.get_user(access_token)

        if not user.get('name'):
            user['name'] = _get_name_from_email(user['email'])

        pipeline.bind_state('user', user)

        return pipeline.next_step()
