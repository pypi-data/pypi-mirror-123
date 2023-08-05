# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omniclient']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'omniclient',
    'version': '0.5.14597',
    'description': '',
    'long_description': None,
    'author': 'Zafar Iqbal',
    'author_email': 'ultrasine@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
