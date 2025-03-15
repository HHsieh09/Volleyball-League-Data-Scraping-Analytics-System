from os import path
from io import open
from setuptools import setup, find_packages

location = path.abspath(path.dirname(__file__))

with open(path.join(location,"README.md", encoding="utf-8")) as f:
    long_description = f.read()

setup(
    name = "volleyball-data-project",
    version = "1.0.0",
    description = "volleyball data mining",
    long_description = long_description,
    url = "https://github.com/HHsieh09/",
    author = "Henry Hsieh",
    author_email = "henryfbs01@gmail.com",
    classifiers = [
        "Intended Audience :: Developers",
        "Licencse :: GPL-3.0 license",
        "Programming Language :: Python :: 3.9.21",
    ],
    keywords = "volleyball, python, analytics, data engineering",
    project_urls = {
        "source" : "https://github.com/HHsieh09/Volleyball-League-Data-Scraping-Analytics-System",
    },
)