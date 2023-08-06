# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tendon', 'tendon.api', 'tendon.api.nodes', 'tendon.gql']

package_data = \
{'': ['*']}

install_requires = \
['graphql-core>=3.0.3,<4.0.0', 'httpx>=0.12.1,<0.13.0']

setup_kwargs = {
    'name': 'tendon',
    'version': '1.2.0',
    'description': '',
    'long_description': None,
    'author': 'Tendon',
    'author_email': 'alastair@tendon.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
