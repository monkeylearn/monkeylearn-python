#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='monkeylearn',
    version='3.0.0',
    author='MonkeyLearn',
    author_email='hello@monkeylearn.com',
    description='Official Python client for the MonkeyLearn API',
    url='https://github.com/monkeylearn/monkeylearn-python',
    download_url='https://github.com/monkeylearn/monkeylearn-python/tarball/v3.0.0-pre',
    keywords=['monkeylearn', 'machine learning', 'python'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    package_dir={'': '.'},
    packages=find_packages('.'),
    install_requires=[
        # use "pip install requests[security]" for taking out the warnings
        'requests>=2.8.1',
        'six>=1.10.0',
    ],
)
