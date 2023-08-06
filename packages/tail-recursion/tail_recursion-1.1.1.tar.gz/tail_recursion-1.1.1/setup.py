# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tail_recursion']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tail-recursion',
    'version': '1.1.1',
    'description': 'Tail call recursion in Python',
    'long_description': None,
    'author': 'Incomplete',
    'author_email': 'incomplete@aixon.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
