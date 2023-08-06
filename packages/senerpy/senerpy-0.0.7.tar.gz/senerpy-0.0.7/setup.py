import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="senerpy",
    version="0.0.7",
    author="Julio Rodriguez",
    author_email="julio.rodriguez@sener.es",
    description="Librerias para uso de Data Science por parte de SENER",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/stulbfl/senerpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)