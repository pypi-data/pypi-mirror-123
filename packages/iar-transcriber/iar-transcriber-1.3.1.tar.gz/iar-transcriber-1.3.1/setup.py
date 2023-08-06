#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Iván Arias Rodríguez, CC BY-NC-SA 4.0 license

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
http://creativecommons.org/licenses/by-nc-sa/4.0/

This code is given as is without warranty of any kind.
In no event shall the authors or copyright holder be liable for any claim damages or other liability.

If you change or adapt this function, change its name (for example add your initial after the name)
"""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name="iar-transcriber",
                 version="1.3.1",
                 author="Iván Arias Rodríguez",
                 author_email="ivan.arias.rodriguez@gmail.com",
                 description="A phonetic transcriber for Spanish language.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://pypi.org/project/iar-transcriber/",
                 packages=setuptools.find_packages(),
                 classifiers=[
                     "Programming Language :: Python",
                     "Development Status :: 1 - Planning",
                     "Intended Audience :: Science/Research",
                     "License :: Other/Proprietary License",
                     "Natural Language :: Spanish",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 3 :: Only",
                     "Topic :: Scientific/Engineering"],
                 include_package_data=True,
                 install_requires=['nltk', 'num2words', 'roman', 'python-dateutil', 'iar_tokenizer'],
                 license="Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License",
                 )
