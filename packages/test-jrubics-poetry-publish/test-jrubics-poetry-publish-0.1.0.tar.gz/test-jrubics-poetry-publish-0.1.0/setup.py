# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['test_jrubics_poetry_publish']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'test-jrubics-poetry-publish',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jelena Dokic',
    'author_email': 'jelena.dpk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
