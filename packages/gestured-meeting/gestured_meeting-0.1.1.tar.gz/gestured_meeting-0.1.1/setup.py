# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gestured_meeting', 'gestured_meeting.gesture', 'gestured_meeting.meeting']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.2,<9.0.0',
 'PyAutoGUI>=0.9.53,<0.10.0',
 'PyGObject>=3.42.0,<4.0.0',
 'bleak>=0.12.1,<0.13.0',
 'pystray>=0.17.3,<0.18.0']

entry_points = \
{'console_scripts': ['gestured-meeting = gestured_meeting:cli']}

setup_kwargs = {
    'name': 'gestured-meeting',
    'version': '0.1.1',
    'description': 'Online meeting with gesture.',
    'long_description': '<h1 align="center"><img src="./logo.svg" alt="Gestured Meeting" /></h1>\n\n<p align="center">\nOnline meeting with gesture.\n</p>\n\nLogo and icons are remixed [Heroicons](https://heroicons.com/) and [Twemoji](https://twemoji.twitter.com/).\n',
    'author': 'ygkn',
    'author_email': '2000ygkn0713@gmail.com',
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
