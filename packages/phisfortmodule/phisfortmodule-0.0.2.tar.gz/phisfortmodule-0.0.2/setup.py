from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'PhisFort mostly used method for harvesting url on a link.'
LONG_DESCRIPTION = 'This module contains hundred of repetitive method. That will help to reduce the coding complexity.'

# Setting up
setup(
       # the name must match the folder name 'phisfortmodule'
        name="phisfortmodule", 
        version=VERSION,
        author="Adil Reza",
        author_email="adilreza043@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        # install_requires=["fuzzywuzzy", "requests", "tarfile", "zipfile", ""], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        url="https://github.com/adilreza",
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)