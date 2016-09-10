from setuptools import setup, find_packages

setup(name='http-request-randomizer',
      version='0.0.3',
      description='A package using public proxies to randomise http requests.',
      url='https://pgaref.github.io/blog/python-proxy/',
      author='pgaref',
      author_email='pangaref@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      install_requires=["requests", "psutil", "httmock", "python-dateutil", "schedule"],
      zip_safe=False)