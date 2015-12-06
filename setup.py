from setuptools import setup, find_packages
import sys, os

version = '0.0'

test_requires = [
    'unittest2',
    'mock',
    'coverage',
]

setup(
    name='pyrpc',
    version=version,
    description="",
    long_description="""""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='python rpc remote procedure call json',
    author='Winston Ferreira',
    author_email='winstonf88@gmail.com',
    url='https://github.com/winstonf88/pyrpc',
    license='Apache 2.0',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ] + test_requires,
    entry_points="""
        # -*- Entry points: -*-
    """,
)
