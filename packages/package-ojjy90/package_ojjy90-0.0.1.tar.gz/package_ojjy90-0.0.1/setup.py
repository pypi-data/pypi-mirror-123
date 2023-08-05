import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="package_ojjy90",
    version="0.0.1",
    author="Yejin Jo",
    author_email="ojjy90@gmail.com",
    description="ojjy90 let it go",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "package"},
    packages=setuptools.find_packages(where="package"),
    python_requires=">=3.6",
    test_suite="tests",
)