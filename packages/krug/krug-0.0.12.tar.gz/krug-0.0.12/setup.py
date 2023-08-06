import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent


README = (HERE / 'README.md').read_text()


setup(
    name='krug',
    version='0.0.12',
    description='A collection of useful heuristic based optimization algorithms.',
    long_description_content_type='text/markdown',
    long_description=README,
    url='',
    author='Alexander Anthon',
    # author_email='',
    license='GNU GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    packages=find_packages(exclude=('tests',)),
    install_requires=['numpy']
)
