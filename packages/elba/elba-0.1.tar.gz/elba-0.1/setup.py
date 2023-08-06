from setuptools import setup,find_packages
import os

setup(name='elba',
      version='0.1',
      description='A simple tool for graph-based data persistence',
      author='Giuseppe Romano',
      author_email='romanog@mit.edu',
      install_requires=['dill','numpy','deepdiff','networkx','matplotlib','mpi4py','jax','jaxlib','OrderedSet','cloudpickle','termcolor','pyyaml'],
      classifiers=['Programming Language :: Python :: 3.6'],
      license='GPLv3',\
      packages = ['elba'],
      entry_points = {'console_scripts':['elba=elba.__main__:main']},
      zip_safe=False)
