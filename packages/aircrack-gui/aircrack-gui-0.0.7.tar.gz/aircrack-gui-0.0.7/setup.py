import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="aircrack-gui",
	version="0.0.7",
	author="Cod3d.",
	description="Python gui for aircrack-ng",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Cod3dDOT/aircrack-gui",
	scripts=["aircrack-gui.py"],
	packages=setuptools.find_packages(),
	install_requires=[
		'pygobject',
		'termcolor',
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Operating System :: OS Independent",
	],
)