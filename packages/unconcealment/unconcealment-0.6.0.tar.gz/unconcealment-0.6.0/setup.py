# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unconcealment']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0']

setup_kwargs = {
    'name': 'unconcealment',
    'version': '0.6.0',
    'description': 'unconcealment',
    'long_description': None,
    'author': 'adioss',
    'author_email': 'adrien.pailhes@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
