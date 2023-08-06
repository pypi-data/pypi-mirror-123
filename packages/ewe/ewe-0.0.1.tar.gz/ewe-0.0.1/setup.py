from pathlib import Path
from setuptools import setup, find_packages

with open(Path('./requirements.txt')) as f:
    required = f.read().splitlines()

with open(Path(__file__).parent.joinpath('README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ewe',
    description='ewe build tool',
    version='0.0.1',
    long_description=long_description,
    long_description_conent_type='text/markdown',
    author='rwxd',
    author_email='rwxd@pm.me',
    license='MIT',
    packages=find_packages('./', exclude=['tests/']),
    entrypoints={
        'console_scripts': ['ewe = ewe.__main__:main']
    }
)