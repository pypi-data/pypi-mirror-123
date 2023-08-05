# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dis_snek',
 'dis_snek.http_requests',
 'dis_snek.mixins',
 'dis_snek.models',
 'dis_snek.models.discord_objects',
 'dis_snek.models.events',
 'dis_snek.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'attrs>=21.2.0,<22.0.0',
 'mypy>=0.910,<0.911',
 'sentinel[varname]>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'dis-snek',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'LordOfPolls',
    'author_email': 'ddavidallen13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
