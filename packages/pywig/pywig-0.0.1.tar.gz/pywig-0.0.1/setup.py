import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywig",
    version="0.0.1",
    description="A Python package made to create HTML files and web pages seamlessly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BobBrown1/pywig",
    project_urls={
        "Bug Tracker": "https://github.com/BobBrown1/pywig/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires = ["regex"]
)