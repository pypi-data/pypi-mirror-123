# -*- coding: utf-8 -*-
# :Project:   metapensiero.sphinx.patchdb
# :Created:   sab 22 ago 2009 17:26:36 CEST
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2009, 2010, 2012-2019, 2021 Lele Gaifax
#

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    CHANGES = f.read()
with open(os.path.join(here, 'version.txt'), encoding='utf-8') as f:
    VERSION = f.read().strip()

setup(
    name='metapensiero.sphinx.patchdb',
    version=VERSION,
    description="Extract scripts from a reST document and apply them in order.",
    long_description=README + '\n\n' + CHANGES,
    long_description_content_type='text/x-rst',

    author='Lele Gaifax',
    author_email='lele@metapensiero.it',
    url="https://gitlab.com/metapensiero/metapensiero.sphinx.patchdb.git",

    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved ::"
        " GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Database",
        "Topic :: Utilities",
        "Framework :: Sphinx :: Extension",
        "Environment :: Console",
        "Natural Language :: English",
        "Natural Language :: Italian",
        ],

    packages=['metapensiero.sphinx.' + pkg
              for pkg in find_packages('src/metapensiero/sphinx')],
    package_dir={'': 'src'},
    namespace_packages=['metapensiero', 'metapensiero.sphinx'],

    include_package_data=True,

    install_requires=[
        'enlighten',
        'sqlparse',
    ],
    extras_require={
        'dev': [
            'babel',
            'metapensiero.tool.bump_version',
            'pygments',
            'readme_renderer',
            'sphinx',
            'twine',
        ],
    },

    tests_require=[
        'docutils',
        'pygments',
        'pytest',
        'sphinx',
    ],
    test_suite='py.test',

    entry_points="""\
    [console_scripts]
    patchdb = metapensiero.sphinx.patchdb.pup:main
    patchdb-states = metapensiero.sphinx.patchdb.states:main
    """,
)
