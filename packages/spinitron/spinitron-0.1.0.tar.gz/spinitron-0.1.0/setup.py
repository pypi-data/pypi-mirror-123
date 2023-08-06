# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spinitron', 'spinitron.models']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.21,<3.0', 'requests_cache>=0.5.0,<0.6.0']

setup_kwargs = {
    'name': 'spinitron',
    'version': '0.1.0',
    'description': 'Wrapper for Spinitron API',
    'long_description': None,
    'author': 'slogsdon',
    'author_email': 'me@slogsdon.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
