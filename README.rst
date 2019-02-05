Generic Auth for Sentry
======================

An SSO provider for Sentry which enables Generic organization-restricted authentication.

Install
-------

::

    $ pip install https://oauth2.com/getsentry/sentry-auth-oauth2/archive/master.zip

Setup
-----

Create a new application under your organization in Generic. Enter the **Authorization
callback URL** as the prefix to your Sentry installation:

::

    https://example.sentry.com


Once done, grab your API keys and drop them in your ``sentry.conf.py``:

.. code-block:: python

    OAUTH2_APP_ID = ""

    OAUTH2_API_SECRET = ""


Verified email addresses can optionally be required:

.. code-block:: python

    OAUTH2_REQUIRE_VERIFIED_EMAIL = True


Optionally you may also specify the domain (for GHE users):

.. code-block:: python

    OAUTH2_BASE_DOMAIN = "git.example.com"

    OAUTH2_API_DOMAIN = "api.git.example.com"


If Subdomain isolation is disabled in GHE:

.. code-block:: python

    OAUTH2_BASE_DOMAIN = "git.example.com"

    OAUTH2_API_DOMAIN = "git.example.com/api/v3"
