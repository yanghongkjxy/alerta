#!/usr/bin/env python

import setuptools

version = '0.0.1'

setuptools.setup(
    name="alerta-enhance",
    version=version,
    description='Alerta plugin to enhance alerts',
    url='https://github.com/guardian/alerta',
    license='Apache License 2.0',
    author='Nick Satterly',
    author_email='nick.satterly@theguardian.com',
    py_modules=['enhance'],
    install_requires=[
        'alerta-server'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'alerta.plugins': [
            'enhance = alerta.plugins.enhance:EnhanceAlert'
        ]
    }
)