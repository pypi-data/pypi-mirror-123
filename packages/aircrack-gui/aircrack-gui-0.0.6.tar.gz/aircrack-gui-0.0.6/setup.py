import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aircrack-gui",
    version="0.0.6",
    author="Cod3d.",
    author_email="demo@email.com",
    description="Python gui for aircrack-ng",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cod3dDOT/aircrack-gui",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)