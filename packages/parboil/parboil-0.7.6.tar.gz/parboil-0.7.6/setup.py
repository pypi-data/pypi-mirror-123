# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parboil']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0', 'click>=8.0.3,<9.0.0', 'colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'parboil',
    'version': '0.7.6',
    'description': 'Create reusable boilerplate templates to kickstart your next project.',
    'long_description': None,
    'author': 'J. Neugebauer',
    'author_email': 'github@neugebauer.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
