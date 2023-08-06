import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(errors="ignore")

# This call to setup() does all the work
setup(
    name="glorious-markup-language",
    version="1.0.6",
    description="Package for writing and formatting texts and images in Pygame",
    long_description=README,
    long_description_content_type="text/markdown",
    license="CC BY-NC",
    author="Florian Briksa",
    packages=["GML"],
    include_package_data=True,
    install_requires=["pygame",],
)
