import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="auto_checker",
    version="1.0.1",
    author="Kevin Scaria",
    author_email="scariakevin1@gmail.com",
    description="A  light weight package to check the codes of candidates who interview with me.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevinscaria/autochecker",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
