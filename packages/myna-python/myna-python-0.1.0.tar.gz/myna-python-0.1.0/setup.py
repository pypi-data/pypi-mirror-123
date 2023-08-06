# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['myna']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=35.0.0,<36.0.0', 'pyscard>=2.0.2,<3.0.0', 'typer>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'myna-python',
    'version': '0.1.0',
    'description': 'cli-tool/library for interacting with the 個人番号カード',
    'long_description': None,
    'author': 'Yuichiro Smith',
    'author_email': 'contact@yu-smith.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
