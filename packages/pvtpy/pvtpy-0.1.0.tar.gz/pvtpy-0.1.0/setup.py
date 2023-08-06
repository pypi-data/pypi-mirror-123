# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pvtpy',
 'pvtpy.black_oil',
 'pvtpy.compositional',
 'pvtpy.eos',
 'pvtpy.fluids',
 'pvtpy.pvt',
 'pvtpy.units']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.20.3,<2.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'scipy==1.6.1',
 'seaborn>=0.11.1,<0.12.0',
 'statsmodels>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'pvtpy',
    'version': '0.1.0',
    'description': 'Oil&Gas PVT Tool',
    'long_description': None,
    'author': 'scuervo',
    'author_email': 'scuervo91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
