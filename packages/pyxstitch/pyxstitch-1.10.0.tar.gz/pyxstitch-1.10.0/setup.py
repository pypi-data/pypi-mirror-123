#!/usr/bin/python3

"""Setup for pyxstitch."""

from setuptools import setup

__pkg_name__ = "pyxstitch"

long_description = ""
with open("README.rst", 'r') as f:
    long_description = f.read()

setup(
    author="Sean Enck",
    author_email="enckse@voidedtech.com",
    name=__pkg_name__,
    version="1.10.0",
    description='Convert source code to cross stitch patterns',
    long_description=long_description,
    url='https://github.com/enckse/pyxstitch',
    license='GPL3',
    python_requires='>=3.7',
    packages=[__pkg_name__, __pkg_name__ + ".fonts"],
    install_requires=['pygments', 'Pillow'],
    keywords='crossstitch cross stitch',
    entry_points={
        'console_scripts': [
            'pyxstitch = pyxstitch.pyxstitch:main',
        ],
    },
)
