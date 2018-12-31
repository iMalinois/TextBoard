#!/usr/bin/env python

from setuptools import setup, find_packages
from textboard.__init__ import __version__ as textboard_version

with open("README.md", "r") as fd:
    long_description = fd.read()

setup(name='textboard',
      version=textboard_version,
      author="Or Yahalom",
      author_email="itsMalinois@gmail.com",
      description="A module for displaying customizable console text board with your own custom text and lines.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/iMalinois/TextBoard",
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
     )