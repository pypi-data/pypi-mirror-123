
from distutils.core import setup
setup(
  name = 'AdvEMDpy',
  packages = ['AdvEMDpy'],
  version = '0.0.2',
  license='gpl-3.0',
  description = 'Advanced Empirical Mode Decomposition package with '
                'numerous extensions to various aspects of core algorithm.',
  author = 'Cole van Jaarsveldt',
  author_email = 'colevj0303@gmail.com',
  url = 'https://github.com/Cole-vJ/AdvEMDpy.git',
  download_url = 'https://github.com/Cole-vJ/AdvEMDpy/archive/refs/tags/v0.0.2.tar.gz',
  keywords = ['EMPIRICAL MODE DECOMPOSITION', 'EMD', 'STATISTICAL EMPIRICAL MODE DECOMPOSITION', 'SEMD',
              'ENHANCED EMPIRICAL MODE DECOMPOSITION', 'EEMD', 'ENSEMBLE EMPIRICAL MODE DECOMPOSITION',
              'HILBERT TRANSFORM', 'TIME SERIES ANALYSIS', 'FILTERING', 'GRADUATION', 'WINSORIZATION', 'DOWNSAMPLING',
              'SPLINES', 'KNOT OPTIMISATION', 'PYTHON', 'R', 'MATLAB',
              'FULL-SPECTRUM ENSEMBLE EMPIRICAL MODE DECOMPOSITION', 'FSEEMD', 'COMPRESSIVE SAMPLING',
              'COMPRESSIVE SAMPLING EMPIRICAL MODE DECOMPOSITION', 'CSEMD'],
  install_requires=[
          'numpy',
          'seaborn',
	  'scipy',
	  'matplotlib',
	  'cvxpy',
	  'colorednoise',
	  'pytest',
	  'PyEMD',
	  'emd',
	  'pandas',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.7',
  ],
)
