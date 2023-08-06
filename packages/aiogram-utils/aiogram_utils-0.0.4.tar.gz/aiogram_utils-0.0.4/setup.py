#!/usr/bin/env python
from setuptools import find_packages, setup


def get_description():
    with open('README.md') as f:
        return f.read()


def get_requirements():
    with open('requirements.txt') as reqs:
        return [r.strip() for r in reqs]


setup(
    name='aiogram_utils',
    version='0.0.4',
    url='https://github.com/LDmitriy7/aiogram_utils',

    python_requires='>=3.7',
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    install_requires=get_requirements(),

    license='MIT',
    author='LDmitriy7',
    author_email='ldm.work2019@gmail.com',

    description='Misc utils for aiogram',
    long_description=get_description(),
)
