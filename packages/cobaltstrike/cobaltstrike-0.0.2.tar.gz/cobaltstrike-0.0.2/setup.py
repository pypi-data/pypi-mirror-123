#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='cobaltstrike',
    version='0.0.2',
    author='xlzd',
    author_email='cs@gmail.com',
    url='https://blog.cobaltstrike.com',
    description=u'CobaltStrike Python API',
    packages=['cobaltstrike'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bridge=cobaltstrike:bridge',
            'sleep_python_bridge=cobaltstrike:sleep_python_bridge',
            'aggressor=cobaltstrike:aggressor',
            'aggressor_script=cobaltstrike:aggressor_script'
        ]
    }
)