#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

setup(
    name = "finger_sdk",
    author = "Alibaba Cloud · Cloud Security Technology Lab",
    author_email = "",
    version = "0.1",
    keywords = "function symbol recognition",
    description = "a tool for recognizing function symbol",
    packages = find_packages(),
    install_requires = ["requests"],
    url = "https://sec-lab.aliyun.com/",
    license = "GPLv3",
    classifiers = [
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 2.7",
            "Operating System :: OS Independent",
    ],
    project_urls = {
        "github_url": "https://github.com/aliyunav/Finger"
    },
    python_requires = ">=2.7"
)
