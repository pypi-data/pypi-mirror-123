#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
import pkg_resources
import versioneer

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Flask-AppBuilder>=1.5.0"]

test_requirements = [
    "pip==19.2.3",
    "bump2version==0.5.11",
    "wheel==0.33.6",
    "watchdog==0.9.0",
    "flake8==3.7.8",
    "tox==3.14.0",
    "coverage==4.5.4",
    "Sphinx==1.8.5",
    "twine==1.14.0",
]

setup(
    author="Jillian Rowe",
    author_email="jillian@dabbleofdevops.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="CoreUI theme for FlaskAppbuilder",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="fab_coreui_theme",
    name="fab_coreui_theme",
    packages=find_packages(include=["fab_coreui_theme", "fab_coreui_theme.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/Dabble-of-DevOps-BioHub/fab_coreui_theme",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    zip_safe=False,
)
