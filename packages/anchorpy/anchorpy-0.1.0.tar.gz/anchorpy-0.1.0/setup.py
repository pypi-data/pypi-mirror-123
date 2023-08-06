# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['anchorpy', 'anchorpy.coder', 'anchorpy.program', 'anchorpy.program.namespace']

package_data = \
{'': ['*']}

install_requires = \
['apischema>=0.15.6,<0.16.0',
 'borsh-construct-tmp>=0.1.0,<0.2.0',
 'construct-typing>=0.5.1,<0.6.0',
 'inflection>=0.5.1,<0.6.0',
 'solana>=0.16.0,<0.17.0',
 'sumtypes>=0.1a5,<0.2']

setup_kwargs = {
    'name': 'anchorpy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kevinheavey',
    'author_email': 'kevinheavey123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
