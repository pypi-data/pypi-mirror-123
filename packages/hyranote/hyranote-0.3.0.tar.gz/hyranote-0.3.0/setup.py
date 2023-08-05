# !/usr/bin/env python3
from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(name='hyranote',
      version='0.3.0',
      description='Transform mindnode file to weekly notes',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/huuhoa/hyranote',
      author='Huu Hoa NGUYEN',
      author_email='huuhoa@gmail.com',
      license='MIT License',
      packages=find_packages(include=['hyranote']),
      install_requires=[
          'beautifulsoup4==4.9.1',
      ],
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      entry_points={
          'console_scripts': [
              'hyranote = hyranote.cli:main'
          ]
      })
