# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djs3']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.8,<4.0.0', 'boto3>=1.18.59,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'djs3',
    'version': '2021.10.11',
    'description': 'S3 in Django',
    'long_description': None,
    'author': 'Atem18',
    'author_email': 'messer.kevin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
