# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pypitesty',
    version='1.1.0',
    description='python connection tools collection',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='luoanni',
    author_email='luoanni33@gmail.com',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['qPython>=2.0.0']
)
