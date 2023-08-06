import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="hicues",
    version="0.1.0",
    description="Extract cue point locations from Hindenburg Journalist projects",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/andrashann/hicues",
    author="András Hann",
    author_email="dev@hann.io",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Topic :: Utilities"
    ],
    include_package_data = True,
    packages=["hicues"],
    install_requires=["xmltodict","watchdog"],
    entry_points={
        "console_scripts": [
            "hicues=hicues.__main__:main",
        ]
    },
)