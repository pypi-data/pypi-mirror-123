#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import setuptools

with open('docs/README.rst') as fo:
    README = fo.read()

install_requirements = [
    'urllib3',
    'requests',
]

setup_requirements = [
    # TODO: put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    # TODO: put package test requirements here
]

setuptools.setup(
    name='tradernet',
    version='0.1.3',
    description="Interact with Tradernet API",
    long_description=README,
    author="Dmytro Kazanzhy",
    author_email='dkazanzhy@gmail.com',
    url='https://github.com/kazanzhy/tradernet',
    download_url='https://github.com/kazanzhy/tradernet/tarball/main',
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=install_requirements,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    python_requires=">=3.6",
    license="MIT license",
    zip_safe=False,
    keywords='tradernet',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
)
