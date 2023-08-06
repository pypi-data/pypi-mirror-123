# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaffine']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'python-datamuse==1.3.0']

entry_points = \
{'console_scripts': ['affine = pyaffine.main:start']}

setup_kwargs = {
    'name': 'pyaffine',
    'version': '0.2.0',
    'description': 'Thesaurus which uses the Datamuse API.',
    'long_description': 'Thesaurus which access the [Datamuse API](https://www.datamuse.com/api).\n\n## Installation\n```bash\npip install pyaffine\n```\n\n## Example\n```bash\naffine motivate\n```\nwill return synonyms for "motivate".\n\n![](https://i.imgur.com/kIgqZRC.png)\n',
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
