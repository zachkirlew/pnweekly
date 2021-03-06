#!/usr/bin/env python

from setuptools import setup

setup(
    # GETTING-STARTED: set your app name:
    name='PN Weekly',
    # GETTING-STARTED: set your app version:
    version='1.0',
    # GETTING-STARTED: set your app description:
    description='The dankest news app fo real',
    # GETTING-STARTED: set author name (your name):
    author='Group 8',
    # GETTING-STARTED: set author email (your email):
    author_email='zach_kirlew@hotmail.co.uk',
    # GETTING-STARTED: set author url (your url):
    url='http://www.python.org/sigs/distutils-sig/',
    # GETTING-STARTED: define required django version:
    install_requires=[
        'Django==1.11.5',
        'django-cookie-law==1.0.13',
        'djangorestframework==3.7.3',
        'requests==2.18.4',
        'Pillow==4.3.0'
    ],
    dependency_links=[
        'https://pypi.python.org/simple/django/'
    ],
)
