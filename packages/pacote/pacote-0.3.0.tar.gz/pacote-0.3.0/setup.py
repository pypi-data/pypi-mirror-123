# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pacote']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['pacote-script = pacote.cli:cli']}

setup_kwargs = {
    'name': 'pacote',
    'version': '0.3.0',
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
