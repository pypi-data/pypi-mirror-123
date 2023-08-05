# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitsubpull']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['gitsubpull = gitsubpull.main:app']}

setup_kwargs = {
    'name': 'gitsubpull',
    'version': '0.1.0',
    'description': '',
    'long_description': '## How to use\n\n1. cd to git project directory\n```shell\ncd ~/xxx/example/git_project/\n```\n\n2. run the command\n```shell\ngitsubpull\n```\n',
    'author': 'Jonathan Liew',
    'author_email': 'jonathan200934@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
