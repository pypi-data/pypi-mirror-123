# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_cd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-cd',
    'version': '0.6.3',
    'description': '',
    'long_description': None,
    'author': 'dylandoamaral',
    'author_email': 'do.amaral.dylan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
