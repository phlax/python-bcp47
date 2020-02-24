# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


readme = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'README.md')
with open(readme, encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='python-bcp47',
    version="0.0.4",
    license='GPL3',
    url='https://github.com/phlax/bcp47',
    description=(
        'Parser and validator for language codes (bcp47). '
        'Also exposes the IANA language code database'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ryan Northey',
    author_email='ryan@synca.io',
    project_urls={
        'Source': 'https://github.com/phlax/python-bcp47/',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'test': [
            'flake8==2.4.1',
            'pytest',
            'pytest-cov',
            'codecov'
        ]}
)
