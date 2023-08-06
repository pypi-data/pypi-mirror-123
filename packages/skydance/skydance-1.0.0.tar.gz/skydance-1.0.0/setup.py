# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skydance', 'skydance.network', 'skydance.tests', 'skydance.tests.network']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'skydance',
    'version': '1.0.0',
    'description': 'A library for communication with Skydance Wi-Fi relays.',
    'long_description': '# Overview\n\nA library for communication with Skydance Wi-Fi relays.\n\n[![Build Status](https://img.shields.io/travis/tomasbedrich/skydance.svg)](https://travis-ci.org/tomasbedrich/skydance)\n[![Coverage Status](https://img.shields.io/coveralls/tomasbedrich/skydance.svg)](https://coveralls.io/r/tomasbedrich/skydance)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/tomasbedrich/skydance.svg)](https://scrutinizer-ci.com/g/tomasbedrich/skydance)\n[![PyPI Version](https://img.shields.io/pypi/v/skydance.svg)](https://pypi.org/project/skydance)\n[![PyPI License](https://img.shields.io/pypi/l/skydance.svg)](https://pypi.org/project/skydance)\n\nThe original product is [a Wi-Fi to RF gateway](http://www.iskydance.com/index.php?c=product_show&a=index&id=810) manufactured by Skydance Co. China.\n\nSometimes, it is re-branded under different names. For example, in the Czech Republic, [it is sold](https://www.t-led.cz/p/ovladac-wifi-dimled-69381) as "dimLED" system.\n\nThis aim of this library is to roughly cover capabilities of [the official SkySmart Android application](https://play.google.com/store/apps/details?id=com.lxit.wifirelay&hl=cs&gl=US).\n\n# Setup\n\n## Requirements\n\n* Python 3.8+\n\n## Installation\n\n```text\n$ pip install skydance\n```\n\n# Usage\n\nThe protocol implementation is [Sans I/O](https://sans-io.readthedocs.io/).\nYou must create the connection and send the byte payloads on your own.\nThere are some helpers in `skydance.network` built on top of Python\'s asyncio which helps you to wrap the I/O.\n\nTODO - In meantime, please see `test/test_manual.py`.\n\n# Links\n- [Home Assistant reverse engineering forum thread](https://community.home-assistant.io/t/skydance-2-4g-rf/99399)\n',
    'author': 'Tomas Bedrich',
    'author_email': 'ja@tbedrich.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/skydance',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
