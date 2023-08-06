import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bmkgnasir",
    version="0.3.2",
    author="Nasir Nooruddin",
    author_email="nasir@nasir.id",
    description="retrieve latest earthquake information in Indonesia",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nasirnooruddin/latest-indonesia-earthquake",
    project_urls={
        "Website": "http://nasir.id",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #package_dir={"": "src"},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
