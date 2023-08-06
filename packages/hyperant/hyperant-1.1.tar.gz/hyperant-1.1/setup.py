from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='hyperant',
   version='1.1',
   python_requires='>3.5.2',
   description='BMC Research Programmer Technical Test - Ant on Cube',
   license="MIT",
   long_description=long_description,
   long_description_content_type='text/markdown',
   author='Victor Arsenescu',
   url="https://github.com/v0rtex20k",
   author_email='victor.arsenescu@tufts.edu',
   packages=['hyperant'],
   scripts=[
            'scripts/hypercube.h',
            'scripts/hypercube.cpp',
            # 'scripts/run-hypercube', // Bash build script for backend
           ]
)
