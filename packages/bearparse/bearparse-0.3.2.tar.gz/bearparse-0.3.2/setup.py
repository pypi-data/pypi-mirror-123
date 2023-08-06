# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bearparse']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'attrs>=21.2.0,<22.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'bearparse',
    'version': '0.3.2',
    'description': 'A custom argument parser for non-standard arguments. Useful for Appworx',
    'long_description': '# bearparse\n\n![Python Unittests](https://github.com/zevaryx/bearparse/actions/workflows/python-package.yaml/badge.svg) [![codecov](https://codecov.io/gh/zevaryx/bearparse/main/graph/badge.svg?token=GG7DVUW7RJ)](https://codecov.io/gh/zevaryx/bearparse)\n\n[![pipeline status](https://git.zevaryx.com/zevaryx/bearparse/badges/main/pipeline.svg)](https://git.zevaryx.com/zevaryx/bearparse/-/commits/main)\n[![coverage report](https://git.zevaryx.com/zevaryx/bearparse/badges/main/coverage.svg)](https://git.zevaryx.com/zevaryx/bearparse/-/commits/main)\n\nA custom argument parser for non-standard arguments. Useful for Appworx\n\n## Purpose\n\nTo simplify\n\n## Requirements\n\n- Python 3.8+\n\n## Usage\n\n```py\nfrom bearparse import Argument, ArgumentParser\n\n# Create the parser\nparser = ArgumentParser(description="Program Description")\nparser.add_argument(Argument(name="arg", description="First Argument"))\nparser.add_argument(Argument(name="arg2", description="Required Argument", required=True))\n\n# Parse from argv\nargs = parser.parse_args()\n\nprint(args.parsed)\n```\n',
    'author': 'Zevaryx',
    'author_email': 'zevaryx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.zevaryx.com/zevaryx/bearparse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
