from setuptools import setup

setup(
    name='foopy21',
    version='0.1.0',
    description='Packege use numpy 1.16.0 that conflicts with pandas 1.3.3',
    url='https://github.com/YaroslavZhurba/foopy21',
    author='Yaroslav Zhurba',
    author_email='shudson@anl.gov',
    license='BSD 2-clause',
    packages=['foopy21'],
    install_requires=['numpy<=1.16.0']
)
