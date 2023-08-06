from setuptools import setup,Extension,find_packages
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
import numpy as np

extensions = [
    Extension("*",["spacetime_tree/*.pyx",],
              libraries=["m"],
              include_dirs=[np.get_include(),]
              )
]

setup(
      name="spacetime_tree_cython",
      version = "3.0.0",
      setup_requires=[
        # Setuptools 18.0 properly handles Cython extensions.
        'setuptools>=18.0',
        'cython',
      ],
      python_requires=">=3.8,<3.10",
      install_requires=[
        "pandas>=1.3.2",
        "numpy>=1.19.2"
        ],
      packages = find_packages(),
      ext_modules = cythonize(
            extensions,
            compiler_directives={
                    "language_level": "3",
                    "boundscheck":False, 
                    "cdivision":True
                },
            annotate = True
            ),
            
      
      )