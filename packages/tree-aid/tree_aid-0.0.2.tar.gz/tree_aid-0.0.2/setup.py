import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tree_aid", 
    version="0.0.2",
    author="180DC Bristol",
    author_email="sv20666@bristol.ac.uk",
    description="ETL tools for Tree Aid",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/charliehpearce/tree_aid_test",
    project_urls={
        "Bug Tracker": "https://github.com/charliehpearce/tree_aid_test/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires = [
        'pandas >= 1.2.0',
        'rasterio >= 1.2.0',
    ],
    include_package_data=True # to include pkg data in install 
)