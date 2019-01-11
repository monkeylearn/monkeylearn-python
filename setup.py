#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='monkeylearn',
    version='3.2.4',
    author='MonkeyLearn',
    author_email='hello@monkeylearn.com',
    description='Official Python client for the MonkeyLearn API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/monkeylearn/monkeylearn-python',
    download_url='https://github.com/monkeylearn/monkeylearn-python/tarball/v3.2.4',
    keywords=['monkeylearn', 'machine learning', 'python'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
