# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idempotency_header_middleware', 'idempotency_header_middleware.backends']

package_data = \
{'': ['*']}

extras_require = \
{'aioredis': ['aioredis>=2,<3', 'lupa'],
 'all': ['fastapi', 'starlette', 'aioredis>=2,<3', 'lupa'],
 'fastapi': ['fastapi'],
 'starlette': ['starlette']}

setup_kwargs = {
    'name': 'asgi-idempotency-header',
    'version': '0.1.1',
    'description': 'Enables idempotent operations in POST and PATCH endpoints.',
    'long_description': None,
    'author': 'Sondre Lillebø Gundersen',
    'author_email': 'sondrelg@live.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
