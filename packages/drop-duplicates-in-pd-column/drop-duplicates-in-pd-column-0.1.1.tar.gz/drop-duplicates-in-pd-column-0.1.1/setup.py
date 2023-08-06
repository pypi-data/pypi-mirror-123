# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drop_duplicates_in_pd_column']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'drop-duplicates-in-pd-column',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'ilikechicken67',
    'author_email': 'thomas.staats443@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
