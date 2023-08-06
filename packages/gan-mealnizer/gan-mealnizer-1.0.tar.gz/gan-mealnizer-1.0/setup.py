# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gan_mealnizer']

package_data = \
{'': ['*'], 'gan_mealnizer': ['data/*']}

install_requires = \
['typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['gan-mealnizer = gan_mealnizer.main:app']}

setup_kwargs = {
    'name': 'gan-mealnizer',
    'version': '1.0',
    'description': '',
    'long_description': '',
    'author': 'Gan Mahmud',
    'author_email': 'ganmahmud@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
