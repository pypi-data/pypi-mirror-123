#!/usr/bin/env python

from setuptools import setup
import re
import os

def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

setup(
    name="oceansoundscape",
    version=get_version("oceansoundscape"),
    url='https://docs.mbari.org/oceansoundscape',
    license='GPL',
    description='A python package for analyzing ocean acoustic data',
    author='Danelle Cline',
    author_email='dcline@mbari.org',
    packages=get_packages("oceansoundscape"),
    package_data={
        "oceansoundscape": ["testdata/*.*"],
    },
    include_package_data=True,
    install_requires=[
        "numpy~=1.19.2",
        "h5py~=2.10.0",
        "librosa==0.8.1",
        "matplotlib==3.2.2",
        "opencv-python==4.5.3.56",
        "pandas~=1.1.0",
        "Pillow==8.3.1",
        "scipy==1.6.2",
        "SoundFile==0.10.2"
    ],
    python_requires='>=3.6,<3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    zip_safe=False,
)
