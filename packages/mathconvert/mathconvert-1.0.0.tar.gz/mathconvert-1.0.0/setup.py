from setuptools import setup, find_packages
import codecs
import os


VERSION = '1.0.0'
DESCRIPTION = 'Convert binary, hex, octal, decimal'


# Setting up
setup(
    name="mathconvert",
    version=VERSION,
    author="Ayoub Ech-chetyouy",
    author_email="<ayoubechchetyouy@yahoo.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'math', 'convert', 'binary', 'hex', 'octal', 'To', 'decimal'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
