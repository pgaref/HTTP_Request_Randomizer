"""Setup script for HTTP_Request_Randomizer."""
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

LONG_DESCRIPTION = read('README.md')


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
      name='HTTP_Request_Randomizer',
      version='0.0.5',
      url='http://github.com/pgaref/HTTP_Request_Randomizer',
      license='MIT',
      author='Panagiotis Garefalakis',
      author_email='pangaref@gmail.com',
      description='A package using public proxies to randomise http requests.',
      long_description=LONG_DESCRIPTION,
      packages=find_packages(exclude=['tests']),
      cmdclass={'test': PyTest},
      test_suite='tests.test_parsers',
      include_package_data=True,
      package_data={
            # Include agents.txt files
            'http.requests': ['data/*'],
      },
      platforms='any',
      install_requires=["beautifulsoup4 >= 4.5.3",
                        "httmock>=1.2.6",
                        "psutil>=5.1.3",
                        "python-dateutil>=2.6.0",
                        "requests>=2.13.0",
                        "schedule>=0.4.2",
                        ],
      setup_requires=[
            'pytest-runner',
      ],
      tests_require=[
            'pytest',
            'pytest-cov'
      ],
      zip_safe=False
)