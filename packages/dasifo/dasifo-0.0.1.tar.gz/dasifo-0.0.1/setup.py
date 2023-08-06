import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='dasifo',
    version='0.0.1',
    author="larou2si",
    author_email="mohamed.laroussi.1@esprit.tn",
    description="This new Library is 'DAta Science In Full Options = dasifo': ...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larou2si/dasifo",
    download_url="https://github.com/larou2si/dasifo/archive/refs/tags/v0.0.1-alpha.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.7',
    install_requires=['numpy', 'scrapeasy'],
)

# to install this package in your python envirement:
# python3 setup.py sdist bdist_wheel
# pip3 install -e .