# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['export_util', 'export_util.test', 'export_util.utility']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.9,<4.0.0',
 'reportlab>=3.6.1,<4.0.0',
 'schematics>=2.1.1,<3.0.0']

setup_kwargs = {
    'name': 'export-lib',
    'version': '0.4',
    'description': '',
    'long_description': None,
    'author': 'bmat tvav',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
