import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="fusionprov",
    version="1.1.1",
    description="A python package for retrieving and documenting the provenance of fusion data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fair-for-fusion/fusionprov",
    author="Nathan Cummings",
    author_email="nathan.cummings@ukaea.uk",
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["fusionprov"],
    install_requires=[
        "prov[dot]",
    ],
    entry_points={
        "console_scripts": [
            "mastprov=fusionprov.mastprov:main",
            "imasprov=fusionprov.imasprov:main",
        ]
    },
)