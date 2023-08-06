from setuptools import setup, find_packages

VERSION = '1.1.1' 
DESCRIPTION = 'Evolutionary DBSCAN and Louvain Method with a Twitter data stream'
LONG_DESCRIPTION = open("README.md").read()
INSTALL_REQUIRES = ['numpy>=1.20.3',
                    'pandas>=1.2.5',
                    'scikit-learn>=0.24.2',
                    'matplotlib>=3.4.2',
                    'python-louvain>=0.13',
                    'tweepy==3.8.0',
                    'networkx>=2.6.1']

setup(
        name="evoclusterstream",
        version=VERSION,
        url="https://github.com/kspurlock/EvoClusterStream",
        author="Kyle Spurlock, Heba Elgazzar, Tanner Bogart",
        author_email="<kdspurlock@moreheadstate.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES,
        license='MIT',
        keywords=["Unsupervised machine learning", "evolutionary clustering",
                  "social networks", "Python", "DBSCAN", "Louvain method"],
        classifiers= [
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
        include_package_data=True,
        package_data={'':['data/*.csv']},
)