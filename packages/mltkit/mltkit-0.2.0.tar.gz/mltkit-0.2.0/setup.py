# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

from setuptools import setup, find_packages
import mltkit

name = 'mltkit'
description = 'A toolkit for ML boilerplate.'
url = 'https://github.com/mdlockyer/mltkit'
author = 'Michael Lockyer'
author_email = 'mdlockyer@gmail.com'
version = mltkit.__version__
license_type = 'MIT License'
classifiers = (
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX"
)
install_requires = ['PrintTags']
packages = find_packages()

setup(name=name, description=description, version=version,
      url=url, author=author, author_email=author_email,
      license=license_type, classifiers=classifiers,
      packages=packages, python_requires='>=3.6')
