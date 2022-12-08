#!/usr/bin/env python

from setuptools import find_packages, setup

requires = []

# dev_requires = [
#     "spacy",
#     "gensim",
#     "bertopic",
#     "pre-commit",
#     "spacytextblob",
# ]

setup(
    name="yt-watch-history-analyzer",
    version="0.0.1",
    description="YouTube watch history analyzer - \
        shows insights for your watch history",
    url="git@github.com:paulbroek/yt-watch-history-analyzer.git",
    author="Paul Broek",
    author_email="pcbroek@paulbroek.nl",
    license="unlicense",
    install_requires=requires,
    # extras_require={"dev": dev_requires},
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.8",
    zip_safe=False,
)
