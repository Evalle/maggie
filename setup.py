# Always prefer setuptools over distutils
from setuptools import setup

setup(
     name='maggie',         # This is the name of your PyPI-package.
     version='0.1',         # Update the version number for new releases
     scripts=['maggie']     # The name of your scipt, and also the command you'll be using for calling it
)