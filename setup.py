#!/usr/bin/python3
"""Setup
"""
from setuptools import find_packages
from setuptools.command.test import test
from distutils.core import setup

version = "1.0.0"

setup(
    name="ofxstatement-hype",
    version=version,
    author="Lorenzo Giudici",
    author_email="lorenzogiudici5@proton.com",
    url="https://github.com/lorenzogiudici5/ofxstatement-hype",
    description=("Hype plugin for ofxstatement"),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="GPLv3",
    keywords=["ofx", "banking", "statement", "hype"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["ofxstatement", "ofxstatement.plugins"],
    entry_points={
        "ofxstatement":
        [
            "hype = ofxstatement.plugins.hype:HypePlugin"
        ]
    },
    install_requires=["ofxstatement", "pandas", "tabula-py", "pypdf2"],
    extras_require={"test": ["pytest"]},
    include_package_data=True,
    zip_safe=True,
)
