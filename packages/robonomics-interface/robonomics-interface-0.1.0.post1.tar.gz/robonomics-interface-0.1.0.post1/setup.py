# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['robonomicsinterface']

package_data = \
{'': ['*']}

install_requires = \
['substrate-interface>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'robonomics-interface',
    'version': '0.1.0.post1',
    'description': 'Robonomics wrapper over https://github.com/polkascan/py-substrate-interface created to facilitate programming with Robonomics',
    'long_description': None,
    'author': 'Pavel Tarasov',
    'author_email': 'p040399@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Multi-Agent-io/robonomics-interface',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6,<4.0',
}


setup(**setup_kwargs)
