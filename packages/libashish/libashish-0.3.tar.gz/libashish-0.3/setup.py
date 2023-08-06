#from distutils.core import setup
from setuptools import setup
setup(
  name = 'libashish',         # How you named your package folder (MyLib)
  packages = ['libashish'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'first pypi deploy',   # Give a short description about your library
  author = 'Ashish',                   # Type in your name
  author_email = 'agarwal.ashish.singhal@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/CRLannister/pypitest',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/CRLannister/pypitest/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['first', 'pypi', 'package'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pydantic',
          'numpy',
          'pandas',
          'tensorflow',
          'unidecode',
          'transliterate',
          'sklearn',
          'scipy',
          'matplotlib',
          'dload',
          'requests',
          'google',
          'tqdm'
      ],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
