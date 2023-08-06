#!python3
# coding:utf8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name="iar_wiki_parser",
                 version="1.0.3",
                 author="Iván Arias Rodríguez",
                 author_email="ivan.arias.rodriguez@gmail.com",
                 description="A parser for the Spanish Wikipedia.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/ivansiiito/iar_wiki_parser",
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
                 install_requires=['iar_tokenizer', 'urllib3', 'bz2file'],
                 )
