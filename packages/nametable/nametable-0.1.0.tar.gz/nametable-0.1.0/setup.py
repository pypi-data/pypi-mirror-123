# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nametable']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 'nametable',
    'version': '0.1.0',
    'description': 'An OOP approach to represent nametables on the NES',
    'long_description': None,
    'author': 'TheJoeSmo',
    'author_email': 'joesmo.joesmo12@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.7,<3.11',
}


setup(**setup_kwargs)
