# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['angry_logger']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'angry-logger',
    'version': '0.1.0',
    'description': 'Make your logging more passive agressive. Or just agressive.',
    'long_description': None,
    'author': 'Toby Devlin',
    'author_email': 'toby@thedevlins.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
