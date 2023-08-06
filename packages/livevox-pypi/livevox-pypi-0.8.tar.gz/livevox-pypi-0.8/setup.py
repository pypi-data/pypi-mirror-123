
from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.8'
DESCRIPTION = 'Use Livevox fast as fuck!!'
LONG_DESCRIPTION = 'Use Livevox fast as fuck!!'

# Setting up
setup(
    name = 'livevox-pypi',
    version = VERSION,
    author = 'Javier Daza',
    author_email = "javierjdaza@gmail.com",
    description = DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,#LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['selenium','pandas'],
    keywords=['livevox'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)