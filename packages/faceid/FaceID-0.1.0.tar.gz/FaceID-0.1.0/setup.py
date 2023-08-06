# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['faceid']
setup_kwargs = {
    'name': 'faceid',
    'version': '0.1.0',
    'description': 'FaceID().load().search()',
    'long_description': None,
    'author': 'dudha369',
    'author_email': 'duduha2010@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
