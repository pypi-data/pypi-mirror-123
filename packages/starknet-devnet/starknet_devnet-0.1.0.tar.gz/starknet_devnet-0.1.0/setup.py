# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['starknet_devnet']

package_data = \
{'': ['*']}

install_requires = \
['Flask[async]>=2.0.2,<3.0.0', 'cairo-lang>=0.4.2,<0.5.0']

entry_points = \
{'console_scripts': ['starknet-devnet = starknet_devnet.server:main']}

setup_kwargs = {
    'name': 'starknet-devnet',
    'version': '0.1.0',
    'description': 'A local testnet for Starknet',
    'long_description': None,
    'author': 'FabijanC',
    'author_email': 'fabijan.corak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
