# -*- coding: utf-8 -*-

""" PSSSA BBS packaging instructions.
"""

from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='psssa-bbs',
    version='0.0.2',
    description='Python Software Society of South Africa BBS',
    long_description=long_description,
    url='https://github.com/ctpug/psssa-bbs',
    author='Python Software Society of South Africa',
    author_email='team@za.pycon.org',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='python psssa bbs',
    packages=[
        "psssa_bbs",
    ],
    package_data={
        "psssa_bbs": ["*.txt"],
    },
    install_requires=[
        "click",
        "pyfiglet",
        "telnetlib3",
        "termcolor",
    ],
    extras_require={
        'dev': ['flake8'],
    },
    entry_points={
        'console_scripts': [
            'psssa-bbs=psssa_bbs.cli:cli',
        ],
    },
)
