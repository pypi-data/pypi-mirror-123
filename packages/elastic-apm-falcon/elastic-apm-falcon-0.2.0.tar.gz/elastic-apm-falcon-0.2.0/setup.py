# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elastic_apm_falcon']

package_data = \
{'': ['*']}

install_requires = \
['elastic-apm>=6.0.0,<7.0.0', 'falcon>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'elastic-apm-falcon',
    'version': '0.2.0',
    'description': 'Middleware for tracking Falcon requests/responses with Elastic APM.',
    'long_description': '# elastic-apm-falcon\n',
    'author': 'Benedikt Brief',
    'author_email': 'b.brief@snapaddy.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
