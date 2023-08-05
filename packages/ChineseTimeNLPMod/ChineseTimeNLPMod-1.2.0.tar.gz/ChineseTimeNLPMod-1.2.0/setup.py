import pathlib
import setuptools
from setuptools import setup

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="ChineseTimeNLPMod",
    version="1.2.0",
    keywords=["chinese time", "chinese time nlp"],
    url="https://github.com/iamtes1a/ChineseTimeNLP",
    author="liveid",
    author_email="",
    long_description_content_type="text/markdown",
    description="将中文时间表达词转为相应的时间字符串，支持时间点，时间段，时间间隔。",
    long_description=README,
    license="MIT Licence",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "arrow >= 0.17.0",
        "loguru >= 0.5.3",
        "regex >= 2020.11.13",
    ],
    classifiers=["Programming Language :: Python :: 3.8"],
)
