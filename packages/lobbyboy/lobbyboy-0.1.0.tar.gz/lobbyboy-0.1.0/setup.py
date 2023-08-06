# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lobbyboy']

package_data = \
{'': ['*']}

install_requires = \
['paramiko[gssapi]>=2.8.0,<3.0.0']

setup_kwargs = {
    'name': 'lobbyboy',
    'version': '0.1.0',
    'description': 'Give me a server.',
    'long_description': None,
    'author': 'laixintao',
    'author_email': 'laixintaoo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
