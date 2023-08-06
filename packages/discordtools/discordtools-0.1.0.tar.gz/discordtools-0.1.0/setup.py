# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['discordtools']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'discord.py>=1.7.3,<2.0.0', 'rich>=10.12.0,<11.0.0']

entry_points = \
{'console_scripts': ['discordtools = discordtools.cli:cli']}

setup_kwargs = {
    'name': 'discordtools',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marco Rougeth',
    'author_email': 'pypi@rougeth.com',
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
