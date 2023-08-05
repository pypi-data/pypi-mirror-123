from pathlib import Path

from setuptools import find_packages, setup

README = (Path(__file__).parent / "PyPI_README.md").read_text()

setup(
    name="seacorenlp",
    packages=find_packages(exclude=("tests.*", "tests")),
    include_package_data=True,
    version="0.0.2",
    description="SEACoreNLP: A Python NLP Toolkit for Southeast Asian languages",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Wei Qi Leong, Arie Pratama Sutiono",
    author_email="seacorenlp@aisingapore.org",
    license="GNU General Public License v3 (GPLv3)",
    keywords=[
        "NLP",
        "Thai",
        "Vietnamese",
        "Indonesian",
        "Malay",
        "POS Tagging",
        "NER",
        "Constituency Parsing",
        "Dependency Parsing"
    ],
    install_requires=[
        "allennlp==1.5.0",
        "allennlp-models==1.5.0",
        "attacut==1.0.6",
        "benepar==0.2.0",
        "pythainlp==2.2.5",
        "malaya==4.0",
        "networkx==2.5",
        "spacy-thai==0.6.0",
        "ssg==0.0.6",
        "stanza==1.1.1",
        "underthesea==1.2.3"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Indonesian",
        "Natural Language :: Thai",
        "Natural Language :: Vietnamese",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    entry_points={"console_scripts": ["seacorenlp=seacorenlp.__main__:main"]}
)
