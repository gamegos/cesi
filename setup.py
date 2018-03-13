from setuptools import setup, find_packages

setup(
  name='cesi',
  version='0.1.0.dev0',
  description='Centralized supervisor interface.',
  long_description=('uzun tanimlama'),
  url='http://github.com/gamegos/cesi',
  license='GPLv3',
  author='Gulsah Kose',
  author_email='gulsah.1004@gmail.com',
  install_requires=[
  "flask==0.10.1",
  "passlib==1.7.1",
  "argon2_cffi==18.1.0"
  ],
  include_package_data=True,
  packages=find_packages()
)
