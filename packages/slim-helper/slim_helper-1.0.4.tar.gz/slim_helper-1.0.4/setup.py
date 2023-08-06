import pathlib
from setuptools import setup

# The directory containing this file
pwd = pathlib.Path(__file__).parent

# The text of the README file
README = (pwd / "README.md").read_text()

pack_name='slim_helper'

# This call to setup() does all the work
setup(
    name=pack_name,
    version="1.0.4",
    python_requires='~=3.8',
    description="Simple helpers",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/xfoobar/slim_helper",
    author="xfoobar",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation'
    ],
    packages=[pack_name],
    include_package_data=True,
    install_requires=[],
    platforms=["all"]
)
