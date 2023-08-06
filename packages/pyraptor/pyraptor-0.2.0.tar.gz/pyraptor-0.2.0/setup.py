# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyraptor', 'pyraptor.dao', 'pyraptor.gtfs', 'pyraptor.model']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0.1,<2.0.0', 'loguru>=0.5.3,<0.6.0', 'pandas>=1.3.2,<2.0.0']

setup_kwargs = {
    'name': 'pyraptor',
    'version': '0.2.0',
    'description': 'Journey planner with RAPTOR algorithm',
    'long_description': None,
    'author': 'Leo van der Meulen, Thom Hopmans',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
