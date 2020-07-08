from setuptools import setup
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    install_requires=required,
    name='algorithmplatform',
    version='0.0.1',
    packages=['py_client.aidm',
              'py_client.Conversion',
              'py_client.Communication',
              'py_client.algorithm_interface'],
    url='https://www.sma-partner.com/en/19-software-en/1401-algorithm-platform',
    license='Only for authorized use!',
    author='mhe, ffu',
    author_email='mhe@sma-partner.com',
    description=''
)
