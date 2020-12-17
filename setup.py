#!/usr/bin/env python
"""
sentry-auth-oauth2
==================

:copyright: (c) 2016 Functional Software, Inc
"""
from setuptools import setup, find_packages


install_requires = [
    'sentry>=10.0.0',
]

tests_require = [
    'mock',
    'flake8>=2.0,<2.1',
]

setup(
    name='sentry-auth-oauth2',
    version='0.2.0',
    author='Sentry',
    author_email='support@getsentry.com',
    url='https://www.getsentry.com',
    description='Generic authentication provider for Sentry',
    long_description=__doc__,
    license='Apache 2.0',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'tests': tests_require},
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'auth_oauth2 = sentry_auth_oauth2.apps.Config',
        ],
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
    python_requires='>=3.6',
)
