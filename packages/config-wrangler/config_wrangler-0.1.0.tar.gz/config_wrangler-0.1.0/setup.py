# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['config_wrangler',
 'config_wrangler.config_data_loaders',
 'config_wrangler.config_templates',
 'config_wrangler.types']

package_data = \
{'': ['*']}

install_requires = \
['StrEnum>=0.4.7,<0.5.0', 'pydantic>=1.8.2,<2.0.0']

extras_require = \
{'sqlalchemy': ['SQLAlchemy>=1.4,<2.0']}

setup_kwargs = {
    'name': 'config-wrangler',
    'version': '0.1.0',
    'description': 'pydantic based configuration wrangler.\nHandles reading multiple ini or toml files with inheritance rules and variable expansions.\n',
    'long_description': None,
    'author': 'Derek Wood',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
