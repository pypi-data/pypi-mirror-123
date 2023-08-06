import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="flyerops",
    version="0.1.6",
    description="Helper functions for AWS and MLOPs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://git.delta.com/158734/flyer_pkg",
    author="Steven Forrester",
    author_email="sjforrester32@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "awswrangler>=2.10.0",
        "pandas>=1.1.5",
        "psycopg2>=2.7.7",
        "SQLAlchemy>=1.4.23",
        "teradatasql>=17.10.0.2",
    ],
)
