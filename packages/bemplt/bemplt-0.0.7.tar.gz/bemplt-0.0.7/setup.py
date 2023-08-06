import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bemplt",
    version="0.0.007",
    author="dy1901",
    author_email="gaetan.desrues@inria.fr",
    license="MIT License",
    description="Plot standard ECG chart from data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GaetanDesrues/ecg_plot",  # forked from https://github.com/dy1901/ecg_plot
    packages=["bemplt"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
