# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import six


if six.PY2:
    install_requires = ['six', 'enum34']
else:
    install_requires = ['six']


setup(
    name = 'enum34-custom',
    version = '0.7.2',
    description = 'Custom Enum classes for enum in Python 3.4 '
                  'or for enum34 for Python2.7',
    long_description = open('README.rst').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = ['enum'],
    author = 'Kiss György',
    author_email = 'kissgyorgy@me.com',
    url = 'https://github.com/Walkman/enum34-custom',
    license = 'MIT',
    py_modules = ['enum_custom'],
    install_requires = install_requires,
    tests_require = ['pytest', 'pytest-raisesregexp'],
)
