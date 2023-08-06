# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snap2py']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'snap2py',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'joecooldoo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
