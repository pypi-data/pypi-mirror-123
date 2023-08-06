#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='MetricTool',
    version='0.1.4',
    description=(
        '针对多种不同源码语言的度量分析工具。'
    ),
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    author='bobo.yang',
    author_email='ybb_y1b1b1@163.com',
    maintainer='boboyang',
    maintainer_email='ybb_y1b1b1@163.com',
    license='BSD License',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    url='https://gitee.com/imlaji/cyclomatic-complexity/tree/master',
    install_requires = ['tree-sitter>=0.19.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)