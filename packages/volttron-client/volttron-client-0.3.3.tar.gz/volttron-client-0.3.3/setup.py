# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volttron',
 'volttron.client',
 'volttron.client.messaging',
 'volttron.client.vip',
 'volttron.client.vip.agent',
 'volttron.client.vip.agent.subsystems',
 'volttron.commands']

package_data = \
{'': ['*']}

install_requires = \
['dateutils>=0.6,<0.7',
 'grequests>=0.6.0,<0.7.0',
 'idna>=2.5,<3',
 'requests>=2.26.0,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'volttron-utils>=0.3,<0.4']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['vctl = volttron.commands.control:main',
                     'volttron-ctl = volttron.commands.control:main']}

setup_kwargs = {
    'name': 'volttron-client',
    'version': '0.3.3',
    'description': 'Client for connecting to a volttron server',
    'long_description': None,
    'author': 'C. Allwardt',
    'author_email': 'craig.allwardt@pnnl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4',
}


setup(**setup_kwargs)
