import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stdpio",
    version="0.0.9",
    author="stdp",
    author_email="info@stdp.io",
    description="A library to interact with the stdp.io REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Apache License 2.0",
    url="https://stdp.io",
    keywords=[
        "stdp",
        "stdp.io",
        "neuromorphic",
        "akida",
        "brainchip",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/stdp/stdpio/issues",
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
