from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))


with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="batchcreate",
    version="0.1.5",
    description="Demo batchcreate library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://batchcreate.readthedocs.io/",
    author="Amruta K",
    author_email="",
    license="",
    packages=["batchcreate"],
    include_package_data=True,
    install_requires=[],
    test_suite='tests',
    tests_require=[],
)