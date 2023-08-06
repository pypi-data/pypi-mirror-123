import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SearchAlgoPlayground",
    version="1.0.0",
    author="Sritabh Priyadarshi",
    author_email="sobydanny@gmail.com",
    description="Search Algorithm Playground is a python package to work with graph related algorithm, mainly dealing with different Artificial Intelligence Search alorithms.The tool provides an user interface to work with the graphs and visualise the effect of algorithm on the graph while giving the freedom to programmer to make adjustments in the way they wants. It also provides a way to save the graph in json format hence enabling the programmers to share the files and use different algorithm on same graph with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SobyDamn/SearchAlgorithmPlayground",
    project_urls={
        "Bug Tracker": "https://github.com/SobyDamn/SearchAlgorithmPlayground/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: pygame",
    ],
    include_package_data=True,
    package_data={"":[".png"]},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
       "pygame >= 2.0.1",
   ]
)