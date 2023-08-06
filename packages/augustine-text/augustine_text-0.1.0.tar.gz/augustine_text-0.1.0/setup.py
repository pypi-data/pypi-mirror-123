import pathlib

from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name="augustine_text",
    version="0.1.0",
    author="Patrick Shechet",
    author_email="patrick.shechet@gmail.com",
    description=(""),
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kajuberdut/augustine-text",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
