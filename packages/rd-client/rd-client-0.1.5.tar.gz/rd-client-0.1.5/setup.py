# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rd_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'rd-client',
    'version': '0.1.5',
    'description': 'Client for RDStation API',
    'long_description': None,
    'author': 'Ramiro Tician',
    'author_email': 'ramirotician@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
