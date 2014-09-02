import os
from distutils.core import setup

setup(
  name='cesi',
  version='0.1.0',
  description='Centralized supervisor interface.',
  long_description=('uzun tanimlama'),
  url='http://github.com/GulsahKose/cesi',
  license='GPLv3',
  author='Gulsah Kose',
  author_email='gulsah.1004@gmail.com',
  install_requires=[
  "Flask==0.10.1",
  "sqlite3==3.8.2"
  ],
  package_data={
    'static': 'cesi/static/*',
    'templates': 'cesi/templates/*'},
  packages = [
    'cesi.cesi',
    'cesi.web',
  ]
)
