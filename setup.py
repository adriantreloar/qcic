#!/usr/bin/env python

import os
import sys

from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://qcic.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='qcic',
    version='0.0.1',
    description='Monitor for expected messages and send out mor emessages if they are not received',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Jonathan Adrian Treloar',
    author_email='qcic@cubeshine.com',
    url='https://github.com/adriantreloar/qcic',
    packages=[
        'qcic',
    ],
    package_dir={'qcic': 'qcic'},
    include_package_data=True,
    install_requires=[
    ],
    license='MPL2',
    zip_safe=False,
    keywords='qcic',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MPL2 License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    tests_require=['pytest'],
    cmdclass = {'test': PyTest},
    test_suite = 'test.test_qcic',
)
