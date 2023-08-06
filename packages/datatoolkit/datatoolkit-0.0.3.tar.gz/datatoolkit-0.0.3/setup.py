# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datatoolkit']

package_data = \
{'': ['*']}

install_requires = \
['bokeh>=2.4.0,<3.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'statsmodels>=0.13.0,<0.14.0',
 'typeguard>=2.12.1,<3.0.0']

setup_kwargs = {
    'name': 'datatoolkit',
    'version': '0.0.3',
    'description': 'A collection of tools for visualization and data processing for exploratory data analysis',
    'long_description': '[![DOI](https://zenodo.org/badge/408053914.svg)](https://zenodo.org/badge/latestdoi/408053914)\n\n# Datatoolkit\n\nA collection of tools for visualization and data processing for exploratory data analysis.',
    'author': 'Humberto STEIN SHIROMOTO',
    'author_email': 'h.stein.shiromoto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
