import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twneo",
    version="0.0.6",
    author="Pankaj Kumar",
    author_email="kumarp@mail.smu.edu",
    description=" uses twitter api to create neo4j graphs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pankajti/twneo",
    project_urls={
        "Bug Tracker": "https://github.com/pankajti/twneo/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages( ),
    python_requires=">=3.6",
    include_package_data = True
)