# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['application_kit_hxrn']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.3.1', 'aiohttp>=3.7.4,<4.0.0', 'python-dotenv==0.13.0']

setup_kwargs = {
    'name': 'application-kit-hxrn',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'hexrain',
    'author_email': 'hexrain@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
