from setuptools import setup, find_packages
from os import path

def get_long_description():
    with open(path.join(here, 'README.md'), encoding='utf-8') as readme:
        return readme.read()

setup(name="nielvis",
      description="Python API for interacting with National Instrument's ELVIS III Devices",
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      version='2.2.0',
      packages=find_packages(),
      install_requires=['nifpga', 'pyvisa'],
      author="National Instruments",
      url="https://github.com/ni/NI-ELVIS-III-Python-Examples",
      license="MIT",
      classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Education",
        "Topic :: Engineering",
        "Topic :: Software Deveopment",
        "Topic :: System :: Hardware"]
      )