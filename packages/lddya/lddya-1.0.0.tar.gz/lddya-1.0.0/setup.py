#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: gm
# Mail: 1025304567@qq.com
# Created Time: 2019-04-11 15:37:04
#############################################


from setuptools import setup, find_packages

setup(
    name = "lddya",
    version = "1.0.0",
    keywords = ("pip", "license","licensetool", "tool", "gm"),
    description = "Creat by Li Dong-dong.",
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
