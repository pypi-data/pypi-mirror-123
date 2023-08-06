import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

project_id = "tomsk-energosbyt-python"
setuptools.setup(
    name=project_id,
    version="0.0.23a1",
    author=["Alexander Ryazanov", "Anton Zolotukhin"],
    author_email="anton.i.zolotukhin@gmail.com",
    description="Inter RAO API bindings for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonzolotukhin/" + project_id,
    project_urls={
        "Bug Tracker": "https://github.com/antonzolotukhin/" + project_id + "/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        # "console_scripts": ["energosbyt=energosbyt.command_line:main"],
    },
    packages=setuptools.find_packages(exclude=("old", "tests")),
    python_requires=">=3.8",
)
