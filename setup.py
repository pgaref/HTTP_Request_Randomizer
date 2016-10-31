from setuptools import setup, find_packages
from glob import glob

setup(name='HTTP_Request_Randomizer',
      version='0.0.5',
      description='A package using public proxies to randomise http requests.',
      url='https://pgaref.github.io/blog/python-proxy/',
      author='pgaref',
      author_email='pangaref@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      package_data={
            # Include agents.txt files
            'http.requests': ['data/*'],
      },
      include_package_data=True,
      install_requires=["requests", "bs4", "psutil", "httmock", "python-dateutil", "schedule"],
      zip_safe=False)