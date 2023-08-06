import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="visualizer-torch",
    version="0.0.3",
    author="neonsecret",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bironsecret/pytorch-model-visualizer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "visualizer"},
    packages=setuptools.find_packages(where="visualizer"),
    python_requires=">=3.6",
    download_url="https://github.com/bironsecret/pytorch-model-visualizer/archive/refs/tags/v0.0.3.tar.gz"
)
