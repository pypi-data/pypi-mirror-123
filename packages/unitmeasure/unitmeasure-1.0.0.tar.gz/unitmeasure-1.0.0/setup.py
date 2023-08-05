import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="unitmeasure",
    version="1.0.0",
    author="Greg Bock",
    description="Python units and measurements",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gabock/unitmeasure",
    project_urls={
        "Bug Tracker": "https://github.com/gabock/unitmeasure/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)