#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ghokie",
    version="0.0.1",
    python_requires='>=3.3.0',
    author="Afraz",
    author_email="afrazo@proton.me",
    description="GH App Application Access token generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/guidion-digital/ghokie",
    keywords=['github'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'PyJWT',
        'requests'
    ],
    scripts=['ghokie-cli.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    zip_safe=False
)
