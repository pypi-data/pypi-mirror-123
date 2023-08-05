#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "requests",
]

test_requirements = [ ]

setup(
    author="Masaya Kataoka",
    author_email='ms.kataoka@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="simple python client library for github rest API",
    entry_points={
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='python_github',
    name='python_github_api',
    packages=find_packages(include=['python_github', 'python_github.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/hakuturu583/python_github',
    version='0.1.0',
    zip_safe=False,
)
