# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atrends']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.3,<4.0.0', 'pytrends>=4.7.3,<5.0.0']

entry_points = \
{'console_scripts': ['atrends = atrends.main:start',
                     'trends = atrends.main:start']}

setup_kwargs = {
    'name': 'atrends',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'davidshivaji',
    'author_email': 'davidshivaji@gmail.com',
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
