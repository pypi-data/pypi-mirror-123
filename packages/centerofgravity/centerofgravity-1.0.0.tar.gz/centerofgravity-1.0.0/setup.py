# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 10:19:49 2021

@author: Abram Moats
"""
  
from setuptools import setup

setup(name='centerofgravity',
      version='1.0.0',
      description='Automated Center of Gravity Mapping',
      url='https://github.com/abrammoats/centerofgravity',
      download_url = 'https://github.com/abrammoats/centerofgravity/archive/refs/tags/1.0.0.tar.gz',
      author='Scott Mutchler, Abram Moats',
      author_email='smutchler@trilabyte.com, abramdanielmoats@gmail.com',
      license='GPLv3',
      packages=['centerofgravity'],
      keywords = ['CENTROID', 'MAPPING', 'VISUALIZATION', 'CLUSTERING'],
      install_requires=[
        'pandas',
        'scikit-learn',
        'numpy',
        'json',
        'math',
        'folium'
      ],
      classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
      ],
      zip_safe=False)


