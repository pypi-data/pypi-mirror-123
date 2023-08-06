

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="djangomockingbird",
    version="1.0.2",
    description="The fastest way to write the fastest Django unit tests",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/larsvonschaff/Django-mockingbird",
    author_email="larsvonschaff@gmail.com",
    license="MIT",
    install_requires=["django"],
    packages=["djangomockingbird"],

)

