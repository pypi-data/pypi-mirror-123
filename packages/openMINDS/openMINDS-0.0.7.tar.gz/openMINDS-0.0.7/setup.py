import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openMINDS",
    version="0.0.7",
    author="Stefan Köhnen",
    author_email="s.koehnen@fz-juelich.de",
    description="Python library for interacting with openMINDS metadata schemas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HumanBrainProject/openMINDS_generator",
    project_urls={
        "Bug Tracker": "https://github.com/HumanBrainProject/openMINDS_generator/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "click==8.0.1",
        "jsonschema==4.1.0",
        "requests==2.26.0",
        "GitPython==3.1.24"
    ],
    python_requires=">=3.6",
)
