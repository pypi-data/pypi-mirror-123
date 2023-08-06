# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_hub_sdk', 'django_hub_sdk.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0,<4.0', 'djangorestframework', 'requests2']

setup_kwargs = {
    'name': 'django-hub-sdk',
    'version': '0.1.0',
    'description': 'The ISS (International Space Station) aims to be a space station (client) of connection between the microservices of its ecosystem and the authentication and permissions microservice of the user that here is called in the script as Hub.permissions modules / microservices (Hub)',
    'long_description': '# django-hub-sdk\n\nThe ISS (International Space Station) aims to be a space station (client) of connection between the microservices of its\necosystem and the authentication and permissions microservice of the user that here is called in the script as\nHub.permissions modules / microservices (Hub)',
    'author': 'Guilherme Haynes Howe',
    'author_email': 'zerossb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bildvitta/django-hub-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
