# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['komolibs',
 'komolibs.aws',
 'komolibs.aws.s3',
 'komolibs.caching',
 'komolibs.core',
 'komolibs.core.utils',
 'komolibs.db',
 'komolibs.db.influx',
 'komolibs.logger',
 'komolibs.messaging',
 'komolibs.pubsub']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0',
 'boto3>=1.18.27,<2.0.0',
 'influxdb-client>=1.19.0,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'redis>=3.5.3,<4.0.0']

setup_kwargs = {
    'name': 'komolibs',
    'version': '0.1.510',
    'description': '',
    'long_description': None,
    'author': 'Makhosonke Morafo',
    'author_email': 'makhosonke@komokun.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
