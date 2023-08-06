#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: lukun2010(lukun@live.cn)
# Description:

from setuptools import setup, find_packages

setup(
    name = 'learn_rec_algorithm',
    version = '0.0.1',
    keywords=['recommendation', 'algorithm'],
    description = 'Private project for learning recommendation algorithm',
    license = 'MIT License',
    url = 'https://github.com/lukun2010/learn_rec_algorithm',
    author = 'lukun2010',
    author_email = 'lukun@live.cn',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'tensorflow==1.15.0',
        'deepctr',
        'tqdm'
        ],
)