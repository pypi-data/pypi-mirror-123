from setuptools import setup, Extension, find_packages
from setuptools.command.install import install
import subprocess
import os
import numpy as np

extensions = [Extension("*", ["./biobox/lib/*.pyx"])]
from Cython.Build import cythonize
extensions = cythonize(extensions)

setup(
  name = 'biobox',
  packages = ['biobox',
              'biobox.classes',
              'biobox.lib',
              'biobox.measures',
              'biobox.test'
      ],
  version = '1.0.2',
  license='GPL3',
  description = 'Biobox provides a collection of data structures and methods for loading, manipulating and analyzing atomistic and pseudoatomistic structures.',
  author = 'Matteo T. Degiacomi, Lucas S.P. Rudden, Samuel C. Musson',
  author_email = 'lucas.s.p.rudden@gmail.com',
  url = 'https://github.com/degiacom/biobox',
  download_url = 'https://github.com/degiacom/biobox/archive/v1.0.0.tar.gz',
  keywords = ['biobox'],
  install_requires=[
          'numpy',
          'scipy',
          'scikit-learn',
          'pandas'
      ],
  package_data={'biobox' : ['./lib/*.pyx', './classes/*.sh', './classes/*.dat, ./*.cfg', './test/*.pdb', './test/*.mrc']},
  ext_modules = extensions, include_dirs=[np.get_include()]
)
