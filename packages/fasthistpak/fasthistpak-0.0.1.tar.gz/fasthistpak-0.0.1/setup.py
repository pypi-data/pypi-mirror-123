from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Test Python package with method that creates histogram'
LONG_DESCRIPTION = 'Test Python package without long description'

# Setting up
setup(
        name="fasthistpak", 
        version=VERSION,
        author="Aleksandr Pak",
        author_email="sancho20021@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'typing'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
