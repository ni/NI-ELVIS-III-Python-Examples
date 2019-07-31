from setuptools import setup, find_packages
from os import path

def get_long_description():
    with open(path.join(here, 'README.md'), encoding='utf-8') as readme:
        return readme.read()

setup(name="nielvis",
      description="Python API for interacting with National Instrument's ELVIS III Devices",
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      version='1.0',
      packages=find_packages(),
      install_requires=['nifpga', 'pyvisa'],
      author="National Instruments",
      url="https://github.com/ni/NI-ELVIS-III-Python-Examples",
      license="MIT",
      classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: Linux",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Hardware"]
      )