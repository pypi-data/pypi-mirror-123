# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yamlizer']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'yamlizer',
    'version': '1.0.0',
    'description': 'Yamlizer simplifies loading (dumping) of custom Python objects from (to) yaml configuration files',
    'long_description': None,
    'author': 'Atharv Joshi',
    'author_email': 'atharvjoshi@ymail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
