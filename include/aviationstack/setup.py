from setuptools import find_packages
from setuptools import setup

setup(
    name="aviationstack",
    version="0.1.0",
    packages=find_packages("src"),
    package_dir={"": "src"},
    license="MIT",
    author="Kalen Willits",
    description="Python Wrapper for the Aviation Stack API."
)
