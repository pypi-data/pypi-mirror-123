# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rcbm']

package_data = \
{'': ['*']}

install_requires = \
['pandas-stubs>=1.2,<2.0', 'pandas>=1.0,<2.0', 'pandera>=0.7.2,<0.8.0']

setup_kwargs = {
    'name': 'rcbm',
    'version': '0.2.3',
    'description': 'A Resistance Capacitance (RC) Model for the Simulation of Building Stock Energy Usage',
    'long_description': None,
    'author': 'Rowan Molony',
    'author_email': 'rowan.molony@codema.ie',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/codema-dev/rc-building-model',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
