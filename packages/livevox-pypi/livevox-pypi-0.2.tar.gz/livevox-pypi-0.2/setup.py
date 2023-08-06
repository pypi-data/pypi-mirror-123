
from setuptools import setup, find_packages


VERSION = '0.2'
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
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['selenium','pandas'],
    keywords=['livevox'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)