# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='python-bcp47',
    version="0.0.1",
    license='GPL3',
    url='https://github.com/phlax/bcp47',
    description='Parser and validator for language codes (bcp47)',
    author='Ryan Northey',
    author_email='ryan@synca.io',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],

    packages=find_packages(),
    zip_safe=False,
    extras_require={
        'test': [
            'flake8==2.4.1',
            'pytest',
            'pytest-cov',
            'codecov'
        ]}
)
