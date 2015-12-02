#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='monkeylearn',
    version='0.1.1',
    author='MonkeyLearn',
    author_email='hello@monkeylearn.com',
    description='Official Python client for the MonkeyLearn API',
    url='https://github.com/monkeylearn/monkeylearn-python',
    download_url='https://github.com/monkeylearn/monkeylearn-python/tarball/v0.1.1',
    keywords=['monkeylearn', 'machine learning', 'python'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    package_dir={'': '.'},
    packages=find_packages('.'),
    install_requires=[
        # use "pip install requests[security]" for taking out the warnings
        'requests>=2.8.1',
        'six>=1.10.0',
    ],
)
