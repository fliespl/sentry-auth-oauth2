from django.conf import settings

CLIENT_ID = getattr(settings, 'OAUTH2_APP_ID', None)

CLIENT_SECRET = getattr(settings, 'OAUTH2_API_SECRET', None)

SCOPE = getattr(settings, 'OAUTH2_SCOPE', 'user:email')

API_DOMAIN = getattr(settings, 'OAUTH2_API_DOMAIN','oauth2.com/api')

BASE_DOMAIN = getattr(settings, 'OAUTH2_BASE_DOMAIN', 'oauth2.com')

ACCESS_TOKEN_URL = 'https://{0}/oauth/v2/token'.format(BASE_DOMAIN)

AUTHORIZE_URL = 'https://{0}/oauth/v2/auth'.format(BASE_DOMAIN)
