# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tikbot', 'tikbot.handler', 'tikbot.handler.command']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'cattrs>=1.8.0,<2.0.0',
 'python-dotenv>=0.19.1,<0.20.0',
 'python-telegram-bot>=13.7,<14.0']

setup_kwargs = {
    'name': 'tikbot',
    'version': '0.1.0',
    'description': 'Telegram Bot for Mikrotik (RouterOS)',
    'long_description': '# TikBot\n\nMikrotik (RouterOS) Telegram Bot\n',
    'author': 'hexatester',
    'author_email': 'hexatester@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
