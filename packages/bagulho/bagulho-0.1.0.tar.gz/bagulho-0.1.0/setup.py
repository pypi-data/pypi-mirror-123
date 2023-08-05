# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bagulho']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['bagulho-cli = bagulho.cli:cli']}

setup_kwargs = {
    'name': 'bagulho',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'dunossauro',
    'author_email': 'mendesxeduardo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
