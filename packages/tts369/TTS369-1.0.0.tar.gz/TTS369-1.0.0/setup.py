# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['tts369']
setup_kwargs = {
    'name': 'tts369',
    'version': '1.0.0',
    'description': 'TTS("Your message").say()',
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
