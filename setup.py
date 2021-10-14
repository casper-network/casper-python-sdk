import os
import re

from setuptools import setup
from setuptools import find_packages
from setuptools import Extension
from setuptools.dist import Distribution


# List of 3rd party python dependencies.
with open("requirements.txt", "r") as fstream:
     _REQUIRES = fstream.read().splitlines()


class _BinaryDistribution(Distribution):
    """Distribution sub-class to override defaults.

    """
    def is_pure(self):
        """Gets flag indicating whether build is pure python or not.

        """
        return False


def _read(fname):
    """Returns content of a file.

    """
    fpath = os.path.dirname(__file__)
    fpath = os.path.join(fpath, fname)
    with open(fpath, 'r', encoding='utf-8') as fstream:
        return fstream.read()


def _get_version():
    """Returns library version by inspecting __init__.py file.

    """
    return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                     _read("pycspr/__init__.py"),
                     re.MULTILINE).group(1)


# Libary version.
_VERSION = _get_version()

# Library packages.
_PACKAGES = find_packages()

# User readme.
_README = _read('README.rst')


setup(
    name='pycspr',
    version=_VERSION,
    description="Python library for interacting with a CSPR node",
    description_content_type="text/plain",
    long_description=_README,
    long_description_content_type="text/plain",
    author='Mark A. Greenslade',
    author_email='mark@casperlabs.io',
    url='https://github.com/casper-network/casper-python-sdk',
    packages=_PACKAGES,
    include_package_data=True,
    install_requires=_REQUIRES,
    license='Apache-2.0',
    zip_safe=False,
    distclass=_BinaryDistribution,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
