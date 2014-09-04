from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name='cesi',
  version='0.1.0-test-0',
  description='Centralized supervisor interface.',
  long_description=('uzun tanimlama'),
  url='http://github.com/GulsahKose/cesi',
  license='GPLv3',
  author='Gulsah Kose',
  author_email='gulsah.1004@gmail.com',
  install_requires=[
  "Flask==0.10.1"
  ],
  include_package_data=True,
  packages=['pack'],
  package_dir={
    'pack': 'pack',
    'pack': 'pack/static/noty-2.2.4/demo'
  },
  package_data={
    'pack': ['templates/*'],
    'pack': ['static/noty-2.2.4/demo/*']
  },
)
