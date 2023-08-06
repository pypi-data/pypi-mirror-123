# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyades',
 'hyades.connection',
 'hyades.connection.wrappers',
 'hyades.device',
 'hyades.inventory',
 'hyades.parsers',
 'hyades.parsers.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['asyncssh>=2.7.2,<3.0.0',
 'genie>=21.7,<22.0',
 'netmiko>=3.4.0,<4.0.0',
 'pyats>=21.7,<22.0',
 'scrapli-community>=2021.7.30,<2022.0.0',
 'scrapli[ssh2]>=2021.7.30,<2022.0.0']

setup_kwargs = {
    'name': 'hyades',
    'version': '0.1.0',
    'description': 'Network Automation Inventory',
    'long_description': None,
    'author': 'Renato Almeida de Oliveira',
    'author_email': 'renato.almeida.oliveira@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
