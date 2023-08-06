# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['astraszab_hypermodern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.2,<9.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.13.0,<4.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['hypermodern-python = '
                     'astraszab_hypermodern_python.console:main']}

setup_kwargs = {
    'name': 'astraszab-hypermodern-python',
    'version': '0.1.0',
    'description': 'The hypermodern Python project',
    'long_description': '[![Tests](https://github.com/astraszab/astraszab-hypermodern-python/workflows/Tests/badge.svg)](https://github.com/astraszab/astraszab-hypermodern-python/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/astraszab/astraszab-hypermodern-python/branch/master/graph/badge.svg)](https://codecov.io/gh/astraszab/astraszab-hypermodern-python)\n\n# astraszab-hypermodern-python\n',
    'author': 'astraszab',
    'author_email': 'u.astraszab@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astraszab/astraszab-hypermodern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
