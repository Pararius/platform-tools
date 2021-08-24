from setuptools import setup, find_packages
import os, codecs, re

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='platform_tools',
    author='Martijn Barendregt',
    author_email='m.barendregt@pararius.nl',
    version=find_version('platform_tools','__init__.py'),
    description='A collection of tools for working with GCP',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires = 
        [
            'pandas>=1.0', 
            'google-cloud-storage',
        ],
    python_requires='>=3.7',
)
