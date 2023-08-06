# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_extend_headers']

package_data = \
{'': ['*']}

install_requires = \
['flask>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'flask-extend-headers',
    'version': '1.0.0',
    'description': 'Flask extend headers module for API versioning.',
    'long_description': '# flask-extend-headers\nFlask extend headers module for API versioning.\n',
    'author': 'Luis Emilio Moreno',
    'author_email': 'emilio@touchof.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lemiliomoreno/flask-extend-headers',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.10,<4.0.0',
}


setup(**setup_kwargs)
