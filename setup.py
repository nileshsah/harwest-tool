# -*- coding: utf-8 -*-


"""setup.py: setuptools control"""


import re
from setuptools import setup, find_packages


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('harwest/harwest.py').read(),
    re.M
).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(
    name = "harwest",
    packages = find_packages(),
    include_package_data=True,
    entry_points = {
        "console_scripts": ['harwest = harwest.harwest:main']
    },
    install_requires = install_requires,
    version = version,
    description = "Harvest code submissions from different platforms to git",
    long_description = long_descr,
    author = "Nilesh Sah",
    author_email = "nilesh.sah13@outlook.com",
    zip_safe=False
)