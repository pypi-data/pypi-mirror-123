# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['projectaile',
 'projectaile.config',
 'projectaile.data',
 'projectaile.data.extractors',
 'projectaile.data.loaders',
 'projectaile.engine',
 'projectaile.loggers',
 'projectaile.model',
 'projectaile.pipelines',
 'projectaile.pipelines.augmentations',
 'projectaile.pipelines.preprocesses',
 'projectaile.savers',
 'projectaile.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'projectaile',
    'version': '0.0.1',
    'description': 'A framework agnostic architecture and utility library for all machine learning and deep learning projects providing an abstract and easy to use but still very configurable API.',
    'long_description': None,
    'author': 'abtExp',
    'author_email': 'abt.exp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
