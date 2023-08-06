import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbmsValCheck",
    version="0.0.2",
    author="Able Analytics LLC",
    author_email="yjjo@able-analytics.com",
    description="The tool for checking validation of a variety of DBMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ojjy/dbmsValCheck",
    project_urls={
        "Bug Tracker": "https://github.com/ojjy/dbmsValCheck/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=["*.sql", "*.SQL", "*.json"]),
    python_requires=">=3.6",
)