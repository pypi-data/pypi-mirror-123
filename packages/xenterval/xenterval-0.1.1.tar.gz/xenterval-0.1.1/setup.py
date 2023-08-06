# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xenterval', 'xenterval.interval', 'xenterval.interval.name']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.6.0,<9.0.0']

setup_kwargs = {
    'name': 'xenterval',
    'version': '0.1.1',
    'description': 'Xenharmonic theory utilities and more.',
    'long_description': '# xenterval\n\nXenharmonic theory utilities and more.\n\n## Usage\n\n`import xenterval`\n',
    'author': 'arseniiv',
    'author_email': 'arseniiv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arseniiv/xenterval',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
