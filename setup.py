#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

cur_dir = path.abspath(path.dirname(__file__))
with open(path.join(cur_dir, 'README.md')) as f:
    long_desc = f.read()


setup(
    name='flask-file-sharing',
    packages=['upload'],
    version='0.0.1',
    description='A flask-based file sharing server',
    long_description=long_desc,
    author='https://github.com/learningpython08',
    license='GPLv3',
    keywords=['flask', 'sharing', 'curl']
)
