import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xlsxToCsv",
    version="1.0.3",
    author="Will Michel",
    author_email="willmichel81@gmail.com",
    description="Takes user specified range data from .xlsx and then converts data to json dict and/or csv.",
    long_description=long_description,
    keywords=["csv","excel","xlsx","excelToCsv","xlsxToCsv"],
    py_modules=["excelToCSV"],
    install_requires=['openpyxl'],
    long_description_content_type="text/markdown",
    url="https://github.com/willmichel81/excelToCSV",
    project_urls={
        "Bug Tracker": "https://github.com/willmichel81/excelToCSV/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    python_requires=">=3.6",
)