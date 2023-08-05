# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datagrep', 'datagrep.platform']

package_data = \
{'': ['*'],
 'datagrep': ['{{cookiecutter.project_slug}}/*',
              '{{cookiecutter.project_slug}}/docs/*',
              '{{cookiecutter.project_slug}}/services/caddy/*']}

install_requires = \
['click>=7.1.1,<7.2.0',
 'cookiecutter>=1.7.3,<2.0.0',
 'plumbum>=1.7.0,<2.0.0',
 'typer[all]>=0.3,<0.4']

entry_points = \
{'console_scripts': ['datagrep = datagrep.main:app',
                     'dgp = datagrep.platform.main:app']}

setup_kwargs = {
    'name': 'datagrep',
    'version': '3.0.1a6',
    'description': 'The datagrep CLI.',
    'long_description': '# datagrep\n\n[![Documentation Status](https://readthedocs.org/projects/datagrep/badge/?version=latest)](https://datagrep.readthedocs.io/en/latest/?badge=latest)\n\nThe datagrep CLI.\n',
    'author': 'Michael Schock',
    'author_email': 'm@mjschock.com',
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
