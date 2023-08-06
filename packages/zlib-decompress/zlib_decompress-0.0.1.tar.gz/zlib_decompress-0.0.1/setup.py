from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = ""
LONG_DESCRIPTION = ""

setup(
    name="zlib_decompress",
    version=VERSION,
    author="",
    author_email="",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    url="https://github.com/jgibo/zlib-decompress",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': ['zlib-decompress=zlib_decompress.cli:main']
    }
)