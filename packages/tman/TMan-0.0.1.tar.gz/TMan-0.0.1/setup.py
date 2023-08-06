# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'tman', 'tman.backend', 'tman.cli', 'tman.gui', 'tman.util']

package_data = \
{'': ['*']}

install_requires = \
['PySimpleGUI>=4.49.0,<5.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'attrs>=21.2.0,<22.0.0',
 'click>=8.0.1,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.8.2,<2.0.0']

extras_require = \
{'dev': ['bump2version>=1.0.1,<2.0.0',
         'pip>=20.3.1,<21.0.0',
         'pre-commit>=2.12.0,<3.0.0',
         'toml>=0.10.2,<0.11.0',
         'tox>=3.20.1,<4.0.0',
         'twine>=3.3.0,<4.0.0',
         'virtualenv>=20.2.2,<21.0.0'],
 'doc': ['mkdocs>=1.1.2,<2.0.0',
         'mkdocs-autorefs>=0.3.0,<0.4.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=7.3.3,<8.0.0',
         'mkdocs-material-extensions>=1.0.1,<2.0.0',
         'mkdocstrings>=0.16.2,<0.17.0'],
 'test': ['black>=21.5b2,<22.0',
          'flake8>=4.0.1,<5.0.0',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'hypothesis>=6.23.2,<7.0.0',
          'isort>=5.8.0,<6.0.0',
          'mypy>=0.910,<0.911',
          'pytest>=6.2.4,<7.0.0',
          'pytest-cov>=3.0.0,<4.0.0',
          'types-appdirs>=1.4.1,<2.0.0',
          'types-attrs>=19.1.0,<20.0.0',
          'types-click>=7.1.7,<8.0.0',
          'types-setuptools>=57.4.2,<58.0.0']}

entry_points = \
{'console_scripts': ['tman = tman.cli:main', 'tman-gui = tman.gui:main']}

setup_kwargs = {
    'name': 'tman',
    'version': '0.0.1',
    'description': 'TODO',
    'long_description': '# TMan\n\n\n[![pypi](https://img.shields.io/pypi/v/TMan.svg)](https://pypi.org/project/TMan/)\n[![python](https://img.shields.io/pypi/pyversions/TMan.svg)](https://pypi.org/project/TMan/)\n[![Build Status](https://github.com/Danmou/TMan/actions/workflows/dev.yml/badge.svg)](https://github.com/Danmou/TMan/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/Danmou/TMan/branch/main/graphs/badge.svg)](https://codecov.io/github/Danmou/TMan)\n\n\n\nSkeleton project created by Cookiecutter PyPackage\n\n\n* Documentation: <https://Danmou.github.io/TMan>\n* GitHub: <https://github.com/Danmou/TMan>\n* PyPI: <https://pypi.org/project/TMan/>\n* Free software: GPL-3.0-only\n\n\n## Features\n\n* TODO\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Daniel Mouritzen',
    'author_email': 'dmrtzn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Danmou/TMan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<4.0',
}


setup(**setup_kwargs)
