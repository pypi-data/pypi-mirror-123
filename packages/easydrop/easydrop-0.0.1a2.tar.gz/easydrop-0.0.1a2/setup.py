# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['easydrop']

package_data = \
{'': ['*'], 'easydrop': ['bins/*']}

install_requires = \
['click>=8.0.0,<9.0.0',
 'ifaddr>=0.1.7,<0.2.0',
 'loguru>=0.5.3,<0.6.0',
 'opendrop>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'easydrop',
    'version': '0.0.1a2',
    'description': 'Tool that makes using AirDrop on Linux *easy*',
    'long_description': '# easydrop\n\nEasily share files through AirDrop *without a Mac*\n\n[![PyPI](https://img.shields.io/pypi/v/easydrop)](https://pypi.org/project/easydrop/)\n[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg?logo=paypal)](https://www.paypal.me/TheLastGimbus)\n\n`easydrop` is a simple cli utility for quick and easy ~~sending~~/receiving files with AirDrop on ~~Windoza~~/Linux\n\n// Strikethrough words are stuff that doesn\'t work yet tho I would really want it to\n\n## Using\n0. Make sure you have [everything required](#supported-hardware-and-platforms)\n1. `pip install -U easydrop`\n2. Receive files:\n    ```bash\n    $ easydrop receive\n    sudo password:  # Password to manage network interfaces\n    22:01:51 Hang tight! Disabling normal WiFi...  # easydrop will disable your normal network when running\n    22:01:52 Starting OWL...\n    22:01:54 OWL running!\n    22:01:55 Starting HTTP server - press CTRL+C to stop...\n    ^C22:01:59 Stopping OWL...\n    22:01:59 Restarting network...  # ...but will bring it back up after it\'s done!\n    Aborted!\n    ```\n3. Send files: not yet implemented :disappointed:\n\n## Credits\n\nThis is a very simple wrapper around much much bigger work of guys @seemoo-lab - it uses [owl](https://github.com/seemoo-lab/owl) for low-level AirDrop network layer as well as [opendrop](https://github.com/seemoo-lab/opendrop) for some app level - HUGE shout-out for them for reverse enineering all of this!!!\n\n## Supported hardware and platforms\n\nAs noted on [owl repo](https://github.com/seemoo-lab/owl/#requirements), you need WiFi card that supports *active* monitor mode - you can quickly check it by running:\n```bash\n$ iw list | grep "active monitor"\n# You should see:\n> \tDevice supports active monitor (which will ACK incoming frames)\n```\nIf you don\'t have it, then I\'m sorry, but it probably won\'t work :disappointed:\n\nFor now, `easydrop` only works on Linux (amd64 arch) (`owl` itself works on MacOS too, but you already have AirDrop there :laugh:)\n\nYou will also need to install `libpcap`, `libev` and `libnl`:\n- on Debian: `sudo apt install libpcap-dev libev-dev libnl-3-dev libnl-genl-3-dev libnl-route-3-dev`\n- on Fedora: `sudo dnf install libpcap-devel libev-devel libnl3-devel`\n- on other distros: idk, you can do it :muscle:\n\n`owl` is already included in the package :wink:\n\n// TODO: Include those dependencies in package\n\n\n## TODO:\n- [ ] Sending files - may require more work to also [advertise BLE beacons to wake up receivers](https://github.com/seemoo-lab/opendrop/issues/30)\n- [ ] Windoza\n',
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
