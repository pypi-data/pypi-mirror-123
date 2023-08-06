# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easydrop']

package_data = \
{'': ['*'], 'easydrop': ['bins/*']}

install_requires = \
['click>=8.0.0,<9.0.0', 'loguru>=0.5.3,<0.6.0', 'opendrop>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'easydrop',
    'version': '0.0.1a1',
    'description': 'Tool that makes using AirDrop on Linux *easy*',
    'long_description': "# easydrop\n\nEasily share files through AirDrop *without a Mac*\n\n\n`easydrop` is a simple cli utility that's ment for quick and easy ~~send~~/receive files with AirDrop on ~~Windoza~~/Linux\n\n// Strikethough words are stuff that doesn't work yet tho I would really want it to\n\n## Credits\n\nThis is a very simple wrapper around much much bigger work of guys @seemoo-lab - it uses [owl](https://github.com/seemoo-lab/owl) for low-level AirDrop network layer as well as [opendrop](https://github.com/seemoo-lab/opendrop) for some app level - HUGE shout-out for them for reverse enineering all of this!!!\n\n// Note: tho I'm thinking of also forking `opendrop` in future for better control over the flow\n\n\n",
    'author': 'TheLastGimbus',
    'author_email': 'mateusz.soszynski@tuta.io',
    'maintainer': 'TheLastGimbus',
    'maintainer_email': 'mateusz.soszynski@tuta.io',
    'url': 'https://github.com/TheLastGimbus/easydrop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
