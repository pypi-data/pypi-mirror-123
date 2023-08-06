# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['raspberry_epaper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'raspberry-epaper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'yskoht',
    'author_email': 'ysk.oht@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
