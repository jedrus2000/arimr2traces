# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='arimr2traces',
    version='1.1.0',
    description='Downloads data from ARiMR for usage in TRACES',
    long_description=readme,
    author='Andrzej Bargański',
    author_email='a.barganski@gmail.com',
    url='https://github.com/jedrus2000/arimr2traces',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
