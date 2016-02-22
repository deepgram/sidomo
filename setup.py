# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sdpm',
    version='0.0.1',
    description='Simple Docker Python Module',
    long_description=readme,
    author='Noah Shutty',
    author_email='noah@deepgram.com',
    url='https://github.com/noajshu/sdpm',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)