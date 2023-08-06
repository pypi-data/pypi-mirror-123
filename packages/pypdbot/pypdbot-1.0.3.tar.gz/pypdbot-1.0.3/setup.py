import os
import setuptools
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme:
    long_description = readme.read()

setuptools.setup(
    name="pypdbot",
    version="1.0.3",
    author="Ravi raj purohit PURUSHOTTAM RAJ PUROHIT",
    author_email="purushot@esrf.fr",
    description="GUI routine for binance based automated bot",
    long_description=long_description ,
    long_description_content_type="text/markdown",
    packages=["pypdbot"],
    url="https://github.com/ravipurohit1991/pypdbot",
    install_requires=['twisted', 'autobahn', 'beautifulsoup4', 'selenium','matplotlib','PyQt5','numpy'],
    entry_points={
                 "console_scripts": ["pypdbot=pypdbot.pumpdumppyqtlite:start"]
                },
    classifiers=[
                    "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent",
                ],
    python_requires='>=3.6',
)