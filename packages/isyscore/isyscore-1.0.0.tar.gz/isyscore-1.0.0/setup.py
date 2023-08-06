#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: rarnu
# Mail: rarnu1985@gmail.com
# Created Time:  2021-10-18 10:23:35
#############################################


from setuptools import setup, find_packages

setup(
    name = "isyscore",
    version = "1.0.0",
    keywords = ("isyscore", "component","sdk"),
    description = "ISYSCORE COMPONENT SDK",
    long_description = "ISYSCORE COMPONENT SDK",
    license = "Apache 2.0",

    url = "https://github.com/isyscore/component-py",
    author = "rarnu",
    author_email = "rarnu1985@gmail.com",

    packages = find_packages(),
    include_package_data = False,
    platforms = "any",
    install_requires = []
)