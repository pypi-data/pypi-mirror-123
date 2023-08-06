# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_poetry_123']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-poetry-123',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Robert Kowalski',
    'author_email': 'rkowalski@algopolis.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
