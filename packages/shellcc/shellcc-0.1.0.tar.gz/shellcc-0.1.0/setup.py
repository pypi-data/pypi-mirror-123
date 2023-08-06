# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shellcc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shellcc',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'hattmo',
    'author_email': 'matthew@hattmo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
