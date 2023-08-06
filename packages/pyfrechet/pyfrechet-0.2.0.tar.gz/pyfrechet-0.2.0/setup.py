# Setup file for uploading to PyPi
#
# Command line executions:
# python3 pyfrechet/build.py
# python3 setup.py sdist
# twine upload dist/*

from os import path
from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

long_description = long_description.replace('![Image](/docs/', 'File unavailable: ')
long_description = long_description.replace('?raw=true)', '')
long_description = long_description.replace('[documentation.html](documentation.html)', 'documentation.html')
long_description = long_description.replace('[/docs](/docs)', '/docs')

setup(
  name = 'pyfrechet',
  packages = ['pyfrechet'],
  version = '0.2.0',
  license='MIT',
  description = 'Frechet Distance Python Library',
  long_description_content_type='text/markdown',
  long_description=long_description,
  author = 'Will Rodman',
  author_email = 'wrodman@tulane.edu',
  url = 'https://github.com/compgeomTU/frechetForCurves',
  download_url = 'https://github.com/compgeomTU/frechetForCurves/archive/refs/tags/0.1.8.tar.gz',
  setup_requires=['cffi>=1.0.0'],
  install_requires=[
          'numpy',
          'matplotlib',
          'shapely',
          'cffi>=1.0.0'
      ],
  classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9'
    ],
)
