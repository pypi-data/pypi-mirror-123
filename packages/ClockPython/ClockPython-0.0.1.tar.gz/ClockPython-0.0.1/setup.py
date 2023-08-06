from setuptools import setup

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name='ClockPython',
	version='0.0.1',
	description='Gets the current 12 or 24 hour time',
	py_modules=["clockpython"],
	package_dir={'': 'src'},
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
		"Operating System :: OS Independent",
	],
	long_description=long_description,
	long_description_content_type="text/markdown",
	extras_require = {
		"dev": [
			"pytest>=3.7",
		],
	},
	url="https://github.com/gingerphoenix10/ClockPython",
	author="gingerphoenix10",
	author_email="gingerphoenix10@gmail.com"

)