import setuptools
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tippie",
    version="1.0.2",
    author="Aryan Arora",
    author_email="aryanarora232004@gmail.com",
    description="you do not have to bother type hinting in python from now on, tippie will take care of it :)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aryan-debug/tippie",
    project_urls={
        "Music Player": "https://github.com/aryan-debug/Music_Player",
        "Chess Game": "https://github.com/aryan-debug/chess_game"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        'console_scripts': ['tippie=tippie.type_hint:type_hint']
    }
)