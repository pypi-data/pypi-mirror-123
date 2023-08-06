# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-keycloak-jea',
    version='0.26.1',
    url='https://bitbucket.org/j-and-a/python-keycloak-jea.git',
    download_url='https://bitbucket.org/j-and-a/python-keycloak-jea/get/release0.1.tar.gz',
    license='The MIT License',
    author='Leandro de Souza',
    author_email='marcospereira.mpj@gmail.com',
    keywords='keycloak openid jea',
    description='python-keycloak is a Python package providing access to the Keycloak API.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['keycloak', 'keycloak.authorization', 'keycloak.tests'],
    install_requires=['requests>=2.20.0', 'python-jose>=1.4.0'],
    tests_require=['httmock>=1.2.5'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Utilities'
    ]
)
