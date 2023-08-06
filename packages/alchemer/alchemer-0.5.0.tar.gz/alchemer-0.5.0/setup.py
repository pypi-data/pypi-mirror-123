# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alchemer']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'alchemer',
    'version': '0.5.0',
    'description': '',
    'long_description': None,
    'author': 'Charlie Bini',
    'author_email': '5003326+cbini@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
