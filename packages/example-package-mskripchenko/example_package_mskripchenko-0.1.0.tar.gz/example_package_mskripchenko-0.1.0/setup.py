from setuptools import setup

setup(
    name='example_package_mskripchenko',
    version='0.1.0',    
    description='A example Python package. Very welcoming',
    author='Maria Skripchenko',
    author_email="idontwanttowritemyrealemail@gmail.com",
    url="https://random-url.com",
    packages=['mskripchenko'],
    install_requires=['numpy',
                      ],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)