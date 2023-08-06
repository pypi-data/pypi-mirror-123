# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phevaluator', 'phevaluator.tables']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'phevaluator',
    'version': '0.4.0.2',
    'description': 'Poker-Hand-Evaluator: An efficient poker hand evaluation algorithm and its implementation, supporting 7-card poker and Omaha poker evaluation',
    'long_description': None,
    'author': 'Henry Lee',
    'author_email': 'lee0906@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
