# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bqsc']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.910,<0.911']

setup_kwargs = {
    'name': 'bqsc',
    'version': '1.0.1',
    'description': 'Define schema object from bigquery schema definition json file',
    'long_description': None,
    'author': 'Yasunori Horikoshi',
    'author_email': 'hotoku@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
