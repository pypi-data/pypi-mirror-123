# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scratch_text_to_nums']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'scratch-text-to-nums',
    'version': '0.1.2',
    'description': 'Encodes strings to send to the Scratch cloud',
    'long_description': None,
    'author': 'joecooldoo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
