# -*- coding: utf-8 -*-

import sys
from setuptools import setup


setup(
    name='enum34-custom',
    version='0.7.2',
    description='Custom Enum classes for enum in Python 3.4 '
                'or for enum34 for Python2.7',
    long_description=open('README.rst').read(),
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords=['enum'],
    author=u'Kiss György',
    author_email='kissgyorgy@me.com',
    url='https://github.com/kissgyorgy/enum34-custom',
    license='MIT',
    py_modules=['enum_custom'],
    install_requires=['enum34', 'six'] if sys.version_info[0] < 3 else ['enum34'],
    tests_require=['pytest', 'pytest-raisesregexp'],
)
