#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: lidongdong
# Mail: 927052521@qq.com
# Created Time: 2021.10.11  16.30
############################################


from setuptools import setup, find_packages

setup(
    name = "lddya",
    version = "1.1.4",
    keywords = ("pip", "license","licensetool", "tool", "gm"),
    description = "初步加入多种基本优化算法。",
    long_description = "具体功能，请自行挖掘。",
    license = "MIT Licence",

    url = "https://github.com/not_define/please_wait",
    author = "lidongdong",
    author_email = "927052521@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['chardet']
)
