#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of famulus
#
# Copyright (C) 2016 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages
from disthelpers import extract_messages, init_catalog, update_catalog
from disthelpers import build, build_catalog, build_man, build_html
from glob import glob
import famulus

setup(name='famulus',
      version=famulus.__version__,
      description='Servile test runner',
      long_description='''
      Famulus is a tool to run non-regression tests on a remote device.
      ''',
      license='GPLv3',
      url='https://github.com/elebihan/famulus/',
      platforms=['Any'],
      keywords=[],
      install_requires=[
          'colorama>=0.3',
          'pyaml>=15.8'
      ],
      classifiers=[
          'Development Status :: 1 - Pre-Alpha',
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(),
      data_files=[
          ('share/famulus/samples', glob('data/samples/*.yaml')),
          ('share/zsh/site-functions', glob('shell-completion/zsh/_*')),
      ],
      include_package_data=True,
      entry_points={
          'console_scripts': [
              'famulus = famulus.cli:main',
          ],
       },
      author='Eric Le Bihan',
      author_email='eric.le.bihan.dev@free.fr',
      cmdclass={'build': build,
                'build_man': build_man,
                'build_html': build_html,
                'extract_messages': extract_messages,
                'init_catalog': init_catalog,
                'update_catalog': update_catalog,
                'build_catalog': build_catalog})

# vim: ts=4 sts=4 sw=4 sta et ai
