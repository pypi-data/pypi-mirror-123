# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bearparse']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'attrs>=21.2.0,<22.0.0']

setup_kwargs = {
    'name': 'bearparse',
    'version': '0.3.0',
    'description': 'A custom argument parser for non-standard arguments. Useful for Appworx',
    'long_description': None,
    'author': 'Zevaryx',
    'author_email': 'zevaryx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
