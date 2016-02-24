# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('./requirements.txt') as reqs_txt:
    requirements = [line for line in reqs_txt]


setup(
    name='sidomo',
    version='0.0.1',
    description='Simple Docker Module',
    long_description=readme,
    install_requires=requirements,
    author='Noah Shutty',
    author_email='noah@deepgram.com',
    url='https://github.com/deepgram/sidomo',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
