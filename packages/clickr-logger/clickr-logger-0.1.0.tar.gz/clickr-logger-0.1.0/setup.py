# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clickr_logger']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'clickr-logger',
    'version': '0.1.0',
    'description': 'Common logger functions for clickr',
    'long_description': None,
    'author': 'Grzegorz Bajson',
    'author_email': 'gbajson@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
