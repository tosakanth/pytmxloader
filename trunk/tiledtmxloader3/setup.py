# -*- coding: utf-8 -*-
from distutils.core import setup
import sys

sys.path.append('tiledtmxloader')
import tiledtmxloader


setup(name='tiledtmxloader',
      version=tiledtmxloader.__version__,
      author='DR0ID',
      author_email='',
      url='https://code.google.com/p/pytmxloader/',
      download_url='https://code.google.com/p/pytmxloader/downloads/list',
      description='',
      long_description=tiledtmxloader.tiledtmxloader.__doc__,
      package_dir={'': 'tiledtmxloader'},
      py_modules=['tiledtmxloader', '__init__', 'helperspygame', 'helperspyglet'],
      provides=['tiledtmxloader'],
      keywords='pygame tiled mapeditor game map',
      license='Lesser Affero General Public License v3',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: GNU General Public License Version 2',
                  ],
     )