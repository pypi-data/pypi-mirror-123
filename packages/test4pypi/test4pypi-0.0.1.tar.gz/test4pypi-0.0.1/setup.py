#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: pony(747289639@qq.com)
# Description:none

from setuptools import setup, find_packages

setup(
    name = 'test4pypi',
    version = '0.0.1',
    keywords='test4pypi',
    description = 'just a test 4 pypi',
    license = 'MIT License',
    url = 'https://github.com/zsdlove/hades',
    author = 'pony',
    author_email = '747289639@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'requests>=2.19.1',
        ],
)