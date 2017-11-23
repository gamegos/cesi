from setuptools import setup, find_packages

setup(
  name='cesi',
  version='2.0.0',
  description='Centralized supervisor interface.',
  long_description=('CESI is a web based interface to manage multiple supervizor instances'),
  url='http://github.com/gamegos/cesi',
  license='GPLv3',
  author='Gulsah Kose',
  author_email='gulsah.1004@gmail.com',
  install_requires=[
  "flask==0.10.1"
  ],
  include_package_data=True,
  packages=find_packages()
)
