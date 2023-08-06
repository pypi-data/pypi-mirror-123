#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021/10/12 6:00 下午
# @Author : A Big Boby
# @File : setup.py.py 
# @Software: PyCharm


import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='whrtest',
    version='0.0.1',
    author='A Big Boby',
    author_email='ilikepython@163.com',
    description='Oh! whr',
    long_description=long_description,
    url='https://github.com/BigGoby/BigPig',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)