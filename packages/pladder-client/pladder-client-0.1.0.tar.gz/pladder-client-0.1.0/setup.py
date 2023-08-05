# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pladder_client']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0', 'requests>=2,<3']

entry_points = \
{'console_scripts': ['pladder-client = pladder_client.client:main',
                     'strutern = pladder_client.client:main']}

setup_kwargs = {
    'name': 'pladder-client',
    'version': '0.1.0',
    'description': 'Client for the Web API of the Pladder Bot',
    'long_description': "# pladder-client\n\nA client for the Web API of the Pladder Bot.\n\n## Installation\n\n    pip install pladder-client\n\nYou may need to replace `pip` with `pip3`.\n\n## Usage\n\nCreate a token using `create-token` at the bot to get access. Then invoke `pladder-client` like this:\n\n    pladder-client 'echo This is a test command'\n\nThe first time, `pladder-client` will ask for the API endpoint URL and the API token and then store it in a config file.\n\nA `strutern` alias for `pladder-client` is also installed. They can be used interchangeably.\n",
    'author': 'Rasmus Bondesson',
    'author_email': 'raek@raek.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/raek/pladder-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
