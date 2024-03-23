#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0']

test_requirements = [ ]

setup(
    author="CGI Externship Team - Spring 2024",
    author_email='michaesm@rutgers.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    description="This package allows users to generate synthetic data via ChatGPT using a streamlit powered web interface.",
    entry_points={
        'console_scripts': [
            'synthetic_data_llm=synthetic_data_llm.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='synthetic_data_llm',
    name='synthetic_data_llm',
    packages=find_packages(include=['synthetic_data_llm', 'synthetic_data_llm.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/michaesm/synthetic_data_llm',
    version='0.1.0',
    zip_safe=False,
)
