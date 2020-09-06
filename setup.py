# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    lines = [line.strip() for line in f]
    requirements = [line for line in lines if line and not line.startswith('#')]

setup(
    name = '163marker',
    version = '0.1.0',
    description = 'add "163 key" for media file',
    url = 'http://github.com/nondanee/163marker',
    author = 'nondanee',
    author_email = 'iminezn5656@outlook.com',
    license = 'MIT',
    packages = find_packages(),
    platforms = 'any',
    zip_safe = False,
    python_requires = '>=3.4',
    install_requires = requirements,
    entry_points = {
        'console_scripts': [
            '163marker=163marker.main:app'
        ]
    }
)