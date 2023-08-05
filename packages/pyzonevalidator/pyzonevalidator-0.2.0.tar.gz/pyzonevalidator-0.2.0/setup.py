# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzonevalidator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyzonevalidator',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Teun Ouwehand',
    'author_email': 'teun@nextpertise.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
