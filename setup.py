from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name = 'enum34-custom',
    version = '0.2.1',
    description = 'Custom Enum classes for Python 3.4',
    long_description = open('README.rst').read(),
    classifiers = [
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
    ],
    keywords = ['enum'],
    author = 'Kiss György',
    author_email = 'kissgyorgy@me.com',
    url = 'https://github.com/Walkman/enum34-custom',
    license = 'MIT',
    py_modules = ['enum34_custom'],
    tests_require = ['pytest'],
    cmdclass = {'test': PyTest},
)
