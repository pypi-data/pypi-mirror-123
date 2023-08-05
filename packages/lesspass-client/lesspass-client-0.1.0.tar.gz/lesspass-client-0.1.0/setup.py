# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lesspass_client']

package_data = \
{'': ['*']}

install_requires = \
['lesspass>=10.0.2,<11.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['lesspass-client = lesspass_client.cli:main']}

setup_kwargs = {
    'name': 'lesspass-client',
    'version': '0.1.0',
    'description': 'A LessPass API client written in Python',
    'long_description': None,
    'author': 'Kyle Williams',
    'author_email': 'kyle.anthony.williams2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
