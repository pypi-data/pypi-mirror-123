# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpha_galaxy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'alpha-galaxy',
    'version': '0.1.0',
    'description': 'Alpha Galaxy is a framework of quantitative analysis development',
    'long_description': None,
    'author': 'ZhengYu, Xu',
    'author_email': 'zen-xu@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
