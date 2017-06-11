'''Setup script for HTTP_Request_Randomizer.'''
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import sys
import os
HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), 'r').read()

LONG_DESCRIPTION = read('README.rst')


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--strict',
            '--verbose',
            '--tb=long',
            'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='http_request_randomizer',
    version='1.0.5',
    url='http://pgaref.com/blog/python-proxy',
    license='MIT',
    author='Panagiotis Garefalakis',
    author_email='pangaref@gmail.com',
    description='A package using public proxies to randomise http requests.',
    long_description=LONG_DESCRIPTION,
    packages=find_packages(exclude=['tests']),
    platforms='any',
    test_suite='tests.test_parsers',
    # tests_require=['tox'],
    # cmdclass={'test': Tox},
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': PyTest},
    install_requires=['beautifulsoup4 >= 4.6.0',
                      'httmock >= 1.2.6',
                      'psutil >= 5.2.2',
                      'python-dateutil >= 2.6.0',
                      'requests >= 2.14.2',
                      'schedule >= 0.4.2',
                      ],
    setup_requires=['pytest-runner'],
    zip_safe=False,
    # include_package_data=True,
    package_data={
        # Include agents.txt files
        'http_request_randomizer.requests': ['data/*'],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
