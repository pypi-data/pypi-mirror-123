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
    'version': '1.0.0',
    'description': 'Middleware for tracking Falcon requests/responses with Elastic APM',
    'long_description': '# elastic-apm-falcon\nMiddleware for tracking Falcon requests/responses with Elastic APM.\n\nThis package provides a middleware for monitoring [Falcon](https://falconframework.org/)\napplications with [Elastic APM](https://www.elastic.co/apm/). The middleware hooks into Falcon\'s\nrequest and response processing and maintains an Elastic APM client to track transactions and\nmetadata.\n\n## Installation\nYou can install the latest stable version from\n[PyPI](https://pypi.org/project/elastic-apm-falcon/):\n\n```\n$ pip install elastic-apm-falcon\n```\n\n## Usage\nYou can add `elastic_apm_falcon` like any other middleware to your Falcon application. However,\nyou should make sure to import and instrument `elasticapm` as early as possible.\n\n```python\n# import and instrument elasticapm as early as possible\nimport elasticapm\nelasticapm.instrument()\n\n# import remaining modules\nimport falcon\nfrom elastic_apm_falcon import ElasticApmMiddleware\n\n\n# initialize Elastic APM middleware\nelastic_apm_middleware = ElasticApmMiddleware(service_name="your_service")\n\n# initialize Falcon application\napplication = falcon.App(middleware=elastic_apm_middleware)\n\n# add routes and resources to your application below\n...\n```\n\n## License\nThis package is licensed under the terms of the MIT license.\n\nMade with ♥ at [snapADDY](https://snapaddy.com/).\n',
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
