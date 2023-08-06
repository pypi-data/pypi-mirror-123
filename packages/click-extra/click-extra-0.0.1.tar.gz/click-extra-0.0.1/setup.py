# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['click_extra', 'click_extra.tests']

package_data = \
{'': ['*']}

install_requires = \
['boltons>=21.0.0,<22.0.0',
 'click>=8.0.2,<9.0.0',
 'cloup>=0.12.1,<0.13.0',
 'tomli>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'click-extra',
    'version': '0.0.1',
    'description': '🌈 Extra colorization and configuration file for Click.',
    'long_description': '# Click Extra\n\n[![Last release](https://img.shields.io/pypi/v/click-extra.svg)](https://pypi.python.org/pypi/click-extra)\n[![Python versions](https://img.shields.io/pypi/pyversions/click-extra.svg)](https://pypi.python.org/pypi/click-extra)\n[![Unittests status](https://github.com/kdeldycke/click-extra/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/kdeldycke/click-extra/actions/workflows/tests.yaml?query=branch%3Amain)\n[![Coverage status](https://codecov.io/gh/kdeldycke/click-extra/branch/main/graph/badge.svg)](https://codecov.io/gh/kdeldycke/click-extra/branch/main)\n\n**What is Click Extra?**\n\n`click-extra` is a collection of helpers and utilities for\n[Click](https://click.palletsprojects.com), the Python CLI framework.\n\nIt mainly consist of hacks, workarounds and other patches that have not reached\nupstream yet. Or are unlikely to be accepted upstream.\n\n## Installation\n\nInstall `click-extra` with `pip`:\n\n```shell-session\n$ pip install click-extra\n```\n\n## Features\n\n- Platform recognition utilities\n- `unless_linux`, `unless_macos`, `unless_windows` markers for `pytest`\n- `destructive` and `non_destructive` markers for `pytest`\n\n## Dependencies\n\nHere is a graph of Python package dependencies:\n\n![click-extra dependency graph](https://github.com/kdeldycke/click-extra/blob/main/dependencies.png)\n\n## Development\n\n[Development guidelines](https://kdeldycke.github.io/meta-package-manager/development.html)\nare the same as\n[parent project `mpm`](https://github.com/kdeldycke/meta-package-manager), from\nwhich `click-extra` originated.\n',
    'author': 'Kevin Deldycke',
    'author_email': 'kevin@deldycke.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kdeldycke/click-extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
