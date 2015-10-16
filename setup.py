#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='monkeylearn',
    version='0.1',
    author='MonkeyLearn',
    author_email='hello@monkeylearn.com',
    description='',
    url='',
    download_url='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python',
    ],
    package_dir={'': '.'},
    packages=find_packages('.'),
    install_requires=[
        'requests==2.8.1',
        'cffi==1.2.1',
        'cryptography==1.0.2',
        'enum34==1.0.4',
        'idna==2.0',
        'ipaddress==1.0.14',
        'ndg-httpsclient==0.4.0',
        'pyOpenSSL==0.15.1',
        'pyasn1==0.1.9',
        'pycparser==2.14',
        'six==1.10.0',
    ],
)
