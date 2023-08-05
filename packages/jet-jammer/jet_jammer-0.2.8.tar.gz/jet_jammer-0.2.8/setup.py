# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jet_jammer']
install_requires = \
['MIDIUtil>=1.2.1,<2.0.0',
 'fastapi>=0.70.0,<0.71.0',
 'platformdirs>=2.4.0,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'jet-jammer',
    'version': '0.2.8',
    'description': 'Jamming tool',
    'long_description': None,
    'author': 'Jack Reilly',
    'author_email': 'jackdreilly@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
