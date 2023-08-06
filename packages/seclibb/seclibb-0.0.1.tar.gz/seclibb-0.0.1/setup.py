import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seclibb",
    version="0.0.1",
    author="Alrahl",
    author_email="author@example.com",
    description="seclibb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IT-Err0R/1sec-lib",
    project_urls={
        "Bug Tracker": "https://github.com/IT-Err0R/1sec-lib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
