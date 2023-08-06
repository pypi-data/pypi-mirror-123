# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jaxex']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0',
 'cloudpickle>=2.0.0,<3.0.0',
 'dm-haiku>=0.0.4,<0.0.5',
 'dm-tree>=0.1.6,<0.2.0',
 'gym>=0.20.0,<0.21.0',
 'jax>=0.2.21,<0.3.0',
 'jaxlib>=0.1.71,<0.2.0',
 'numpy>=1.21.2,<2.0.0',
 'optax>=0.0.9,<0.0.10',
 'pandas>=1.3.3,<2.0.0',
 'plotly>=5.3.1,<6.0.0',
 'pybullet>=3.1.9,<4.0.0',
 'pyglet>=1.5.21,<2.0.0',
 'torch>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'jaxex',
    'version': '0.0.0',
    'description': 'A tool for creating science experiments in jax, torch, brax, etc',
    'long_description': None,
    'author': 'LSaldyt',
    'author_email': 'lucassaldyt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
