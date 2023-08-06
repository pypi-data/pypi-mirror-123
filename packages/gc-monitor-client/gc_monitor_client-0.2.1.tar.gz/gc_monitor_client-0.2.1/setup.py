from os import environ

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gc_monitor_client",
    version=environ.get("VERSION_STRING", "dev"),
    author="Nick Farrell",
    author_email="nick.farrell@genesiscare.com",
    description="Client library for stateful monitoring service",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/genesiscare/python-packages",
    project_urls={
        "Bug Tracker": "https://github.com/genesiscare/python-packages/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
