# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gmas']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gmas',
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
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
