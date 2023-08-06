# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redcap_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'redcap-client',
    'version': '0.1.2',
    'description': 'A fork of seattleflu/id3c containing only the redcap Project client',
    'long_description': None,
    'author': 'Tom Thorogood',
    'author_email': 'goodtom@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
