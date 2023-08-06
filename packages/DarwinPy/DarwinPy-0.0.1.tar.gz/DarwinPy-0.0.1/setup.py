from setuptools import setup, find_packages

classifiers = [
"Development Status :: 5 - Production/Stable",
"Intended Audience :: Developers",
"Operating System :: Microsoft :: Windows :: Windows 10",
"License :: OSI Approved :: MIT License",
"Programming Language :: Python :: 3"
]


setup(
name = "DarwinPy",
version = "0.0.1",
description = "A evolutionary computation module",
long_description = open("README.md").read() + "\n\n" + open("CHANGELOG.txt").read(),
long_description_content_type = "text/markdown",
url = "",
author = "Pius Arhanbhunde",
author_email = "pjacks419@gmail.com",
license = "MIT License",
classifiers = classifiers,
keywords = "evolution",
packages = find_packages(),
install_requires = ['numpy']
)
