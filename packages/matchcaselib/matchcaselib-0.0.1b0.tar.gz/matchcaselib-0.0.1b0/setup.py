from setuptools import setup

with open("README.md", "r") as f:
  long_description = f.read()

setup(
  name='matchcaselib',
  version='0.0.1b',
  description="Easy implementation of Python 3.10's structural pattern matching.",
  py_modules=["matchcaselib"],
  package_dir={"": "src"},
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/MasterCoder21/matchcaselib",
  author="minecraftpr03",
  author_email=None,
  classifiers=[
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
  ]
)