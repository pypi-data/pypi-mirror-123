from setuptools import setup, find_packages

VERSION = "0.0.2"
DESCRIPTION = ""
LONG_DESCRIPTION = ""

setup(
    name="zlib_decompress",
    version=VERSION,
    author="Jordan Gibbings",
    author_email="jgibbings94@gmail.com",
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    url="https://github.com/jgibo/zlib-decompress",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': ['zlib-decompress=zlib_decompress.cli:main']
    }
)