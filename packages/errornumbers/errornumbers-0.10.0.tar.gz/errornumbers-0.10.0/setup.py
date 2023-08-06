# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['errornumbers']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'errornumbers',
    'version': '0.10.0',
    'description': 'Classes and functions for handling with numbers with errors',
    'long_description': None,
    'author': 'Anton Leagre',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
