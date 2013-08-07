#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

from corrida import __version__ as version

source = 'http://pypi.python.org/packages/source'
install_requires = ['numpy', 'pandas']

classifiers = """\
Development Status :: 5 - Production/Stable
Environment :: Console
Intended Audience :: Science/Research
Intended Audience :: Developers
Intended Audience :: Education
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Scientific/Engineering
Topic :: Education
Topic :: Software Development :: Libraries :: Python Modules
"""

README = open('README.md').read()
CHANGES = open('CHANGES.txt').read()
LICENSE = open('LICENSE.txt').read()

config = dict(name='corrida',
              version=version,
              packages=['corrida'],
              test_suite='test',
              use_2to3=True,
              license=LICENSE,
              long_description='%s\n\n%s' % (README, CHANGES),
              classifiers=filter(None, classifiers.split("\n")),
              description='Running spreadsheet',
              author='Filipe Fernandes',
              author_email='ocefpaf@gmail.com',
              maintainer='Filipe Fernandes',
              maintainer_email='ocefpaf@gmail.com',
              url='http://pypi.python.org/pypi/corrida/',
              download_url='%s/c/corrida/corrida-%s.tar.gz' % (source, version),
              platforms='any',
              keywords=['oceanography', 'data analysis', 'cnv', 'DataFrame'],
              install_requires=install_requires)

setup(**config)
