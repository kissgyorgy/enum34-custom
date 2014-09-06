from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


setup(
    name = 'enum34-custom',
    version = '0.6.1',
    description = 'Custom Enum classes for Python 3.4',
    long_description = open('README.rst').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = ['enum'],
    author = 'Kiss György',
    author_email = 'kissgyorgy@me.com',
    url = 'https://github.com/Walkman/enum34-custom',
    license = 'MIT',
    py_modules = ['enum34_custom'],
    tests_require = ['pytest', 'pytest-raisesregexp'],
)
