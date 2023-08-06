# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google-stubs']

package_data = \
{'': ['*'],
 'google-stubs': ['auth/*',
                  'auth/compute_engine/*',
                  'auth/crypt/*',
                  'auth/transport/*',
                  'oauth2/*']}

install_requires = \
['google-auth>=2.3.0,<3.0.0',
 'grpc-stubs>=1.24.7,<2.0.0',
 'types-requests>=2.25.9,<3.0.0']

setup_kwargs = {
    'name': 'google-auth-stubs',
    'version': '0.1.0',
    'description': 'Type stubs for google-auth',
    'long_description': '# Type stubs for google-auth-stubs\n[![PyPI version](https://badge.fury.io/py/google-auth-stubs.svg)](https://badge.fury.io/py/google-auth-stubs)\n\nThis package provides type stubs for the [google-auth](https://pypi.org/project/google-auth/) package.\n\n**This is in no way affiliated with Google.**\n\nThe stubs were created automatically by [stubgen](https://mypy.readthedocs.io/en/stable/stubgen.html).\n\n## Installation\n```shell script\n$ pip install google-auth-stubs\n```\n',
    'author': 'Henrik Bruåsdal',
    'author_email': 'henrik.bruasdal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/henribru/google-auth-stubs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
