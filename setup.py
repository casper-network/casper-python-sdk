import os
import re
from codecs import open

from setuptools import setup
from setuptools import find_packages
from setuptools.dist import Distribution


# List of 3rd party python dependencies.
_REQUIRES = [
    'pytest',
    'tox'
    ]


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
    with open(fpath, 'r', 'utf-8') as file_:
        return file_.read()


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
_README = _read('README.md')



setup(
    name='pycspr',
    version=_VERSION,
    description='Python library for interacting with a CSPR node.',
    long_description=_README,
    author='Mark A. Greenslade',
    author_email='mark@casperlabs.io',
    url='https://github.com/pycspr',
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
        'License :: OSI Approved :: Apache 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
