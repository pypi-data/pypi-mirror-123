#!/usr/bin/env python3

from setuptools import setup, find_packages


install_requires = [
    'ase>=3.22.0',
]


setup(
    name='ase-gpatom',
    version='0.1',
    license='LGPLv2.1+',
    packages=find_packages(),
    install_requires=install_requires,
)
