# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_demo_1199']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.910,<0.911', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'poetry-demo-1199',
    'version': '0.1.0',
    'description': 'Demo of poetry for akashkj.com',
    'long_description': None,
    'author': 'Akash',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
