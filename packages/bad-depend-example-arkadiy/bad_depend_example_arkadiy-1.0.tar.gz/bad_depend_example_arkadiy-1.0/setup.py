from setuptools import setup

setup(
    name='bad_depend_example_arkadiy',
    version='1.0',    
    description='A example Python package with bad dep',
    packages=['bad_depend_example_arkadiy'],
    install_requires=['numpy==1.10.4',],
)