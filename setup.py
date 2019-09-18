from setuptools import setup, find_packages
import os

def get_long_description():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'PIPDESCRIPTION.md'), encoding='utf-8') as readme:
        return readme.read()

setup(name="nielvis",
      description="Python API for interacting with National Instrument's ELVIS III Devices",
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      version='2.2.7',
      packages=find_packages(),
      package_data={'': ['./bitfile/*.lvbitx']},
      install_requires=['nifpga', 'pyvisa'],
      author='National Instruments',
      author_email="opensource@ni.com",
      maintainer="National Instruments",
      maintainer_email="opensource@ni.com",
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
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: System :: Hardware"]
      )