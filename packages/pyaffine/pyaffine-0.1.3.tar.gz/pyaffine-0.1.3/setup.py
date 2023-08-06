# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaffine']

package_data = \
{'': ['*']}

install_requires = \
['python-datamuse==1.3.0']

entry_points = \
{'console_scripts': ['affine = pyaffine:main']}

setup_kwargs = {
    'name': 'pyaffine',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'davidshivaji',
    'author_email': 'davidshivaji@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
