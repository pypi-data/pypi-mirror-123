import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Earthquakeupdate-indonesia",
    version="0.1",
    author="Vivi Rosita R",
    author_email="vivirosita.r@gmail.com",
    description="This package will receive the latest earthquake information from BMKG | Meteorological, Climatological,"
                " and Geophysical Agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rosita222-bit/Indonesia-earthquake-monitoring",
    #project_urls={
    #   "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    #},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "src"},
    #packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
