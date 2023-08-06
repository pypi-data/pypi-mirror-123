import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyapi-framework",
    version=read("VERSION").strip(),
    author="Wael Ramadan",
    author_email="wamramadan@gmail.com",
    description="A simple python REST api framework.",
    license="GPLv3",
    packages=["src"],
    data_files=["VERSION", "requirements.txt", "README.md", "LICENSE"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/WMRamadan/pyapi-framework",
    install_requires=read("requirements.txt").split("\n"),
    include_package_data=True
)
