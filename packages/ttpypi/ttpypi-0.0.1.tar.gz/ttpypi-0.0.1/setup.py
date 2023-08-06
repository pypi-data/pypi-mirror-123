#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/10/15 4:45 下午 
# @Author : A Big Boby
# @File : setup.py 
# @Software: PyCharm


import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ttpypi',
    version='0.0.1',
    author='A Big Boby',
    author_email='ilikepython@163.com',
    description='测试包',
    long_description=long_description,
    url='https://www.baidu.com',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)