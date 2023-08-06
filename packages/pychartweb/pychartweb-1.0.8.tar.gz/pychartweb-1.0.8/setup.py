from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.8'
DESCRIPTION = 'Display Graph'
LONG_DESCRIPTION = 'A package that allows to Display Chart on Browser.'

# Setting up
setup(
    name="pychartweb",
    version=VERSION,
    author="Harsh",
    author_email="<singhharshhs586@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data = True,
    install_requires=['bottle'],
    keywords=['python', 'chart.js', 'show chart'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
