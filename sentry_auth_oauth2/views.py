from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from django.http import HttpRequest
from django.http.response import HttpResponseBase

from sentry.auth.view import AuthView

from .client import GenericApiError, GenericClient

if TYPE_CHECKING:
    from sentry.auth.helper import AuthHelper

logger = logging.getLogger("sentry.auth.oauth2")

ERR_INVALID_RESPONSE = "Unable to fetch user information from the identity provider."


def _get_name_from_email(email: str) -> str:
    """
    Given an email return a capitalized name. Ex. john.smith@example.com would return John Smith.
    """
    name = email.rsplit("@", 1)[0]
    name = " ".join(n_part.capitalize() for n_part in name.split("."))
    return name


class FetchUser(AuthView):
    def __init__(
        self, client_id: str | None, client_secret: str | None, org: Any = None, *args: Any, **kwargs: Any
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.org = org
        super().__init__(*args, **kwargs)

    def handle(self, request: HttpRequest, pipeline: AuthHelper) -> HttpResponseBase:
        data: dict[str, Any] | None = pipeline.fetch_state("data")
        if not data or "access_token" not in data:
            return pipeline.error(ERR_INVALID_RESPONSE)

        with GenericClient(self.client_id, self.client_secret) as client:
            try:
                user = client.get_user(data["access_token"])
            except GenericApiError as e:
                logger.warning("oauth2.fetch-user-failed", extra={"status": e.status})
                return pipeline.error(ERR_INVALID_RESPONSE)

        if not isinstance(user, dict) or not user.get("email") or user.get("id") is None:
            return pipeline.error(ERR_INVALID_RESPONSE)

        if not user.get("name"):
            user["name"] = _get_name_from_email(user["email"])

        pipeline.bind_state("user", user)

        return pipeline.next_step()
