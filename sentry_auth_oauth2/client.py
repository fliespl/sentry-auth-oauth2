from __future__ import annotations

import orjson

from requests.exceptions import RequestException

from sentry import http

from .constants import API_DOMAIN


class GenericApiError(Exception):
    def __init__(self, message='', status=0):
        super().__init__(message)
        self.status = status


class GenericClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.http = http.build_session()

    def __enter__(self) -> GenericClient:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.http.close()

    def _request(self, path, access_token):
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        headers = {
            'Authorization': 'Bearer {0}'.format(access_token),
        }

        try:
            req = self.http.get('https://{0}/{1}'.format(API_DOMAIN, path.lstrip('/')),
                params=params,
                headers=headers,
            )
        except RequestException as e:
            raise GenericApiError(f"{e}", status=getattr(e, 'status_code', 0))
        if req.status_code < 200 or req.status_code >= 300:
            raise GenericApiError(req.content, status=req.status_code)
        return orjson.loads(req.content)

    def get_user(self, access_token):
        return self._request('/user/me', access_token)

