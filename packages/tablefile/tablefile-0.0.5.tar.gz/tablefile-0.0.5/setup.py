import setuptools

with open("D:/My Folder/PythonWorkshop/MyPyPi_Packages/package_3/readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tablefile", # Package Name
    version="0.0.5",
    author="Dwaipayan Deb",
    author_email="dwaipayandeb@yahoo.co.in",
    description="A package for reading and processing tabular data files for analytical applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dwaipayandeb/scifile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)