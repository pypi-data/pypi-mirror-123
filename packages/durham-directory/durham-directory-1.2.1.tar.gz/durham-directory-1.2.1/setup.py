# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['durham_directory']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'lxml>=4.6.3,<5.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['durham-directory = durham_directory:main']}

setup_kwargs = {
    'name': 'durham-directory',
    'version': '1.2.1',
    'description': 'Python Bindings for the Durham University (UK) Directory',
    'long_description': None,
    'author': 'John Maximilian',
    'author_email': '2e0byo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
