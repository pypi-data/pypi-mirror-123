# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdpaper']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.7,<4.0.0',
 'invoke>=1.6.0,<2.0.0',
 'pandoc-docx-pagebreak>=0.0.2,<0.0.3',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['md-paper = mdpaper.main:app',
                     'pandoc-docxtras = mdpaper.filters:main']}

setup_kwargs = {
    'name': 'mdpaper',
    'version': '0.0.1',
    'description': 'A package for organizing and compiling a thesis type document with markdown.',
    'long_description': None,
    'author': 'Thomas Tu',
    'author_email': 'thomasthetu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
