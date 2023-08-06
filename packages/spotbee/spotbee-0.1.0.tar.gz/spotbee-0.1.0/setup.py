# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spotbee']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'spotipy>=2.19.0,<3.0.0']

setup_kwargs = {
    'name': 'spotbee',
    'version': '0.1.0',
    'description': 'A simple module that converts Spotify Playlists into a list of Youtube URLs',
    'long_description': None,
    'author': 'Nishant Sapkota',
    'author_email': 'snishant306@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
