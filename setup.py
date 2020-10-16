'''Setup script for HTTP_Request_Randomizer.'''
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs
import sys
import os
import re

NAME = 'http_request_randomizer'
HERE = os.path.abspath(os.path.dirname(__file__))

PROJECT_URLS = {
    'Blog': 'http://pgaref.com/blog/python-proxy',
    'Documentation': 'https://pythonhosted.org/http-request-randomizer',
    'Source Code': 'https://github.com/pgaref/http_request_randomizer',
}

def read(*parts):
    """Return multiple read calls to different readable objects as a single
    string."""
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(HERE, *parts), "rb", "utf-8").read()

try:
    META_PATH = os.path.join(HERE, "http_request_randomizer", "__init__.py")
finally:
    print(META_PATH)
    META_FILE = read(META_PATH)

def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    print(META_PATH)
    meta_match = re.search(
        fr"^__{meta}__ = ['\"]([^'\"]*)['\"]", META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{ meta }__ string.")

LONG_DESCRIPTION = read('README.rst')
#########################################################################
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
#########################################################################
setup(
    name=NAME,
    version=find_meta("version"),
    url=find_meta("uri"),
    project_urls=PROJECT_URLS,
    license=find_meta("license"),
    author=find_meta("author"),
    author_email=find_meta("email"),
    maintainer=find_meta("author"),
    maintainer_email=find_meta("email"),
    description=find_meta("description"),
    long_description=LONG_DESCRIPTION,
    packages=find_packages(exclude=['tests']),
    platforms='any',
    test_suite='tests.test_parsers',
    # tests_require=['tox'],
    # cmdclass={'test': Tox},
    tests_require=['pytest', 'pytest-cov'],
    cmdclass={'test': PyTest},
    install_requires=['beautifulsoup4 >= 4.9.3',
                      'httmock >= 1.3.0',
                      'psutil >= 5.7.2',
                      'python-dateutil >= 2.8.1',
                      'requests >= 2.24.0',
                      'pyOpenSSL >= 19.1.0',
                      'fake-useragent >= 0.1.11'
                      ],
    use_scm_version=True,
    setup_requires=['setuptools-scm', 'pytest-runner'],
    zip_safe=False,
    # include_package_data=True,
    package_data={
        # Include agents.txt files
        'http_request_randomizer.requests': ['data/*'],
    },
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'proxyList = http_request_randomizer.requests.runners.proxyList:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
