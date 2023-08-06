# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['interval_tool']

package_data = \
{'': ['*']}

install_requires = \
['tail-recursion>=1.1.1']

setup_kwargs = {
    'name': 'interval-tool',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Incomplete',
    'author_email': 'incomplete@aixon.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
