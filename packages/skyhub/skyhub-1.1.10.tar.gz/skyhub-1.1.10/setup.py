# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skyhub', 'skyhub.controllers', 'skyhub.models', 'skyhub.utils']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.7,<4.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'skyhub',
    'version': '1.1.10',
    'description': '',
    'long_description': None,
    'author': 'Carmo-sousa',
    'author_email': 'carmosousa20@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
