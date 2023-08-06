# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioridwell']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'aioridwell',
    'version': '0.0.1',
    'description': 'DESCRIPTION GOES HERE',
    'long_description': '# 🚰 package_name: DESCRIPTION\n\n[![CI](https://github.com/bachya/package_name/workflows/CI/badge.svg)](https://github.com/bachya/package_name/actions)\n[![PyPi](https://img.shields.io/pypi/v/package_name.svg)](https://pypi.python.org/pypi/package_name)\n[![Version](https://img.shields.io/pypi/pyversions/package_name.svg)](https://pypi.python.org/pypi/package_name)\n[![License](https://img.shields.io/pypi/l/package_name.svg)](https://github.com/bachya/package_name/blob/master/LICENSE)\n[![Code Coverage](https://codecov.io/gh/bachya/package_name/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/package_name)\n[![Maintainability](https://api.codeclimate.com/v1/badges/a03c9e96f19a3dc37f98/maintainability)](https://codeclimate.com/github/bachya/package_name/maintainability)\n[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)\n\nDESCRIPTION\n\n- [Installation](#installation)\n- [Python Versions](#python-versions)\n- [Usage](#usage)\n- [Commands](#commands)\n- [Contributing](#contributing)\n\n# Installation\n\n```python\npip install package_name\n```\n\n# Python Versions\n\n`package_name` is currently supported on:\n\n* Python 3.8\n* Python 3.9 \n\n# Usage\n\n# Contributing\n\n1. [Check for open features/bugs](https://github.com/bachya/package_name/issues)\n  or [initiate a discussion on one](https://github.com/bachya/package_name/issues/new).\n2. [Fork the repository](https://github.com/bachya/package_name/fork).\n3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`\n4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`\n5. Install the dev environment: `script/setup`\n6. Code your new feature or bug fix.\n7. Write tests that cover your new functionality.\n8. Run tests and ensure 100% code coverage: `script/test`\n9. Update `README.md` with any new documentation.\n10. Add yourself to `AUTHORS.md`.\n11. Submit a pull request!\n',
    'author': 'Aaron Bach',
    'author_email': 'bachya1208@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bachya/aioridwell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
