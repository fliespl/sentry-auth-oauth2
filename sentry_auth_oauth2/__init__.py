from __future__ import absolute_import

from sentry.auth import register

from .provider import GenericOAuth2Provider

register('oauth2', GenericOAuth2Provider)
