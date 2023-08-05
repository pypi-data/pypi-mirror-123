# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['roboworld']

install_requires = \
    ['matplotlib>=3.2.1,<4.0.0', 'rich>=3.3.1,<4.0.0']

package_data = \
    {'': ['*']}

setup_kwargs = {
    'name': 'roboworld',
    'version': '0.1.0',
    'description': 'A Python library to learn loops',
    'author': 'Benedikt Zoennchen',
    'author_email': 'benedikt.zoennchen@web.de',
    'maintainer': 'BZoennchen',
    'maintainer_email': 'benedikt.zoennchen@web.de',
    'url': 'https://github.com/BZoennchen/robo-world',
    'packages': packages,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}

setup(**setup_kwargs)
