#!/usr/bin/env python

from setuptools import setup, Command
import sys
import os.path
import subprocess

def main():
    setup(name='eric-rf-snmplibrary',
          version='0.2.2',
          description='Ericsson SNMP Library for Robot Framework',
          author='Davide Battaglia',
          download_url='https://pypi.python.org/pypi/eric-rf-snmplibrary',
          classifiers=[
              'Development Status :: 4 - Beta',
              'Framework :: Robot Framework',
              'Programming Language :: Python :: 2',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Topic :: Software Development :: Testing',
          ],
          packages=['eric-rf-snmplibrary'],
          install_requires=['robotframework', 'pysnmp'],
    )

if __name__ == '__main__':
    main()
