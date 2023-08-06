# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gopos', 'gopos.models']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.2.0,<2.0.0', 'requests>=2.21.0,<3.0.0']

setup_kwargs = {
    'name': 'gopos',
    'version': '1.0.0',
    'description': 'Python bindings for gopos (https://github.com/thepieterdc/gopos).',
    'long_description': '# gopos-python\nPython bindings for gopos (https://github.com/thepieterdc/gopos).\n',
    'author': 'Pieter De Clercq',
    'author_email': 'pieterdeclercq@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thepieterdc/gopos-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
