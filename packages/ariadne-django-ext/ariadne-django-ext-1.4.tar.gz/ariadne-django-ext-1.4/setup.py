# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ariadne_django_ext']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ariadne-django-ext',
    'version': '1.4',
    'description': 'Usable utility extensions for Ariadne & Django',
    'long_description': '<h1 align="center">\n  ariadne-django-ext\n</h1>\n\n<p align="center">\n  <a href="https://github.com/dulmandakh/ariadne-django-ext/">\n    <img src="https://img.shields.io/github/workflow/status/dulmandakh/ariadne-django-ext/CI?label=Test&logo=github&style=for-the-badge" alt="ci status">\n  </a>\n  <a href="https://pypi.org/project/ariadne-django-ext/">\n    <img src="https://img.shields.io/pypi/v/ariadne-django-ext?style=for-the-badge" alt="pypi link">\n  </a>\n  <a href="https://codecov.io/github/dulmandakh/ariadne-django-ext">\n    <img src="https://img.shields.io/codecov/c/github/dulmandakh/ariadne-django-ext?logo=codecov&style=for-the-badge" alt="codecov">\n  </a>\n  <br>\n  <a>\n    <img src="https://img.shields.io/pypi/pyversions/ariadne-django-ext?logo=python&style=for-the-badge" alt="supported python versions">\n  </a>\n  <a>\n    <img src="https://img.shields.io/pypi/djversions/ariadne-django-ext?logo=django&style=for-the-badge" alt="supported django versions">\n  </a>\n</p>\n\n<p align="center">\n  <a href="#installation">Installation</a> •\n  <a href="#contributing">Contributing</a> •\n  <a href="#license">License</a>\n</p>\n\n<p align="center">Custom, simple Django User model with email as username</p>\n\n## Installation\n\n```sh\npip install ariadne-django-ext\n```\n\n## Usage\n\n### cache\n\n**cache** decorator will cache a result returned from resolver using Django cache framework. You can it accepts same keyword arguments and passed down to Django cache.\n\nCache key must be either value or callable. Callable will receive same arguments as resolver then return cache key. Callable may return **None** to bypass the cache.\n\nIt uses **typename** and **key** from **info.path** as cache key prefix.\n\n```python\nfrom ariadne_django_ext import cache\n\n@cache(key=\'cache_key\')\ndef resolver(parent, info):\n    ...\n    return \'result\'\n\n```\n\n### wrap_result\n\n**wrap_result** decorator wraps return value of a resolver into dictionary with the key\n\n```python\nfrom ariadne_django_ext import wrap_result\n\n@wrap_result(key=\'result\')\ndef resolver(parent, info):\n    return \'result\'\n\n```\n\nAbove example will return following dict\n\n```json\n{ "result": "result" }\n```\n\n### isAuthenticated & isStaff directive\n\nA resolver will receive an authenticated user as keyword argument.\n\n```graphql\ndirective @isAuthenticated on FIELD_DEFINITION\n\ntype User {\n  id: ID\n  username: String\n  ipAddress: String @isAuthenticated\n}\n```\n\n```python\nfrom ariadne_django_ext import IsAuthenticatedDirective\n\nschema = make_executable_schema(\n  type_defs,\n  resolvers,\n  directives={"isAuthenticated": IsAuthenticatedDirective}\n)\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT License](https://choosealicense.com/licenses/mit/)\n\n```\n\n```\n',
    'author': 'Dulmandakh',
    'author_email': 'dulmandakh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dulmandakh/ariadne-django-ext',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
