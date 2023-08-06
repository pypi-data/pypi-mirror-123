# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickpomdps']

package_data = \
{'': ['*']}

install_requires = \
['julia>=0.5,<0.6']

setup_kwargs = {
    'name': 'quickpomdps',
    'version': '0.1.0',
    'description': 'Describing and Solving POMDPs in Python',
    'long_description': None,
    'author': 'rejuvyesh',
    'author_email': 'mail@rejuvyesh.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
