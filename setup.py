#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("READMEPY.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "Click==8.0",
    "Django==3.2.7",
    "django-cors-headers==3.8.0",
    "djangorestframework==3.12.4",
    "drf-yasg==1.20.0",
    "emoji==1.4.2",
    "PyYAML==5.4.1",
    "black==21.7b0",
]

test_requirements = [
    "pytest>=3",
]

setup(
    author="Sotunde Abiodun",
    author_email="sotundeabiodun00@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="DRF Compose generates ready to use API using Django Rest Framework",
    entry_points={
        "console_scripts": [
            "drf-compose=drf_compose.cli:main",
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    include_package_data=True,
    keywords="drf_compose",
    name="drf_compose",
    packages=find_packages(include=["drf_compose", "drf_compose.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/IamAbbey/drf_compose",
    version="0.1.0",
    zip_safe=False,
)
