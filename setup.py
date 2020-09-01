# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    from pip._internal.req import parse_requirements
except ImportError:
    from pip.req import parse_requirements

requirements = parse_requirements(
    os.path.join(os.path.dirname(__file__), 'requirements.txt'),
    session = False
)
try:
    install_requires = [str(requirement.req) for requirement in requirements]
except:
    install_requires = [str(i.requirement) for i in requirements]
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
    install_requires = install_requires,
    entry_points = {
        'console_scripts': [
            '163marker=163marker.main:app'
        ]
    }
)