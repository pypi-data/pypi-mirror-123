from setuptools import setup

setup(
   name='bunk_py',
   version='2.3.1',
   description='An API wrapper for BunkServices API.',
   author='DaWinnerIsHere',
   author_email='dawinnerishere@gmail.com',
   url = 'https://github.com/DaWinnerIsHere/bunk_py',
   download_url = 'https://github.com/DaWinnerIsHere/bunk_py/archive/refs/tags/2.3.1.tar.gz',
   packages=['bunk_py'],
   package_dir={'bunk_py': './bunk_py'},
   install_requires=['wheel'],
)
