# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sapiclient']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'sapiclient',
    'version': '0.2.85905',
    'description': '',
    'long_description': None,
    'author': 'Zafar Iqbal',
    'author_email': 'zaf@sparc.space',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
