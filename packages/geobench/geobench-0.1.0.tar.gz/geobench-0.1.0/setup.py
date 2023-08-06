# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geobench']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0']

setup_kwargs = {
    'name': 'geobench',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Qing Yin',
    'author_email': 'qingbyin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
