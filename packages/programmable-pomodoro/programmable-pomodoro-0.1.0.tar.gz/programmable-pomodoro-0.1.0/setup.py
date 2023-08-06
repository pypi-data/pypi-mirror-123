# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['programmable_pomodoro']

package_data = \
{'': ['*'], 'programmable_pomodoro': ['audio/*']}

install_requires = \
['aioconsole>=0.3.2,<0.4.0',
 'colorama>=0.4.4,<0.5.0',
 'simpleaudio>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'programmable-pomodoro',
    'version': '0.1.0',
    'description': 'A programmable pomodoro timer.',
    'long_description': None,
    'author': 'Matthew Caseres',
    'author_email': 'matthewcaseres@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
