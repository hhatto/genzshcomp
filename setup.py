#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import genzshcomp

setup(
    name='genzshcomp',
    version=genzshcomp.__version__,
    description="Automatic generated to zsh completion function, "
                "for Python's Option Parser Modules.",
    long_description=open("README.rst").read(),
    license='New BSD License',
    author='Hideo Hattori',
    author_email='hhatto.jp@gmail.com',
    url='http://bitbucket.org/hhatto/genzshcomp/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: Unix',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Unix Shell',
        'Topic :: System :: Shells',
    ],
    keywords="auto automation bash zsh completion",
    py_modules=['genzshcomp'],
    zip_safe=False,
    entry_points={'console_scripts': ['genzshcomp = genzshcomp:main']},
)
