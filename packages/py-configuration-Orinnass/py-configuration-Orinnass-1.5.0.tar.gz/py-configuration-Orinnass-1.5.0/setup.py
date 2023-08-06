#!/usr/bin/env python

from setuptools import setup
from setuptools import find_packages
from config import __version__, __name__


def get_install_requires():
    with open('requirements.txt', 'r') as file_req:
        lines_req = file_req.readlines()
        for index, i in enumerate(lines_req):
            if '-e' in i:
                module_name = i.split('#egg=')[1].strip()
                install_command = i.split('-e ')[1].strip()
                lines_req[index] = f'{module_name} @ {install_command}\n'
        return lines_req


setup(
    name=__name__,
    version=__version__,
    download_url="https://gitlab.com/Orinnass/python-module-configuration",
    packages=find_packages(include=('config',), exclude=('test',)),
    install_requires=['PyMySQL==1.0.2', 'pyrsistent==0.18.0', 'six==1.16.0', 'coverage==5.5', 'attrs==21.2.0'],
    setup_requires=['PyMySQL==1.0.2', 'pyrsistent==0.18.0', 'six==1.16.0', 'coverage==5.5', 'attrs==21.2.0'],
    scripts=['cli.py']
)
