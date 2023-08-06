# encoding: utf-8
import sys

from setuptools import setup


def read_description():
    with open('README.md', 'r') as f:
        return f.read()


NAME = "feast-schema"
DESCRIPTION = "Feast schema inspect library"
URL = "https://github.com/qooba/feast-schema"
AUTHOR = "Kuba Sołtys"
REQUIRES_PYTHON = ">=3.7.0"
REQUIRED = [
    "feast",
    "json2html",
    "ipython",
    "Click"
]
REQUIRED_DEV = [
    "pytest",
    "requests",
    "pytest-cov>=2.10.1"
]

setup(
    name=NAME,
    version='0.0.1',
    url=URL,
    license='MIT',
    author=AUTHOR,
    author_email='dev@qooba.net',
    description=DESCRIPTION,
    long_description=read_description(),
    long_description_content_type="text/markdown",
    packages=['feast_schema'],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    extras_require={
        "dev": REQUIRED_DEV,
    },
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={"console_scripts": ["feast-schema=feast_schema.cli:cli"]},

)
