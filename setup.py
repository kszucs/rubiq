#!/usr/bin/env python

import os
from setuptools import setup


setup(name='rubiq',
      version='0.1',
      packages=['rubiq'],
      description='sequely',
      url='http://github.com/kszucs/rubiq',
      maintainer='Krisztian Szucs',
      maintainer_email='szucs.krisztian@gmail.com',
      license='BSD',
      keywords='',
      install_requires=[],
      tests_require=[],
      setup_requires=[],
      long_description=(open('README.md').read() if os.path.exists('README.md')
                        else ''),
      zip_safe=False)
