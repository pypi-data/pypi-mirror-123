# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['njet', 'njet..ipynb_checkpoints']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0', 'sympy>=1.8,<2.0']

setup_kwargs = {
    'name': 'njet',
    'version': '0.1.2',
    'description': 'Lightweight automatic differentiation package for higher-order differentiation.',
    'long_description': None,
    'author': 'Malte Titze',
    'author_email': 'mtitze@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://njet.readthedocs.io/en/latest/index.html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
