# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:52:11 2022

@author: ELNN
"""

from setuptools import setup

setup(
    name='timearea',
    version='1.1.0',    
    description='Python Package for calculating a time area curve for a Mike Urban Database',
    url='https://github.com/enielsen93/timearea',
    author='Emil Nielsen',
    author_email='enielsen93@hotmail.com',
    license='BSD 2-clause',
    packages=['timearea'],
    install_requires=['networker', 'networkx', 'ColebrookWhite', 'mikegraph'],
    dependency_links=['https://github.com/enielsen93/networker/tarball/master', 'https://github.com/enielsen93/ColebrookWhite/tarball/master', 'https://github.com/enielsen93/mikegraph/tarball/master'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)