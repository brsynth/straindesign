# coding: utf-8
import os
import yaml

from setuptools import setup


# Version
version = ''
with open(os.path.join('pyexchange', '_version.py')) as fid:
    lines = fid.read().splitlines()
    version = lines[0].split("=")[-1].strip().replace('"', '')

# App name - dependencies
env = {}
with open('environment.yml') as fid:
    env = yaml.safe_load(fid)
name = env['name']
install_requires = env['dependencies']

setup(
    name=name,
    version=version,
    author=['guillaume-gricourt'],
    author_email=['guipagui@gmail.com'],
    description='',
    long_description_content_type='text/markdown',
    url='https://github.com/brsynth/rpFbaAnalysis',
    packages=[name],
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    install_requires=install_requires
)
