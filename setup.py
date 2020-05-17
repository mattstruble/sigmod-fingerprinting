from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="sigmod_fingerprinting",
    version="1.0.0",
    author="Matt Struble",
    descripion='Python implementation of the algorithm defined in "Winnowing: Local Algorithms for Document Fingerprinting"',
    long_description=long_description,
    url="https://github.com/mattstruble/sigmod-fingerprinting",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    license='MIT',
    zip_safe=True
)