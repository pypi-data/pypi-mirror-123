#!usr/bin/env python

from setuptools import setup, find_packages
import sys
import os

from dm_gym.version import VERSION

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dm_gym'))

setup(name='dm-gym',
      version=VERSION,
      description='DM-Gym: A set of environments for developing reinforcement learning agents for Data Mining problems.',
      author='Ashwin M Devanga',
      author_email='devanga.a@northeastern.edu',
      license='BSD 3-Clause',
      url='https://github.com/ashwin-M-D/DM-Gym',
      packages=find_packages(),
      install_requires=[
          'gym>=0.15.0',
          'numpy>=1.16.1',
          'scipy>=1.0',
          'matplotlib>=3.1',
          'networkx>=2.3',
          'scikit-learn>=1.0'],
      zip_safe=False,
      python_requires='>=3.5',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ]
      )
