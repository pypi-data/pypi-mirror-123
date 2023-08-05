#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: zhanglingkui
# Mail: 1570263833@qq.com
# Created Time: 2021-10-12 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
name = "mSynOrths",
version = "0.0.1",
keywords = ("pip", "genome","synteny", "ortholog", "paralog"),
description = "Multi genome synteny analyse",
long_description = "Find syntenic gene pairs and fragments between multi genome",
license = "MIT Licence",

url = "https://gitee.com/zhanglingkui/msynorths",
author = "zhanglingkui",
author_email = "1570263833@qq.com",

packages = find_packages(),
include_package_data = True,
platforms = "any",
install_requires = []
)