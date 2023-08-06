# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'envex',
    'version': '1.0.1',
    'description': 'An extended os.environ interface',
    'long_description': None,
    'author': 'David Nugent',
    'author_email': 'davidn@uniquode.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
