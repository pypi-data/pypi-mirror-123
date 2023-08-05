# -*- coding:utf-8 -*-
import setuptools
from setuptools import setup, find_packages

setup(
    name='osttools',
    version='1.0.1',
    description='Tools used by ordinary-student',
    author='ordinary-student',
    author_email='1113793417@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/ordinary-student/osttools',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],

    install_requires=[
        'prettytable',
        'PySide2',
    ]
)
