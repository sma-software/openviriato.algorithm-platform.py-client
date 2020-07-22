from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    install_requires=required,
    name='algorithmplatform',
    version='0.0.1',
    packages=['py_client.aidm',
              'py_client.conversion',
              'py_client.communication',
              'py_client.algorithm_interface'],
    url='https://www.sma-partner.com',
    license='',
    author='',
    author_email='',
    description=''
)
