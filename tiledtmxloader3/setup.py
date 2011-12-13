# -*- coding: utf-8 -*-

from distutils.core import setup
import sys

sys.path.append('tiledtmxloader')
import tiledtmxloader


setup(name='tiledtmxloader',
      version=tiledtmxloader.__version__,
      author='DR0ID',
      author_email='dr0iddr0id@gmail.com',
      maintainer='DR0ID',
      url='https://code.google.com/p/pytmxloader/',
      download_url='https://code.google.com/p/pytmxloader/downloads/list',
      description='',
      long_description=tiledtmxloader.tmxreader.__doc__,
      package_dir={'': 'tiledtmxloader'},
      py_modules=['tmxreader', '__init__', 'helperspygame', 'helperspyglet'],
      provides=['tiledtmxloader'],
      keywords='pygame tiled mapeditor game map',
      license='New BSD License',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: GNU General Public License Version 2',
                  ],
     )
