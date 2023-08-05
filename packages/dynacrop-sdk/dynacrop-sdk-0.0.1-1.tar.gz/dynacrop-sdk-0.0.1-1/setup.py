from setuptools import setup, find_packages

VERSION = '0.0.1_1'
LONG_DESCRIPTION = 'Python Software Development Kit library for DynaCrop API'

setup(
    name="dynacrop-sdk",                     # This is the name of the package
    version=VERSION,                        # The initial release version
    author='Jan Chytrý',                     # Full name of the author
    description="Python Software Development Kit library for DynaCrop API",
    long_description=LONG_DESCRIPTION,      # Long description read from the the readme file
    packages=find_packages(),    # List of all python modules to be installed
    install_requires=[],                     # Install other dependencies if any
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.7',                # Minimum version requirement of the package
)