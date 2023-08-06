# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['epaper', 'epaper.e-Paper.RaspberryPi_JetsonNano.python.lib.waveshare_epd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'waveshare-epaper',
    'version': '0.6.0',
    'description': '',
    'long_description': None,
    'author': 'yskoht',
    'author_email': 'ysk.oht@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
