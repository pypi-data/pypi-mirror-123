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
    'version': '0.1.2',
    'description': 'A PyTrends script to access the Google Trends API and return a plot.',
    'long_description': '# CLI for Google Trends\n\nUse this to quickly access the [Google Trends API](https://trends.google.com/trends/) via Command Line.\n\n## Installation\n```bash\npip install atrends\n```\n\n## Usage\n\n#### Run `trends` with any number of arguments\n\n## Example\n```bash\ntrends flask django react\n```\n\n![](https://i.imgur.com/JzzNAZU.png)\n\n## Custom:\nEdit the category, timeframe, colors, lines, in main.py\n',
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
