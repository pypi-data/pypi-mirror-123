from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'For testing'

setup(
    name="Arest7",
    version=VERSION,
    author="Ken Ryuguji",
    author_email="behruzbekabdumutalov@Gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['art', 'rich'],
    keywords=["python", "python banner", "art"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        #"Operation System :: Unix",
        #"Operation System :: MacOS :: MacOS X",
        #"Operation System :: Microsoft :: Windows",
    ]

)